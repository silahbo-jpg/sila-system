"""
Smoke test to verify the test environment is working.
"""
import sys
import os
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def test_smoke():
    """Basic smoke test to verify the test environment."""
    logger.info("Running smoke test...")
    assert 1 + 1 == 2
    logger.info("✓ Smoke test passed")

if __name__ == "__main__":
    logger.info("Running smoke test directly...")
    test_smoke()
    logger.info("All tests completed")
