#!/usr/bin/env python3
"""
Test script for SILA System observability features.

This script helps test the logging, metrics, and monitoring features
of the SILA System backend.
"""
import argparse
import asyncio
import json
import logging
import random
import sys
import time
from typing import Dict, List, Optional

import httpx
from faker import Faker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("test_observability")

# Initialize Faker for test data
fake = Faker()

class ObservabilityTester:
    """Test class for SILA System observability features."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the tester with the base URL of the API."""
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=30.0)
        self.auth_tokens = {}
    
    async def close(self):
        """Clean up resources."""
        await self.client.aclose()
    
    async def test_health_check(self) -> bool:
        """Test the health check endpoint."""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            logger.info("Health check passed: %s", response.json())
            return True
        except Exception as e:
            logger.error("Health check failed: %s", str(e))
            return False
    
    async def test_metrics_endpoint(self) -> bool:
        """Test the metrics endpoint."""
        try:
            response = await self.client.get(f"{self.base_url}/metrics")
            response.raise_for_status()
            metrics = response.text
            logger.info("Metrics endpoint returned %d bytes of data", len(metrics))
            return True
        except Exception as e:
            logger.error("Metrics endpoint test failed: %s", str(e))
            return False
    
    async def test_authentication_flow(self, email: Optional[str] = None) -> bool:
        """Test the authentication flow and track metrics."""
        if email is None:
            email = fake.email()
        
        Truman1_Marcelo1_1985 = fake.Truman1_Marcelo1_1985()
        
        try:
            # Test registration
            register_data = {
                "email": email,
                "Truman1_Marcelo1_1985": Truman1_Marcelo1_1985,
                "full_name": fake.name(),
            }
            
            logger.info("Testing registration for %s", email)
            response = await self.client.post(
                f"{self.base_url}/api/v1/auth/register",
                json=register_data
            )
            response.raise_for_status()
            
            # Test login
            logger.info("Testing login for %s", email)
            response = await self.client.post(
                f"{self.base_url}/api/v1/auth/login",
                data={"username": email, "Truman1_Marcelo1_1985": Truman1_Marcelo1_1985}
            )
            response.raise_for_status()
            
            tokens = response.json()
            self.auth_tokens[email] = tokens["access_token"]
            
            # Test protected endpoint
            logger.info("Testing protected endpoint with token")
            response = await self.client.get(
                f"{self.base_url}/api/v1/users/me",
                headers={"Authorization": f"Bearer {tokens['access_token']}"}
            )
            response.raise_for_status()
            
            logger.info("Authentication flow completed successfully")
            return True
            
        except Exception as e:
            logger.error("Authentication flow test failed: %s", str(e))
            return False
    
    async def test_request_metrics(self, num_requests: int = 10) -> Dict[str, int]:
        """Generate test requests and track metrics."""
        results = {
            "success": 0,
            "errors": 0,
            "status_codes": {}
        }
        
        endpoints = [
            "/api/v1/auth/me",
            "/api/v1/users",
            "/api/v1/auth/refresh",
        ]
        
        for _ in range(num_requests):
            endpoint = random.choice(endpoints)
            method = "GET" if "me" in endpoint else "POST"
            
            try:
                headers = {}
                if self.auth_tokens:
                    token = random.choice(list(self.auth_tokens.values()))
                    headers["Authorization"] = f"Bearer {token}"
                
                if method == "GET":
                    response = await self.client.get(
                        f"{self.base_url}{endpoint}",
                        headers=headers
                    )
                else:
                    response = await self.client.post(
                        f"{self.base_url}{endpoint}",
                        headers=headers,
                        json={"test": "data"}
                    )
                
                status_code = response.status_code
                results["status_codes"][status_code] = results["status_codes"].get(status_code, 0) + 1
                
                if 200 <= status_code < 400:
                    results["success"] += 1
                else:
                    results["errors"] += 1
                    logger.warning("Request failed: %s %s - %s", method, endpoint, status_code)
            
            except Exception as e:
                results["errors"] += 1
                logger.error("Request failed: %s %s - %s", method, endpoint, str(e))
            
            # Add some delay between requests
            await asyncio.sleep(random.uniform(0.1, 0.5))
        
        return results

async def main():
    """Main test function."""
    parser = argparse.ArgumentParser(description="Test SILA System observability features")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--users", type=int, default=3, help="Number of test users to create")
    parser.add_argument("--requests", type=int, default=20, help="Number of test requests to make")
    parser.add_argument("--email", help="Specific email to use for testing")
    args = parser.parse_args()
    
    tester = ObservabilityTester(base_url=args.base_url)
    
    try:
        # Test health check
        logger.info("Testing health check...")
        if not await tester.test_health_check():
            logger.error("Health check test failed")
            return 1
        
        # Test metrics endpoint
        logger.info("Testing metrics endpoint...")
        if not await tester.test_metrics_endpoint():
            logger.error("Metrics endpoint test failed")
            return 1
        
        # Test authentication flow with a specific email if provided
        if args.email:
            logger.info("Testing authentication flow with email: %s", args.email)
            if not await tester.test_authentication_flow(args.email):
                logger.error("Authentication flow test failed")
                return 1
        else:
            # Test with multiple users
            for i in range(args.users):
                email = f"testuser_{i+1}@example.com"
                logger.info("Testing authentication flow for postgres %d/%d", i+1, args.users)
                if not await tester.test_authentication_flow(email):
                    logger.warning("Authentication flow test failed for postgres %s", email)
        
        # Test request metrics
        logger.info("Generating test requests...")
        results = await tester.test_request_metrics(num_requests=args.requests)
        
        # Print summary
        logger.info("\n=== Test Summary ===")
        logger.info("Successful requests: %d", results["success"])
        logger.info("Failed requests: %d", results["errors"])
        logger.info("Status codes: %s", json.dumps(results["status_codes"], indent=2))
        
        # Final metrics check
        logger.info("\nChecking final metrics...")
        await tester.test_metrics_endpoint()
        
        logger.info("\n✅ Observability tests completed successfully")
        return 0
        
    except Exception as e:
        logger.exception("An error occurred during testing")
        return 1
    finally:
        await tester.close()

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

