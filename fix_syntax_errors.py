#!/usr/bin/env python3
"""
Fix syntax errors from malformed Pydantic V2 migration
"""
import os
import re
from pathlib import Path

def fix_syntax_errors(backend_path: str = "backend"):
    """Fix all syntax errors from malformed ConfigDict migrations"""
    backend_path = Path(backend_path)
    fixed_files = []
    
    # Find all Python files
    python_files = list(backend_path.rglob("*.py"))
    
    for file_path in python_files:
        if '__pycache__' in str(file_path) or 'venv' in str(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix pattern: model_config = ConfigDict()        some_attr = value
            pattern1 = r'model_config = ConfigDict\(\)\s+(\w+)\s*=\s*([^\n]+)'
            
            def fix_pattern1(match):
                attr_name = match.group(1)
                attr_value = match.group(2)
                
                # Map old attributes to new ConfigDict format
                if attr_name == 'orm_mode' and 'True' in attr_value:
                    return 'model_config = ConfigDict(from_attributes=True)'
                elif attr_name == 'from_attributes' and 'True' in attr_value:
                    return 'model_config = ConfigDict(from_attributes=True)'
                elif attr_name == 'allow_population_by_field_name' and 'True' in attr_value:
                    return 'model_config = ConfigDict(populate_by_name=True)'
                elif attr_name == 'schema_extra':
                    return f'model_config = ConfigDict(json_json_schema_extra={attr_value})'
                else:
                    # Generic case - put it inside ConfigDict
                    return f'model_config = ConfigDict({attr_name}={attr_value})'
            
            content = re.sub(pattern1, fix_pattern1, content)
            
            # Fix multi-line broken configs
            pattern2 = r'model_config = ConfigDict\(\)\s+json_encoders\s*=\s*\{([^}]+)\}'
            content = re.sub(pattern2, r'model_config = ConfigDict()', content)
            
            # Fix orphaned config attributes after ConfigDict
            pattern3 = r'(model_config = ConfigDict\([^)]*\))\s+(\w+)\s*=\s*([^\n]+)'
            
            def fix_pattern3(match):
                config_dict = match.group(1)
                attr_name = match.group(2)
                attr_value = match.group(3)
                
                # Remove the orphaned attribute line
                return config_dict
            
            content = re.sub(pattern3, fix_pattern3, content)
            
            # Clean up any remaining orphaned lines
            lines = content.split('\n')
            cleaned_lines = []
            skip_next = False
            
            for i, line in enumerate(lines):
                if skip_next:
                    skip_next = False
                    continue
                    
                # Skip orphaned config attributes
                if re.match(r'\s+(orm_mode|from_attributes|allow_population_by_field_name|schema_extra|json_encoders)\s*=', line):
                    continue
                    
                cleaned_lines.append(line)
            
            content = '\n'.join(cleaned_lines)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(str(file_path))
                print(f"✅ Fixed: {file_path}")
                
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
    
    return fixed_files

def main():
    """Main function"""
    print("🔧 Fixing syntax errors from Pydantic migration...")
    fixed_files = fix_syntax_errors()
    
    print(f"\n📊 Summary:")
    print(f"Fixed {len(fixed_files)} files")
    
    if fixed_files:
        print("\n✅ Fixed files:")
        for file in fixed_files:
            print(f"  - {file}")
    
    print("\n🎯 Testing syntax...")
    return 0

if __name__ == "__main__":
    exit(main())

