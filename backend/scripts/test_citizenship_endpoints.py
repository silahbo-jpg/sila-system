#!/usr/bin/env python3
"""
Comprehensive Automated Test Script for Citizenship Endpoints
============================================================

This script tests all citizenship module endpoints with proper error handling,
authentication, and detailed reporting.

Usage:
    python scripts/test_citizenship_endpoints.py
    python scripts/test_citizenship_endpoints.py --verbose
    python scripts/test_citizenship_endpoints.py --endpoint citizens
"""

import requests
import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1/citizenship"
TIMEOUT = 10

@dataclass
class TestResult:
    """Test result data structure"""
    endpoint: str
    method: str
    status_code: int
    success: bool
    response_time: float
    error_message: Optional[str] = None
    response_data: Optional[Dict] = None

class CitizenshipEndpointTester:
    """Comprehensive tester for citizenship endpoints"""
    
    def __init__(self, base_url: str = BASE_URL, verbose: bool = False):
        self.base_url = base_url
        self.api_url = f"{base_url}{API_PREFIX}"
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'SILA-Citizenship-Tester/1.0'
        })
        self.results: List[TestResult] = []
        self.auth_token: Optional[str] = None
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if self.verbose or level in ["ERROR", "SUCCESS"]:
            print(f"[{timestamp}] {level}: {message}")
    
    def check_server_health(self) -> bool:
        """Check if the server is running and accessible"""
        try:
            response = self.session.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                self.log("✅ Server is running and accessible", "SUCCESS")
                return True
            else:
                self.log(f"❌ Server responded with status {response.status_code}", "ERROR")
                return False
        except requests.exceptions.ConnectionError:
            self.log("❌ Server is not running or not accessible", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Error checking server health: {e}", "ERROR")
            return False
    
    def authenticate(self) -> bool:
        """Attempt to authenticate and get access token"""
        # Try to get a test token or use mock authentication
        # For testing purposes, we'll skip authentication for now
        # In production, implement proper authentication flow
        self.log("⚠️ Skipping authentication for testing", "INFO")
        return True
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    params: Optional[Dict] = None) -> TestResult:
        """Make HTTP request and return test result"""
        url = f"{self.api_url}{endpoint}"
        start_time = time.time()
        
        try:
            self.log(f"Testing {method} {endpoint}", "INFO")
            
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=TIMEOUT)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=TIMEOUT)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, timeout=TIMEOUT)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=TIMEOUT)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Determine success based on status code
            success = response.status_code < 400
            
            # Parse response data
            try:
                response_data = response.json() if response.content else None
            except json.JSONDecodeError:
                response_data = {"raw_response": response.text}
            
            result = TestResult(
                endpoint=endpoint,
                method=method.upper(),
                status_code=response.status_code,
                success=success,
                response_time=response_time,
                response_data=response_data
            )
            
            if success:
                self.log(f"✅ {method} {endpoint} - {response.status_code} ({response_time:.1f}ms)", "SUCCESS")
            else:
                error_msg = f"HTTP {response.status_code}"
                if response_data and isinstance(response_data, dict):
                    error_msg += f" - {response_data.get('detail', 'Unknown error')}"
                result.error_message = error_msg
                self.log(f"❌ {method} {endpoint} - {error_msg}", "ERROR")
            
            return result
            
        except requests.exceptions.Timeout:
            result = TestResult(
                endpoint=endpoint,
                method=method.upper(),
                status_code=0,
                success=False,
                response_time=(time.time() - start_time) * 1000,
                error_message="Request timeout"
            )
            self.log(f"❌ {method} {endpoint} - Timeout after {TIMEOUT}s", "ERROR")
            return result
            
        except Exception as e:
            result = TestResult(
                endpoint=endpoint,
                method=method.upper(),
                status_code=0,
                success=False,
                response_time=(time.time() - start_time) * 1000,
                error_message=str(e)
            )
            self.log(f"❌ {method} {endpoint} - {str(e)}", "ERROR")
            return result
    
    def test_get_all_citizens(self):
        """Test GET /citizens/ endpoint"""
        result = self.make_request("GET", "/citizens/")
        self.results.append(result)
        return result
    
    def test_get_citizen_by_id(self, citizen_id: int = 1):
        """Test GET /citizens/{id} endpoint"""
        result = self.make_request("GET", f"/citizens/{citizen_id}")
        self.results.append(result)
        return result
    
    def test_create_citizen(self):
        """Test POST /citizens/ endpoint"""
        test_data = {
            "first_name": "Test",
            "last_name": "Citizen",
            "bi_number": "123456789LA041",
            "birth_date": "1990-01-01",
            "birth_place": "Huambo",
            "nationality": "Angolana",
            "marital_status": "SOLTEIRO",
            "phone": "+244923456789",
            "email": "test.citizen@example.com",
            "address": {
                "province": "Huambo",
                "municipality": "Huambo",
                "commune": "Huambo",
                "neighborhood": "Centro",
                "street": "Rua Principal",
                "house_number": "123"
            }
        }
        
        result = self.make_request("POST", "/citizens/", data=test_data)
        self.results.append(result)
        return result
    
    def test_update_citizen(self, citizen_id: int = 1):
        """Test PUT /citizens/{id} endpoint"""
        update_data = {
            "phone": "+244987654321",
            "email": "updated.citizen@example.com"
        }
        
        result = self.make_request("PUT", f"/citizens/{citizen_id}", data=update_data)
        self.results.append(result)
        return result
    
    def test_delete_citizen(self, citizen_id: int = 999):
        """Test DELETE /citizens/{id} endpoint"""
        result = self.make_request("DELETE", f"/citizens/{citizen_id}")
        self.results.append(result)
        return result
    
    def test_search_citizens(self):
        """Test GET /citizens/ with search parameters"""
        params = {
            "query": "Test",
            "municipality": "Huambo",
            "status": "ACTIVE",
            "limit": 10
        }
        
        result = self.make_request("GET", "/citizens/", params=params)
        self.results.append(result)
        return result
    
    def test_upload_document(self, citizen_id: int = 1):
        """Test POST /citizens/{id}/documents/ endpoint"""
        # Note: This is a simplified test as file upload requires multipart/form-data
        result = self.make_request("GET", f"/citizens/{citizen_id}/documents/")
        self.results.append(result)
        return result
    
    def test_feedback_endpoints(self):
        """Test feedback-related endpoints"""
        # Test create feedback
        feedback_data = {
            "tipo": "SUGESTAO",
            "titulo": "Test Feedback",
            "descricao": "This is a test feedback for the citizenship module",
            "classificacao": 5
        }
        
        result = self.make_request("POST", "/feedback/", data=feedback_data)
        self.results.append(result)
        
        # Test list feedbacks
        result = self.make_request("GET", "/feedback/")
        self.results.append(result)
        
        return result
    
    def run_all_tests(self, specific_endpoint: Optional[str] = None):
        """Run all tests or specific endpoint tests"""
        self.log("🚀 Starting Citizenship Endpoints Testing", "INFO")
        self.log("=" * 60, "INFO")
        
        # Check server health first
        if not self.check_server_health():
            self.log("❌ Cannot proceed - server is not accessible", "ERROR")
            return False
        
        # Authenticate if needed
        if not self.authenticate():
            self.log("⚠️ Authentication failed, proceeding without auth", "INFO")
        
        # Define test functions
        tests = {
            "citizens": [
                ("GET All Citizens", self.test_get_all_citizens),
                ("GET Citizen by ID", self.test_get_citizen_by_id),
                ("POST Create Citizen", self.test_create_citizen),
                ("PUT Update Citizen", self.test_update_citizen),
                ("DELETE Citizen", self.test_delete_citizen),
                ("GET Search Citizens", self.test_search_citizens),
                ("GET Documents", self.test_upload_document),
            ],
            "feedback": [
                ("Feedback Endpoints", self.test_feedback_endpoints),
            ]
        }
        
        # Run specific endpoint tests or all tests
        if specific_endpoint and specific_endpoint in tests:
            test_group = {specific_endpoint: tests[specific_endpoint]}
        else:
            test_group = tests
        
        # Execute tests
        for group_name, group_tests in test_group.items():
            self.log(f"\n📋 Testing {group_name.upper()} endpoints:", "INFO")
            for test_name, test_func in group_tests:
                try:
                    self.log(f"  ▶️ {test_name}", "INFO")
                    test_func()
                    time.sleep(0.1)  # Small delay between requests
                except Exception as e:
                    self.log(f"  ❌ {test_name} failed: {e}", "ERROR")
        
        return True
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        failed_tests = total_tests - successful_tests
        
        avg_response_time = sum(r.response_time for r in self.results) / total_tests if total_tests > 0 else 0
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "successful": successful_tests,
                "failed": failed_tests,
                "success_rate": (successful_tests / total_tests * 100) if total_tests > 0 else 0,
                "average_response_time_ms": round(avg_response_time, 2)
            },
            "results": [
                {
                    "endpoint": r.endpoint,
                    "method": r.method,
                    "status_code": r.status_code,
                    "success": r.success,
                    "response_time_ms": round(r.response_time, 2),
                    "error_message": r.error_message
                }
                for r in self.results
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        return report
    
    def print_summary(self):
        """Print test summary to console"""
        report = self.generate_report()
        summary = report["summary"]
        
        self.log("\n" + "=" * 60, "INFO")
        self.log("📊 TEST SUMMARY", "SUCCESS")
        self.log("=" * 60, "INFO")
        self.log(f"📈 Total Tests: {summary['total_tests']}", "INFO")
        self.log(f"✅ Successful: {summary['successful']}", "SUCCESS")
        self.log(f"❌ Failed: {summary['failed']}", "ERROR" if summary['failed'] > 0 else "INFO")
        self.log(f"📊 Success Rate: {summary['success_rate']:.1f}%", "SUCCESS" if summary['success_rate'] > 80 else "ERROR")
        self.log(f"⏱️ Avg Response Time: {summary['average_response_time_ms']:.1f}ms", "INFO")
        
        if summary['failed'] > 0:
            self.log("\n❌ FAILED TESTS:", "ERROR")
            for result in self.results:
                if not result.success:
                    self.log(f"  • {result.method} {result.endpoint} - {result.error_message}", "ERROR")
        
        self.log("=" * 60, "INFO")
    
    def save_report(self, filename: Optional[str] = None):
        """Save detailed report to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"citizenship_test_report_{timestamp}.json"
        
        report = self.generate_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            self.log(f"💾 Report saved to: {filename}", "SUCCESS")
        except Exception as e:
            self.log(f"❌ Failed to save report: {e}", "ERROR")

def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(description="Test Citizenship Endpoints")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--endpoint", "-e", help="Test specific endpoint group (citizens, feedback)")
    parser.add_argument("--base-url", default=BASE_URL, help="Base URL for the API")
    parser.add_argument("--save-report", "-s", action="store_true", help="Save detailed report to file")
    
    args = parser.parse_args()
    
    # Create tester instance
    tester = CitizenshipEndpointTester(base_url=args.base_url, verbose=args.verbose)
    
    # Run tests
    success = tester.run_all_tests(specific_endpoint=args.endpoint)
    
    if success:
        # Print summary
        tester.print_summary()
        
        # Save report if requested
        if args.save_report:
            tester.save_report()
        
        # Exit with appropriate code
        report = tester.generate_report()
        exit_code = 0 if report["summary"]["failed"] == 0 else 1
        sys.exit(exit_code)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()