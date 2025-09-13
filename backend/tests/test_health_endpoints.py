"""Test health endpoints directly."""
import sys
import requests

# Add backend to Python path
sys.path.insert(0, '.')

def test_health_endpoints():
    """Test health endpoints."""
    base_url = "http://localhost:8000"
    
    # Test health check
    print("\nTesting GET /health/")
    response = requests.get(f"{base_url}/health/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test health metrics
    print("\nTesting GET /health/metrics")
    response = requests.get(f"{base_url}/health/metrics")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_health_endpoints()

