#!/usr/bin/env python3
"""
Service Versioning CLI Tool

This script automates the creation of new API versions for services,
creating copies of routes and updating documentation automatically.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import json
import re

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

class ServiceVersionManager:
    """Manages versioning of individual services"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.backend_dir = base_dir / "backend"
        self.modules_dir = self.backend_dir / "app" / "modules"
        self.api_dir = self.backend_dir / "app" / "api"
        
    def version_service(self, module: str, service: str, from_version: str, to_version: str) -> bool:
        """
        Create a new version of a specific service
        
        Args:
            module: Module name (e.g., 'health')
            service: Service name (e.g., 'agendamento_consulta') 
            from_version: Source version (e.g., 'v1')
            to_version: Target version (e.g., 'v2')
            
        Returns:
            True if successful, False otherwise
        """
        print(f"🔄 Versioning service {module}/{service} from {from_version} to {to_version}...")
        
        # Validate paths
        module_path = self.modules_dir / module
        if not module_path.exists():
            print(f"❌ Module {module} not found")
            return False
            
        # Source and target paths
        source_route = module_path / "routes" / f"{service}.py"
        source_schema = module_path / "schemas" / f"{service}.py"
        source_model = module_path / "models" / f"{service}.py"
        
        if not source_route.exists():
            print(f"❌ Service route {service} not found in {module}")
            return False
            
        # Create versioned copies
        try:
            # Create version directories if they don't exist
            version_routes_dir = module_path / "routes" / to_version
            version_schemas_dir = module_path / "schemas" / to_version
            version_models_dir = module_path / "models" / to_version
            
            version_routes_dir.mkdir(parents=True, exist_ok=True)
            version_schemas_dir.mkdir(parents=True, exist_ok=True)
            version_models_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy files to versioned directories
            target_route = version_routes_dir / f"{service}.py"
            target_schema = version_schemas_dir / f"{service}.py"
            target_model = version_models_dir / f"{service}.py"
            
            shutil.copy2(source_route, target_route)
            if source_schema.exists():
                shutil.copy2(source_schema, target_schema)
            if source_model.exists():
                shutil.copy2(source_model, target_model)
                
            # Update import paths in the copied files
            self._update_imports_for_version(target_route, module, to_version)
            if target_schema.exists():
                self._update_imports_for_version(target_schema, module, to_version)
            if target_model.exists():
                self._update_imports_for_version(target_model, module, to_version)
                
            # Update API prefix in route
            self._update_api_prefix(target_route, to_version)
            
            print(f"✅ Service {service} versioned successfully to {to_version}")
            return True
            
        except Exception as e:
            print(f"❌ Error versioning service: {str(e)}")
            return False
            
    def _update_imports_for_version(self, file_path: Path, module: str, version: str):
        """Update import statements for versioned files"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update relative imports to include version
        patterns = [
            (rf'from app\.modules\.{module}\.schemas\.', f'from app.modules.{module}.schemas.{version}.'),
            (rf'from app\.modules\.{module}\.models\.', f'from app.modules.{module}.models.{version}.'),
            (rf'from \.\.schemas\.', f'from ..schemas.{version}.'),
            (rf'from \.\.models\.', f'from ..models.{version}.'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def _update_api_prefix(self, route_file: Path, version: str):
        """Update API prefix in route file"""
        with open(route_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update router prefix to include version
        content = re.sub(
            r'router = APIRouter\(prefix="/api/([^"]+)"',
            rf'router = APIRouter(prefix="/api/{version}/\1"',
            content
        )
        
        with open(route_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def version_entire_module(self, module: str, from_version: str, to_version: str) -> bool:
        """Version all services in a module"""
        print(f"🔄 Versioning entire module {module} from {from_version} to {to_version}...")
        
        module_path = self.modules_dir / module
        routes_dir = module_path / "routes"
        
        if not routes_dir.exists():
            print(f"❌ Routes directory not found for module {module}")
            return False
            
        success_count = 0
        total_count = 0
        
        # Find all Python files in routes directory (excluding __init__.py)
        for route_file in routes_dir.glob("*.py"):
            if route_file.name == "__init__.py":
                continue
                
            service_name = route_file.stem
            total_count += 1
            
            if self.version_service(module, service_name, from_version, to_version):
                success_count += 1
                
        print(f"📊 Module versioning complete: {success_count}/{total_count} services versioned")
        return success_count == total_count
        
    def list_services(self, module: str = None) -> Dict[str, List[str]]:
        """List all services, optionally filtered by module"""
        services = {}
        
        modules_to_check = [module] if module else [d.name for d in self.modules_dir.iterdir() if d.is_dir()]
        
        for mod in modules_to_check:
            mod_path = self.modules_dir / mod / "routes"
            if not mod_path.exists():
                continue
                
            service_list = []
            for route_file in mod_path.glob("*.py"):
                if route_file.name != "__init__.py":
                    service_list.append(route_file.stem)
                    
            if service_list:
                services[mod] = sorted(service_list)
                
        return services
        
    def generate_version_docs(self, version: str):
        """Generate documentation for a specific API version"""
        docs_dir = self.base_dir / "docs" / "versions"
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        version_doc = docs_dir / f"api_{version}.md"
        
        services = self.list_services()
        
        doc_content = f"""# SILA API {version.upper()} Documentation

Generated automatically by version-service CLI tool.

## Services Overview

Total Services: {sum(len(svc_list) for svc_list in services.values())}
Modules: {len(services)}

## Modules and Services

"""
        
        for module, service_list in sorted(services.items()):
            doc_content += f"### {module.title()} Module ({len(service_list)} services)\n\n"
            for service in service_list:
                doc_content += f"- `/api/{version}/{service.replace('_', '-')}` → **{service.replace('_', ' ').title()}**\n"
            doc_content += "\n"
            
        doc_content += f"""
## Version Features

- All {version.upper()} endpoints follow REST conventions
- Bilingual support (Portuguese/English)
- Comprehensive error handling
- OpenAPI/Swagger documentation available at `/docs`

## Migration Guide

See `/docs/migration_{version}.md` for detailed migration instructions.

*Generated on: {__import__('datetime').datetime.now().isoformat()}*
"""

        with open(version_doc, 'w', encoding='utf-8') as f:
            f.write(doc_content)
            
        print(f"📝 Documentation generated: {version_doc}")

def main():
    parser = argparse.ArgumentParser(description="SILA Service Versioning Tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Version single service
    version_parser = subparsers.add_parser('version', help='Version a single service')
    version_parser.add_argument('module', help='Module name')
    version_parser.add_argument('service', help='Service name')
    version_parser.add_argument('--from', dest='from_version', default='v1', help='Source version')
    version_parser.add_argument('--to', dest='to_version', required=True, help='Target version')
    
    # Version entire module
    module_parser = subparsers.add_parser('version-module', help='Version entire module')
    module_parser.add_argument('module', help='Module name')
    module_parser.add_argument('--from', dest='from_version', default='v1', help='Source version')
    module_parser.add_argument('--to', dest='to_version', required=True, help='Target version')
    
    # List services
    list_parser = subparsers.add_parser('list', help='List all services')
    list_parser.add_argument('--module', help='Filter by module')
    list_parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    # Generate docs
    docs_parser = subparsers.add_parser('docs', help='Generate version documentation')
    docs_parser.add_argument('version', help='Version to document (e.g., v1, v2)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    # Initialize manager
    base_dir = Path(__file__).parent.parent
    manager = ServiceVersionManager(base_dir)
    
    try:
        if args.command == 'version':
            success = manager.version_service(
                args.module, 
                args.service, 
                args.from_version, 
                args.to_version
            )
            sys.exit(0 if success else 1)
            
        elif args.command == 'version-module':
            success = manager.version_entire_module(
                args.module,
                args.from_version, 
                args.to_version
            )
            sys.exit(0 if success else 1)
            
        elif args.command == 'list':
            services = manager.list_services(args.module)
            
            if args.format == 'json':
                print(json.dumps(services, indent=2))
            else:
                for module, service_list in sorted(services.items()):
                    print(f"\n📦 {module} ({len(service_list)} services):")
                    for service in service_list:
                        print(f"  • {service}")
                        
        elif args.command == 'docs':
            manager.generate_version_docs(args.version)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()