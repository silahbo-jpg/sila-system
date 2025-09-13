#!/usr/bin/env python3
"""
Environment Validation Script
Validates .env files for security and completeness.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class EnvValidator:
    """Validates environment files."""
    
    REQUIRED_VARS = [
        'DATABASE_URL',
        'SECRET_KEY',
        'ALGORITHM',
        'ACCESS_TOKEN_EXPIRE_MINUTES'
    ]
    
    SENSITIVE_PATTERNS = [
        (r'password.*=.*123|admin|test', 'Weak password detected'),
        (r'secret.*=.*secret|test|123', 'Weak secret key detected'),
        (r'key.*=.*test|123|abc', 'Weak API key detected'),
    ]
    
    def __init__(self, env_path: Path):
        self.env_path = env_path
        self.issues = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Run all validations."""
        if not self.env_path.exists():
            self.issues.append(f"Environment file not found: {self.env_path}")
            return False
        
        env_vars = self.load_env_vars()
        
        self.check_required_vars(env_vars)
        self.check_sensitive_patterns(env_vars)
        self.check_database_url(env_vars)
        self.check_secret_strength(env_vars)
        
        return len(self.issues) == 0
    
    def load_env_vars(self) -> Dict[str, str]:
        """Load environment variables from file."""
        env_vars = {}
        
        try:
            with open(self.env_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            env_vars[key.strip()] = value.strip().strip('"\'')
                        else:
                            self.warnings.append(f"Line {line_num}: Invalid format")
        except Exception as e:
            self.issues.append(f"Failed to read env file: {e}")
        
        return env_vars
    
    def check_required_vars(self, env_vars: Dict[str, str]):
        """Check for required environment variables."""
        for var in self.REQUIRED_VARS:
            if var not in env_vars:
                self.issues.append(f"Missing required variable: {var}")
            elif not env_vars[var]:
                self.issues.append(f"Empty required variable: {var}")
    
    def check_sensitive_patterns(self, env_vars: Dict[str, str]):
        """Check for sensitive patterns in environment variables."""
        for key, value in env_vars.items():
            for pattern, message in self.SENSITIVE_PATTERNS:
                if re.search(pattern, f"{key}={value}", re.IGNORECASE):
                    self.issues.append(f"{key}: {message}")
    
    def check_database_url(self, env_vars: Dict[str, str]):
        """Validate database URL format."""
        if 'DATABASE_URL' in env_vars:
            db_url = env_vars['DATABASE_URL']
            if not db_url.startswith(('postgresql://', 'postgresql+psycopg2://')):
                self.issues.append("DATABASE_URL should use PostgreSQL")
            
            if 'localhost' in db_url and 'password' in db_url:
                if 'password@' in db_url or 'password:' in db_url:
                    self.warnings.append("DATABASE_URL contains 'password' - verify this is intentional")
    
    def check_secret_strength(self, env_vars: Dict[str, str]):
        """Check secret key strength."""
        if 'SECRET_KEY' in env_vars:
            secret = env_vars['SECRET_KEY']
            if len(secret) < 32:
                self.issues.append("SECRET_KEY should be at least 32 characters long")
            
            if secret.isalnum() and secret.islower():
                self.warnings.append("SECRET_KEY should contain mixed case and special characters")
    
    def print_results(self):
        """Print validation results."""
        if self.issues:
            print("❌ Environment Validation Issues:")
            for issue in self.issues:
                print(f"  • {issue}")
        
        if self.warnings:
            print("\n⚠️ Environment Validation Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.issues and not self.warnings:
            print("✅ Environment validation passed")

def main():
    """Main validation function."""
    print("🔍 Environment File Validation")
    print("=" * 40)
    
    root_dir = Path(__file__).parent.parent.parent
    env_files = [
        root_dir / ".env",
        root_dir / "backend" / ".env",
        root_dir / "frontend" / ".env"
    ]
    
    all_valid = True
    
    for env_file in env_files:
        if env_file.exists():
            print(f"\n📄 Validating: {env_file}")
            validator = EnvValidator(env_file)
            is_valid = validator.validate()
            validator.print_results()
            
            if not is_valid:
                all_valid = False
        else:
            print(f"\nℹ️ Skipping non-existent: {env_file}")
    
    if all_valid:
        print("\n🎉 All environment files are valid!")
        return True
    else:
        print("\n❌ Environment validation failed!")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)