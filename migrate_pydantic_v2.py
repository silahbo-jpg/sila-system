#!/usr/bin/env python3
"""
Comprehensive Pydantic V1 to V2 Migration Script for SILA System
Fixes all aggressive migration errors definitively
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class PydanticV2Migrator:
    def __init__(self, backend_path: str = "backend"):
        self.backend_path = Path(backend_path)
        self.fixes_applied = []
        self.errors_found = []
        
    def log_fix(self, file_path: str, fix_type: str, details: str = ""):
        """Log applied fixes"""
        self.fixes_applied.append(f"[{fix_type}] {file_path}: {details}")
        print(f"✅ Fixed: {fix_type} in {file_path}")
        
    def log_error(self, file_path: str, error: str):
        """Log errors encountered"""
        self.errors_found.append(f"❌ {file_path}: {error}")
        print(f"❌ Error: {file_path}: {error}")

    def fix_validator_imports(self, file_path: Path) -> bool:
        """Fix Pydantic imports to include V2 validators"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern to match pydantic imports
            import_pattern = r'from pydantic import ([^#\n]+)'
            
            def update_import(match):
                imports = match.group(1)
                import_list = [imp.strip() for imp in imports.split(',')]
                
                # Add missing V2 imports
                needed_imports = set()
                if 'validator' in imports and 'field_validator' not in imports:
                    needed_imports.add('field_validator')
                if '@model_validator' in content and 'model_validator' not in imports:
                    needed_imports.add('model_validator')
                if 'ConfigDict' not in imports and ('class Config:' in content or 'orm_mode' in content):
                    needed_imports.add('ConfigDict')
                
                # Add new imports
                for imp in needed_imports:
                    if imp not in import_list:
                        import_list.append(imp)
                
                return f"from pydantic import {', '.join(sorted(import_list))}"
            
            content = re.sub(import_pattern, update_import, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log_fix(str(file_path), "IMPORTS", "Added V2 validator imports")
                return True
                
        except Exception as e:
            self.log_error(str(file_path), f"Import fix failed: {e}")
        return False

    def fix_validators(self, file_path: Path) -> bool:
        """Convert @validator to @field_validator with proper V2 syntax"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix simple field validators
            validator_pattern = r'@validator\([\'"]([^\'"]+)[\'"]\s*(?:,\s*pre=True|,\s*pre=False)?\s*\)\s*\n\s*def\s+(\w+)\s*\(\s*cls\s*,\s*([^)]+)\s*\):'
            
            def replace_validator(match):
                field_name = match.group(1)
                func_name = match.group(2)
                params = match.group(3)
                
                # Check if it's a pre-validator
                is_pre = 'pre=True' in match.group(0)
                mode = ', mode="before"' if is_pre else ''
                
                return f'@field_validator("{field_name}"{mode})\n    @classmethod\n    def {func_name}(cls, {params}):'
            
            content = re.sub(validator_pattern, replace_validator, content, flags=re.MULTILINE)
            
            # Fix multi-field validators
            multi_validator_pattern = r'@validator\(([^)]+)\s*(?:,\s*pre=True|,\s*pre=False)?\s*\)\s*\n\s*def\s+(\w+)\s*\(\s*cls\s*,\s*([^)]+)\s*\):'
            
            def replace_multi_validator(match):
                fields = match.group(1)
                func_name = match.group(2)
                params = match.group(3)
                
                is_pre = 'pre=True' in match.group(0)
                mode = ', mode="before"' if is_pre else ''
                
                return f'@field_validator({fields}{mode})\n    @classmethod\n    def {func_name}(cls, {params}):'
            
            content = re.sub(multi_validator_pattern, replace_multi_validator, content, flags=re.MULTILINE)
            
            # Fix root validators to model validators
            root_validator_pattern = r'@root_validator\s*(?:\([^)]*\))?\s*\n\s*def\s+(\w+)\s*\(\s*cls\s*,\s*([^)]+)\s*\):'
            
            def replace_root_validator(match):
                func_name = match.group(1)
                params = match.group(2)
                return f'@model_validator(mode="after")\n    @classmethod\n    def {func_name}(cls, {params}):'
            
            content = re.sub(root_validator_pattern, replace_root_validator, content, flags=re.MULTILINE)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log_fix(str(file_path), "VALIDATORS", "Migrated to V2 validators")
                return True
                
        except Exception as e:
            self.log_error(str(file_path), f"Validator fix failed: {e}")
        return False

    def fix_config_classes(self, file_path: Path) -> bool:
        """Convert Config classes to ConfigDict"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern to match Config classes
            config_pattern = r'(\s+)class Config:\s*\n((?:\1\s+[^\n]+\n)*)'
            
            def replace_config(match):
                indent = match.group(1)
                config_body = match.group(2)
                
                # Parse config options
                config_dict = {}
                for line in config_body.split('\n'):
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Map V1 to V2 config names
                        if key == 'orm_mode':
                            config_dict['from_attributes'] = value
                        elif key == 'allow_population_by_field_name':
                            config_dict['populate_by_name'] = value
                        elif key == 'schema_extra':
                            config_dict['json_schema_extra'] = value
                        elif key not in ['json_encoders']:  # Skip deprecated options
                            config_dict[key] = value
                
                # Build ConfigDict
                if config_dict:
                    config_items = [f"{k}={v}" for k, v in config_dict.items()]
                    return f"{indent}model_config = ConfigDict({', '.join(config_items)})"
                else:
                    return f"{indent}model_config = ConfigDict()"
            
            content = re.sub(config_pattern, replace_config, content, flags=re.MULTILINE)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log_fix(str(file_path), "CONFIG", "Converted Config to ConfigDict")
                return True
                
        except Exception as e:
            self.log_error(str(file_path), f"Config fix failed: {e}")
        return False

    def fix_field_examples(self, file_path: Path) -> bool:
        """Fix Field(example=...) to use json_schema_extra"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern to match Field with example
            field_pattern = r'Field\(([^)]*example\s*=\s*[^,)]+[^)]*)\)'
            
            def replace_field(match):
                field_args = match.group(1)
                
                # Extract example value
                example_match = re.search(r'example\s*=\s*([^,)]+)', field_args)
                if example_match:
                    example_value = example_match.group(1).strip()
                    # Remove example from original args
                    other_args = re.sub(r',?\s*example\s*=\s*[^,)]+', '', field_args).strip()
                    other_args = re.sub(r'^,\s*', '', other_args)  # Remove leading comma
                    other_args = re.sub(r',\s*$', '', other_args)  # Remove trailing comma
                    
                    # Build new Field call
                    if other_args:
                        return f'Field({other_args}, json_json_schema_extra={{"example": {example_value}}})'
                    else:
                        return f'Field(json_json_schema_extra={{"example": {example_value}}})'
                
                return match.group(0)
            
            content = re.sub(field_pattern, replace_field, content)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log_fix(str(file_path), "FIELD", "Fixed Field example usage")
                return True
                
        except Exception as e:
            self.log_error(str(file_path), f"Field fix failed: {e}")
        return False

    def fix_critical_validator_error(self, file_path: Path) -> bool:
        """Fix the critical 'field and config parameters not available' error"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Find validators using old V1 signature with field/config parameters
            old_validator_pattern = r'@validator\([^)]+\)\s*\n\s*def\s+(\w+)\s*\(\s*cls\s*,\s*v\s*,\s*field[^)]*\):'
            
            def fix_old_validator(match):
                func_name = match.group(1)
                # Replace with V2 compatible signature
                return f'@field_validator("{func_name.replace("validate_", "")}")\n    @classmethod\n    def {func_name}(cls, v):'
            
            content = re.sub(old_validator_pattern, fix_old_validator, content, flags=re.MULTILINE)
            
            # Also fix any remaining validators with complex signatures
            complex_validator_pattern = r'@validator\(([^)]+)\)\s*\n\s*def\s+(\w+)\s*\(\s*cls\s*,\s*v\s*,\s*[^)]*field[^)]*\):'
            
            def fix_complex_validator(match):
                field_spec = match.group(1)
                func_name = match.group(2)
                return f'@field_validator({field_spec})\n    @classmethod\n    def {func_name}(cls, v):'
            
            content = re.sub(complex_validator_pattern, fix_complex_validator, content, flags=re.MULTILINE)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log_fix(str(file_path), "CRITICAL", "Fixed field/config parameter error")
                return True
                
        except Exception as e:
            self.log_error(str(file_path), f"Critical fix failed: {e}")
        return False

    def process_file(self, file_path: Path) -> bool:
        """Process a single Python file"""
        if not file_path.suffix == '.py':
            return False
            
        print(f"🔧 Processing: {file_path}")
        
        fixes_applied = 0
        
        # Apply all fixes
        if self.fix_validator_imports(file_path):
            fixes_applied += 1
        if self.fix_critical_validator_error(file_path):
            fixes_applied += 1
        if self.fix_validators(file_path):
            fixes_applied += 1
        if self.fix_config_classes(file_path):
            fixes_applied += 1
        if self.fix_field_examples(file_path):
            fixes_applied += 1
            
        return fixes_applied > 0

    def migrate_all(self) -> Dict[str, int]:
        """Migrate all Python files in the backend"""
        stats = {
            'files_processed': 0,
            'files_modified': 0,
            'total_fixes': 0,
            'errors': 0
        }
        
        print("🚀 Starting comprehensive Pydantic V2 migration...")
        
        # Find all Python files
        python_files = list(self.backend_path.rglob("*.py"))
        
        for file_path in python_files:
            # Skip __pycache__ and other irrelevant directories
            if '__pycache__' in str(file_path) or 'venv' in str(file_path):
                continue
                
            stats['files_processed'] += 1
            
            if self.process_file(file_path):
                stats['files_modified'] += 1
        
        stats['total_fixes'] = len(self.fixes_applied)
        stats['errors'] = len(self.errors_found)
        
        return stats

    def generate_report(self, stats: Dict[str, int]):
        """Generate migration report"""
        print("\n" + "="*60)
        print("📊 PYDANTIC V2 MIGRATION REPORT")
        print("="*60)
        print(f"Files processed: {stats['files_processed']}")
        print(f"Files modified: {stats['files_modified']}")
        print(f"Total fixes applied: {stats['total_fixes']}")
        print(f"Errors encountered: {stats['errors']}")
        
        if self.fixes_applied:
            print("\n✅ FIXES APPLIED:")
            for fix in self.fixes_applied:
                print(f"  {fix}")
        
        if self.errors_found:
            print("\n❌ ERRORS FOUND:")
            for error in self.errors_found:
                print(f"  {error}")
        
        print("\n🎯 NEXT STEPS:")
        print("1. Run: pytest --tb=short -x")
        print("2. Check for any remaining validation errors")
        print("3. Update any custom validator logic if needed")
        print("="*60)

def main():
    """Main migration function"""
    migrator = PydanticV2Migrator()
    stats = migrator.migrate_all()
    migrator.generate_report(stats)
    
    if stats['errors'] == 0:
        print("🎉 Migration completed successfully!")
        return 0
    else:
        print("⚠️  Migration completed with some errors. Check the report above.")
        return 1

if __name__ == "__main__":
    exit(main())

