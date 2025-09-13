#!/usr/bin/env python3
"""
Development Environment Setup Script
Sets up the complete development environment for SILA-System.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd: str, cwd: Path = None) -> bool:
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {cmd}: {e.stderr}")
        return False

def setup_python_environment():
    """Set up Python virtual environment and dependencies."""
    print("🐍 Setting up Python environment...")
    
    backend_dir = Path(__file__).parent.parent / "backend"
    
    if not run_command("python -m venv venv", backend_dir):
        return False
    
    # Activate venv and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    commands = [
        f"{activate_cmd} && pip install --upgrade pip",
        f"{activate_cmd} && pip install -r requirements.txt",
        f"{activate_cmd} && pip install -r requirements-dev.txt"
    ]
    
    for cmd in commands:
        if not run_command(cmd, backend_dir):
            return False
    
    return True

def setup_database():
    """Set up PostgreSQL database."""
    print("🗄️ Setting up database...")
    
    from scripts.db.setup_database import main as setup_db
    return setup_db()

def setup_frontend():
    """Set up frontend dependencies."""
    print("🌐 Setting up frontend...")
    
    frontend_dir = Path(__file__).parent.parent / "frontend"
    
    commands = [
        "npm install",
        "npm run build"
    ]
    
    for cmd in commands:
        if not run_command(cmd, frontend_dir):
            return False
    
    return True

def create_env_files():
    """Create necessary .env files from examples."""
    print("📄 Creating environment files...")
    
    root_dir = Path(__file__).parent.parent
    env_example = root_dir / ".env.example"
    env_file = root_dir / ".env"
    
    if env_example.exists() and not env_file.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print(f"✅ Created {env_file}")
    
    return True

def main():
    """Main setup function."""
    print("🚀 SILA-System Development Environment Setup")
    print("=" * 50)
    
    steps = [
        ("Python Environment", setup_python_environment),
        ("Environment Files", create_env_files),
        ("Database", setup_database),
        ("Frontend", setup_frontend)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Failed to set up {step_name}")
            sys.exit(1)
    
    print("\n🎉 Development environment setup complete!")
    print("\nNext steps:")
    print("1. Configure your .env file with proper database credentials")
    print("2. Run: python scripts/main.py create-superuser")
    print("3. Run: python scripts/main.py run-tests")

if __name__ == "__main__":
    main()