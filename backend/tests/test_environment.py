"""
Basic test to verify the test environment is working correctly.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_environment_setup(client: TestClient, db_session: Session):
    """Verify that the test environment is set up correctly."""
    logger.info("Running environment setup test...")
    
    # Test database connection
    try:
        result = db_session.execute("SELECT 1")
        assert result.scalar() == 1
        logger.info("✓ Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
    
    # Test FastAPI application
    response = client.get("/api/health")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    logger.info("✓ FastAPI application is running")
    
    logger.info("✓ Environment setup test completed successfully")

def test_skip_example():
    """Example of a skipped test."""
    pytest.skip("This is an example of a skipped test")

@pytest.mark.xfail
def test_expected_failure():
    """Example of an expected test failure."""
    assert False, "This test is expected to fail"
