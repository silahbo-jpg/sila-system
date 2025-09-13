"""
Test database connection and basic operations.
"""
import asyncio
import logging
import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create logs directory if it doesn't exist
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'test_db_connection.log'

# Configure logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),  # Write to file
        logging.StreamHandler(sys.stdout)  # Also log to console
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Logging to {log_file.absolute()}")

async def test_database_connection():
    """Test database connection and basic operations."""
    from app.db.session import get_engine, Base
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import AsyncSession
    
    logger.info("Testing database connection...")
    
    # Get the database engine
    engine = get_engine()
    
    try:
        # Test the connection
        async with AsyncSession(engine) as session:
            # Execute a simple query
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1, f"Expected 1, got {value}"
            logger.info("✓ Database connection successful")
            
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
    finally:
        # Clean up
        await engine.dispose()

async def test_create_tables():
    """Test creating and dropping tables."""
    from app.db.session import get_engine, Base
    from sqlalchemy.ext.asyncio import AsyncEngine
    
    logger.info("Testing table creation...")
    
    # Get the database engine
    engine = get_engine()
    
    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✓ Tables created successfully")
        
        # Verify tables exist
        async with AsyncEngine(engine).connect() as conn:
            result = await conn.execute(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                """
            )
            tables = [row[0] for row in result]
            logger.info(f"Found tables: {', '.join(tables)}")
            assert len(tables) > 0, "No tables found in the database"
        
    except Exception as e:
        logger.error(f"Table creation failed: {e}")
        raise
    finally:
        # Clean up
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()
        logger.info("✓ Cleaned up test database")

async def run_all_tests():
    """Run all database tests."""
    logger.info("=" * 80)
    logger.info("STARTING DATABASE TESTS")
    logger.info("=" * 80)
    
    try:
        logger.info("\n[1/2] Testing database connection...")
        await test_database_connection()
        logger.info("✓ Database connection test passed\n")
        
        logger.info("[2/2] Testing table creation...")
        await test_create_tables()
        logger.info("✓ Table creation test passed\n")
        
        logger.info("=" * 80)
        logger.info("ALL DATABASE TESTS COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"\nERROR: Database tests failed: {e}")
        logger.exception("Test failed with exception:")
        logger.info("=" * 80)
        logger.info("DATABASE TESTS FAILED")
        logger.info("=" * 80)
        raise

if __name__ == "__main__":
    asyncio.run(run_all_tests())
