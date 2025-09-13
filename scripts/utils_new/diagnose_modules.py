#!/usr/bin/env python3
"""
Module Registration Diagnostic Tool
Identifies which modules have routers and checks if they are registered in main.py.
"""

import os
import ast
import re
from pathlib import Path
from typing import List, Dict, Set, Optional

class ModuleDiagnostic:
    """Diagnoses module registration issues."""
    
    def __init__(self, backend_dir: Path):
        self.backend_dir = backend_dir
        self.modules_dir = backend_dir / "app" / "modules"
        self.api_file = backend_dir / "app" / "api" / "v1" / "api.py"
        self.main_app_file = backend_dir / "app" / "core" / "application.py"
        
    def find_modules_with_routers(self) -> Dict[str, Dict]:
        """Find all modules that have router definitions."""
        modules_with_routers = {}
        
        if not self.modules_dir.exists():
            print(f"❌ Modules directory not found: {self.modules_dir}")
            return modules_with_routers
        
        for module_dir in self.modules_dir.iterdir():
            if not module_dir.is_dir() or module_dir.name.startswith('_'):
                continue
                
            router_info = self.analyze_module_router(module_dir)
            if router_info['has_router']:
                modules_with_routers[module_dir.name] = router_info
                
        return modules_with_routers
    
    def analyze_module_router(self, module_dir: Path) -> Dict:
        """Analyze a module directory for router definitions."""
        router_info = {
            'has_router': False,
            'router_files': [],
            'router_names': [],
            'endpoints': []
        }
        
        # Common router file names
        router_files = ['router.py', 'routes.py', 'endpoints.py', '__init__.py']
        
        for file_name in router_files:
            file_path = module_dir / file_name
            if file_path.exists():
                routers = self.extract_routers_from_file(file_path)
                if routers:
                    router_info['has_router'] = True
                    router_info['router_files'].append(file_name)
                    router_info['router_names'].extend(routers['names'])
                    router_info['endpoints'].extend(routers['endpoints'])
        
        return router_info
    
    def extract_routers_from_file(self, file_path: Path) -> Optional[Dict]:
        """Extract router information from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            routers = {'names': [], 'endpoints': []}
            
            # Look for APIRouter definitions
            router_pattern = r'(\w+)\s*=\s*APIRouter\s*\('
            router_matches = re.findall(router_pattern, content)
            routers['names'].extend(router_matches)
            
            # Look for route decorators
            route_patterns = [
                r'@(\w+)\.(?:get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']',
                r'@router\.(?:get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in route_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if len(match) == 2:
                        routers['endpoints'].append(match[1])
                    else:
                        routers['endpoints'].append(match)
            
            # Also check with AST for more reliable parsing
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and isinstance(node.value, ast.Call):
                                if (isinstance(node.value.func, ast.Name) and 
                                    node.value.func.id == 'APIRouter'):
                                    routers['names'].append(target.id)
            except SyntaxError:
                pass  # Skip files with syntax errors
            
            return routers if routers['names'] or routers['endpoints'] else None
            
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")
            return None
    
    def check_registration_in_api(self, module_name: str) -> Dict:
        """Check if a module is registered in the API router."""
        registration_info = {
            'is_registered': False,
            'import_found': False,
            'include_found': False,
            'import_line': '',
            'include_line': ''
        }
        
        if not self.api_file.exists():
            print(f"❌ API file not found: {self.api_file}")
            return registration_info
        
        try:
            with open(self.api_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for import statements
            import_patterns = [
                fr'from\s+app\.modules\.{module_name}(?:\.router|\.routes|\.endpoints)?\s+import\s+\w+',
                fr'from\s+app\.modules\.{module_name}\s+import\s+\w+',
                fr'import\s+app\.modules\.{module_name}(?:\.router|\.routes)?'
            ]
            
            for pattern in import_patterns:
                match = re.search(pattern, content, re.MULTILINE)
                if match:
                    registration_info['import_found'] = True
                    registration_info['import_line'] = match.group(0)
                    break
            
            # Check for include_router statements
            include_patterns = [
                fr'api_router\.include_router\([^)]*{module_name}[^)]*\)',
                fr'include_router\([^)]*{module_name}[^)]*\)'
            ]
            
            for pattern in include_patterns:
                match = re.search(pattern, content, re.MULTILINE)
                if match:
                    registration_info['include_found'] = True
                    registration_info['include_line'] = match.group(0)
                    break
            
            registration_info['is_registered'] = (
                registration_info['import_found'] and registration_info['include_found']
            )
            
        except Exception as e:
            print(f"⚠️ Error reading API file: {e}")
        
        return registration_info
    
    def generate_report(self) -> Dict:
        """Generate comprehensive diagnostic report."""
        print("🔍 Diagnosing module registration...")
        
        modules_with_routers = self.find_modules_with_routers()
        
        report = {
            'total_modules': len(list(self.modules_dir.iterdir())) - 1,  # Exclude __pycache__
            'modules_with_routers': len(modules_with_routers),
            'registered_modules': 0,
            'unregistered_modules': 0,
            'details': {}
        }
        
        print(f"\n📊 Found {len(modules_with_routers)} modules with routers:")
        
        for module_name, router_info in modules_with_routers.items():
            registration_info = self.check_registration_in_api(module_name)
            
            report['details'][module_name] = {
                'router_info': router_info,
                'registration_info': registration_info
            }
            
            if registration_info['is_registered']:
                report['registered_modules'] += 1
                status = "✅ REGISTERED"
            else:
                report['unregistered_modules'] += 1
                status = "❌ NOT REGISTERED"
            
            print(f"\n📦 {module_name} - {status}")
            print(f"   Router files: {', '.join(router_info['router_files'])}")
            print(f"   Router names: {', '.join(router_info['router_names'])}")
            print(f"   Endpoints: {len(router_info['endpoints'])} found")
            
            if not registration_info['is_registered']:
                if not registration_info['import_found']:
                    print(f"   ⚠️ Missing import statement")
                if not registration_info['include_found']:
                    print(f"   ⚠️ Missing include_router statement")
        
        return report
    
    def print_summary(self, report: Dict):
        """Print diagnostic summary."""
        print(f"\n" + "="*50)
        print(f"📋 DIAGNOSTIC SUMMARY")
        print(f"="*50)
        print(f"Total modules: {report['total_modules']}")
        print(f"Modules with routers: {report['modules_with_routers']}")
        print(f"✅ Registered: {report['registered_modules']}")
        print(f"❌ Unregistered: {report['unregistered_modules']}")
        
        if report['unregistered_modules'] > 0:
            print(f"\n🔧 Modules needing registration:")
            for module_name, details in report['details'].items():
                if not details['registration_info']['is_registered']:
                    print(f"   • {module_name}")
            
            print(f"\n💡 Run 'python scripts/main.py auto-register-modules' to fix automatically")
        else:
            print(f"\n🎉 All modules are properly registered!")

def main():
    """Main diagnostic function."""
    backend_dir = Path(__file__).parent.parent.parent / "backend"
    
    if not backend_dir.exists():
        print(f"❌ Backend directory not found: {backend_dir}")
        return False
    
    diagnostic = ModuleDiagnostic(backend_dir)
    report = diagnostic.generate_report()
    diagnostic.print_summary(report)
    
    return report['unregistered_modules'] == 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)