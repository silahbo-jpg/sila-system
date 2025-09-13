#!/usr/bin/env python3
"""
Test script to verify API endpoints are working after routing fixes.
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_endpoint(method, path, data=None, headers=None):
    """Test an endpoint and return the response."""
    url = f"{BASE_URL}{path}"
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        print(f"{method} {path}: {response.status_code}")
        if response.status_code != 404:
            print(f"  Response: {response.text[:100]}...")
        return response
    except Exception as e:
        print(f"{method} {path}: ERROR - {e}")
        return None

def main():
    """Test the main endpoints that were previously returning 404."""
    
    print("Testing API endpoints after routing fixes...")
    print("=" * 50)
    
    # Test health endpoint (should work)
    test_endpoint("GET", "/api/v1/health")
    
    # Test auth endpoints (should be accessible but may require auth)
    test_endpoint("POST", "/api/v1/auth/login", data={
        "email": "admin@sila.gov.ao", 
        "password": "Truman1_Marcelo1_1985"
    })
    
    # Test the old path that was failing
    test_endpoint("POST", "/api/auth/login", data={
        "email": "admin@sila.gov.ao", 
        "password": "Truman1_Marcelo1_1985"
    })
    
    # Test dashboard v2 endpoints
    test_endpoint("GET", "/v2/dashboard/resumo")
    test_endpoint("GET", "/v2/dashboard/municipios")
    
    print("=" * 50)
    print("Test completed. Check the status codes:")
    print("- 200/401/422: Route exists and is working")
    print("- 404: Route not found (still needs fixing)")

if __name__ == "__main__":
    main()