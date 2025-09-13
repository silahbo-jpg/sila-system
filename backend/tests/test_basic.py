"""
Basic test file to verify the test environment and database setup.
"""
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import required modules
try:
    import pytest
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.db.session import Base, SQLALCHEMY_DATABASE_URL
    from app.main import app
    
    logger.info("Successfully imported all required modules")
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    raise

def test_database_connection():
    """Test database connection and table creation."""
    logger.info("Testing database connection...")
    
    try:
        # Create a new engine and session for testing
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully created all database tables")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            assert result.scalar() == 1
            logger.info("✓ Database connection successful")
            
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        raise
    finally:
        # Clean up
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
        logger.info("Cleaned up test database")

def test_fastapi_app():
    """Test FastAPI application setup."""
    logger.info("Testing FastAPI application...")
    
    try:
        with TestClient(app) as client:
            # Test a basic endpoint
            response = client.get("/api/health")
            assert response.status_code == 200
            logger.info(f"✓ Health check successful: {response.json()}")
            
    except Exception as e:
        logger.error(f"FastAPI test failed: {e}")
        raise

if __name__ == "__main__":
    # Run tests directly for debugging
    logger.info("Running tests directly...")
    test_database_connection()
    test_fastapi_app()
    logger.info("All tests completed successfully")
