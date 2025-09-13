#!/usr/bin/env python3
"""
Auto Module Registration Tool
Automatically inserts missing imports and include_router statements into backend/main.py.
Ensures all modules under app/modules/ are exposed as /api/{module}.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))
from diagnose_modules import ModuleDiagnostic

class ModuleAutoRegistrar:
    """Automatically registers missing modules in the API router."""
    
    def __init__(self, backend_dir: Path):
        self.backend_dir = backend_dir
        self.api_file = backend_dir / "app" / "api" / "v1" / "api.py"
        self.diagnostic = ModuleDiagnostic(backend_dir)
        
    def get_unregistered_modules(self) -> Dict[str, Dict]:
        """Get modules that need registration."""
        modules_with_routers = self.diagnostic.find_modules_with_routers()
        unregistered = {}
        
        for module_name, router_info in modules_with_routers.items():
            registration_info = self.diagnostic.check_registration_in_api(module_name)
            if not registration_info['is_registered']:
                unregistered[module_name] = {
                    'router_info': router_info,
                    'registration_info': registration_info
                }
        
        return unregistered
    
    def determine_router_import(self, module_name: str, router_info: Dict) -> str:
        """Determine the correct import statement for a module's router."""
        # Check if router.py exists
        module_dir = self.backend_dir / "app" / "modules" / module_name
        
        if (module_dir / "router.py").exists():
            return f"from app.modules.{module_name}.router import router as {module_name}_router"
        elif (module_dir / "routes.py").exists():
            return f"from app.modules.{module_name}.routes import router as {module_name}_router"
        elif (module_dir / "endpoints.py").exists():
            return f"from app.modules.{module_name}.endpoints import router as {module_name}_router"
        else:
            # Fallback to the first found router name
            if router_info['router_names']:
                router_name = router_info['router_names'][0]
                if router_info['router_files']:
                    file_name = router_info['router_files'][0].replace('.py', '')
                    return f"from app.modules.{module_name}.{file_name} import {router_name} as {module_name}_router"
            
            # Default fallback
            return f"from app.modules.{module_name} import router as {module_name}_router"
    
    def generate_include_statement(self, module_name: str) -> str:
        """Generate the include_router statement for a module."""
        return f'api_router.include_router({module_name}_router, prefix="/{module_name}", tags=["{module_name.title()}"])'
    
    def backup_api_file(self) -> Path:
        """Create a backup of the current API file."""
        backup_path = self.api_file.with_suffix('.py.backup')
        import shutil
        shutil.copy2(self.api_file, backup_path)
        return backup_path
    
    def update_api_file(self, unregistered_modules: Dict[str, Dict]) -> bool:
        """Update the API file with missing module registrations."""
        if not self.api_file.exists():
            print(f"❌ API file not found: {self.api_file}")
            return False
        
        # Create backup
        backup_path = self.backup_api_file()
        print(f"📄 Created backup: {backup_path}")
        
        try:
            with open(self.api_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Find the location to add imports (after existing imports)
            import_section_end = self.find_import_section_end(content)
            
            # Find the location to add include_router statements
            include_section_end = self.find_include_section_end(content)
            
            # Prepare new imports and includes
            new_imports = []
            new_includes = []
            
            for module_name, details in unregistered_modules.items():
                router_info = details['router_info']
                registration_info = details['registration_info']
                
                # Add import if missing
                if not registration_info['import_found']:
                    import_stmt = self.determine_router_import(module_name, router_info)
                    new_imports.append(import_stmt)
                
                # Add include if missing
                if not registration_info['include_found']:
                    include_stmt = self.generate_include_statement(module_name)
                    new_includes.append(include_stmt)
            
            # Insert new imports
            if new_imports:
                lines = content.split('\n')
                import_line = import_section_end
                
                for import_stmt in new_imports:
                    lines.insert(import_line, import_stmt)
                    import_line += 1
                
                content = '\n'.join(lines)
                print(f"✅ Added {len(new_imports)} import statements")
            
            # Insert new includes
            if new_includes:
                lines = content.split('\n')
                # Recalculate include section end after imports were added
                include_line = self.find_include_section_end(content)
                
                for include_stmt in new_includes:
                    lines.insert(include_line, include_stmt)
                    include_line += 1
                
                content = '\n'.join(lines)
                print(f"✅ Added {len(new_includes)} include_router statements")
            
            # Write updated content
            with open(self.api_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Updated API file: {self.api_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating API file: {e}")
            # Restore backup
            import shutil
            shutil.copy2(backup_path, self.api_file)
            print(f"🔄 Restored backup")
            return False
    
    def find_import_section_end(self, content: str) -> int:
        """Find the line number where imports end."""
        lines = content.split('\n')
        
        last_import_line = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (stripped.startswith('from ') or stripped.startswith('import ')) and not stripped.startswith('#'):
                last_import_line = i
        
        # Find the next non-empty line after imports
        for i in range(last_import_line + 1, len(lines)):
            if lines[i].strip():
                return i
        
        return last_import_line + 1
    
    def find_include_section_end(self, content: str) -> int:
        """Find the line number where include_router statements end."""
        lines = content.split('\n')
        
        last_include_line = 0
        for i, line in enumerate(lines):
            if 'include_router' in line and not line.strip().startswith('#'):
                last_include_line = i
        
        # If no includes found, find after router creation
        if last_include_line == 0:
            for i, line in enumerate(lines):
                if 'api_router = APIRouter()' in line:
                    return i + 2  # Add some space
        
        return last_include_line + 1
    
    def register_modules(self) -> bool:
        """Main function to register all unregistered modules."""
        print("🔧 Auto-registering missing modules...")
        
        unregistered_modules = self.get_unregistered_modules()
        
        if not unregistered_modules:
            print("✅ All modules are already registered!")
            return True
        
        print(f"📦 Found {len(unregistered_modules)} unregistered modules:")
        for module_name in unregistered_modules.keys():
            print(f"   • {module_name}")
        
        # Update the API file
        success = self.update_api_file(unregistered_modules)
        
        if success:
            print(f"\n🎉 Successfully registered {len(unregistered_modules)} modules!")
            print(f"💡 All modules are now exposed as /api/v1/{{module}}")
            print(f"🔄 Please restart your backend server to apply changes")
        
        return success

def main():
    """Main auto-registration function."""
    backend_dir = Path(__file__).parent.parent.parent / "backend"
    
    if not backend_dir.exists():
        print(f"❌ Backend directory not found: {backend_dir}")
        return False
    
    registrar = ModuleAutoRegistrar(backend_dir)
    return registrar.register_modules()

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)