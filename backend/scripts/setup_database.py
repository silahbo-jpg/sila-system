"""
Database setup script for SILA System.

This script runs all database migrations and sets up initial data.
"""
import asyncio
import importlib.util
import logging
import sys
from pathlib import Path
from typing import List, Tuple, Any, Callable, Awaitable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the migrations directory
SCRIPT_DIR = Path(__file__).parent.absolute()
MIGRATIONS_DIR = SCRIPT_DIR / "migrations"

Migration = Tuple[str, Any]  # (name, module)

class MigrationError(Exception):
    """Custom exception for migration errors."""
    pass

def import_migration(module_path: Path) -> Any:
    """Import a migration module from a file path."""
    try:
        # Generate a module name from the file path
        module_name = f"scripts.migrations.{module_path.stem}"
        
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load spec for {module_path}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # Check if the module has the required functions
        if not hasattr(module, 'apply'):
            raise AttributeError(f"Migration {module_name} is missing required 'apply' function")
            
        return module
    except Exception as e:
        raise MigrationError(f"Failed to import migration {module_path}: {e}")

def get_migrations() -> List[Tuple[str, Any]]:
    """Get all migration modules in the migrations directory."""
    migrations = []
    
    # Ensure migrations directory exists
    if not MIGRATIONS_DIR.exists():
        logger.warning(f"Migrations directory not found: {MIGRATIONS_DIR}")
        return migrations
    
    # Find all Python files in the migrations directory
    migration_files = sorted(MIGRATIONS_DIR.glob("*.py"))
    
    for file in migration_files:
        if file.name == "__init__.py":
            continue
            
        try:
            module = import_migration(file)
            migrations.append((file.stem, module))
            logger.debug(f"Loaded migration: {file.stem}")
        except Exception as e:
            logger.error(f"❌ Failed to load migration {file.stem}: {e}")
            raise
    
    return migrations

async def run_migrations():
    """Run all database migrations."""
    logger.info("Starting database migrations...")
    
    migrations = get_migrations()
    if not migrations:
        logger.warning("No migrations found!")
        return
    
    # Sort migrations by name to ensure correct order
    migrations.sort(key=lambda x: x[0])
    
    for name, module in migrations:
        try:
            logger.info(f"🚀 Running migration: {name}")
            await module.apply()
            logger.info(f"✅ {name} completed successfully")
        except Exception as e:
            logger.error(f"❌ {name} failed: {str(e)}")
            raise MigrationError(f"Migration {name} failed: {e}")
    
    logger.info("✅ All migrations completed successfully")

async def main():
    """Main function to run database setup."""
    print("\n=== SILA System Database Setup ===\n")
    
    try:
        # Add the scripts directory to the Python path
        if str(SCRIPT_DIR) not in sys.path:
            sys.path.append(str(SCRIPT_DIR))
        
        # Run migrations
        await run_migrations()
        
        # Prompt to create postgres postgres
        print("\n=== postgres postgres Setup ===\n")
        create_admin = input("Would you like to create an postgres postgres now? (y/n): ").lower()
        
        if create_admin == 'y':
            # Import and run create_admin script
            from scripts.create_admin import main as create_admin_main
            await create_admin_main()
        else:
            print("\nYou can create an postgres postgres later by running: python -m scripts.create_admin")
        
        print("\n✅ Database setup completed successfully!")
        return 0
        
    except MigrationError as e:
        logger.error(f"❌ Database migration failed: {e}")
        return 1
    except Exception as e:
        logger.error(f"❌ An unexpected error occurred: {e}", exc_info=True)
        return 1
    finally:
        # Ensure any cleanup happens here
        pass

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

