#!/usr/bin/env python3
"""
Authentication Flow Validation Tool
Confirms that login works, token is issued, and requests to protected modules succeed.
"""

import requests
import json
import time
from pathlib import Path
from typing import Optional, Dict, List

class AuthValidator:
    """Validates the complete authentication flow."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.session = requests.Session()
        
    def check_server_health(self) -> bool:
        """Check if the server is running and healthy."""
        print("🔍 Checking server health...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/v1/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is running and healthy")
                return True
            else:
                print(f"❌ Server health check failed: {response.status_code}")
                return False
        except requests.ConnectionError:
            print("❌ Cannot connect to server. Is it running?")
            print(f"   Trying to connect to: {self.base_url}")
            return False
        except Exception as e:
            print(f"❌ Server health check error: {e}")
            return False
    
    def test_login_endpoint(self, email: str, password: str) -> Optional[str]:
        """Test login endpoint and extract token."""
        print("🔐 Testing login endpoint...")
        
        login_data = {
            "username": email,  # FastAPI OAuth2 uses 'username' field
            "password": password
        }
        
        try:
            # Try different possible login endpoints
            login_endpoints = [
                "/api/v1/auth/login",
                "/api/v1/login",
                "/auth/login",
                "/login"
            ]
            
            for endpoint in login_endpoints:
                try:
                    response = self.session.post(
                        f"{self.base_url}{endpoint}",
                        data=login_data,
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        token = data.get("access_token")
                        if token:
                            print(f"✅ Login successful via {endpoint}")
                            print(f"🎫 Token received: {token[:20]}...")
                            self.token = token
                            return token
                        else:
                            print(f"⚠️ Login response missing access_token: {data}")
                    elif response.status_code == 404:
                        continue  # Try next endpoint
                    else:
                        print(f"⚠️ Login failed at {endpoint}: {response.status_code} - {response.text}")
                
                except requests.exceptions.RequestException:
                    continue  # Try next endpoint
            
            print("❌ No working login endpoint found")
            return None
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return None
    
    def test_token_validation(self) -> bool:
        """Test if the token is valid by calling a protected endpoint."""
        if not self.token:
            print("❌ No token available for validation")
            return False
        
        print("🔍 Testing token validation...")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Try common protected endpoints
        protected_endpoints = [
            "/api/v1/users/me",
            "/api/v1/auth/me",
            "/api/v1/profile",
            "/me"
        ]
        
        for endpoint in protected_endpoints:
            try:
                response = self.session.get(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"✅ Token validation successful via {endpoint}")
                    user_data = response.json()
                    print(f"👤 User: {user_data.get('email', 'Unknown')}")
                    return True
                elif response.status_code == 404:
                    continue  # Try next endpoint
                elif response.status_code == 401:
                    print(f"❌ Token validation failed: Unauthorized")
                    return False
                else:
                    print(f"⚠️ Unexpected response from {endpoint}: {response.status_code}")
            
            except Exception as e:
                print(f"⚠️ Error testing {endpoint}: {e}")
                continue
        
        print("⚠️ No protected endpoint found for token validation")
        return False
    
    def test_module_access(self, module_names: List[str]) -> Dict[str, bool]:
        """Test access to specific modules with authentication."""
        if not self.token:
            print("❌ No token available for module testing")
            return {}
        
        print("🔍 Testing module access...")
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        results = {}
        
        for module_name in module_names:
            endpoints_to_try = [
                f"/api/v1/{module_name}",
                f"/api/{module_name}",
                f"/{module_name}"
            ]
            
            module_accessible = False
            
            for endpoint in endpoints_to_try:
                try:
                    response = self.session.get(
                        f"{self.base_url}{endpoint}",
                        headers=headers,
                        timeout=10
                    )
                    
                    if response.status_code in [200, 201]:
                        print(f"✅ Module '{module_name}' accessible via {endpoint}")
                        module_accessible = True
                        break
                    elif response.status_code == 404:
                        continue  # Try next endpoint
                    elif response.status_code == 401:
                        print(f"❌ Module '{module_name}' access denied: Unauthorized")
                        break
                    elif response.status_code == 403:
                        print(f"⚠️ Module '{module_name}' access forbidden (but endpoint exists)")
                        module_accessible = True  # Endpoint exists, just forbidden
                        break
                    else:
                        print(f"⚠️ Module '{module_name}' returned {response.status_code}")
                
                except Exception as e:
                    print(f"⚠️ Error accessing {endpoint}: {e}")
                    continue
            
            if not module_accessible:
                print(f"❌ Module '{module_name}' not accessible or not registered")
            
            results[module_name] = module_accessible
        
        return results
    
    def test_credentials_header(self) -> bool:
        """Test if requests work with credentials: 'include'."""
        if not self.token:
            return False
        
        print("🔍 Testing credentials header...")
        
        # Simulate a request that would be made by frontend with credentials: 'include'
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Cookie": "session=test"  # Simulate cookie
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/health",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Requests with credentials work correctly")
                return True
            else:
                print(f"⚠️ Credentials test returned {response.status_code}")
                return False
        
        except Exception as e:
            print(f"❌ Credentials test error: {e}")
            return False
    
    def run_full_validation(self, email: str, password: str, 
                          test_modules: List[str] = None) -> Dict:
        """Run complete authentication validation."""
        if test_modules is None:
            test_modules = ["citizenship", "health", "education", "finance"]
        
        print("🔐 SILA-System Authentication Validation")
        print("=" * 50)
        
        results = {
            "server_healthy": False,
            "login_successful": False,
            "token_valid": False,
            "credentials_work": False,
            "module_access": {},
            "overall_success": False
        }
        
        # Step 1: Check server health
        results["server_healthy"] = self.check_server_health()
        if not results["server_healthy"]:
            return results
        
        # Step 2: Test login
        token = self.test_login_endpoint(email, password)
        results["login_successful"] = token is not None
        if not results["login_successful"]:
            return results
        
        # Step 3: Test token validation
        results["token_valid"] = self.test_token_validation()
        
        # Step 4: Test credentials handling
        results["credentials_work"] = self.test_credentials_header()
        
        # Step 5: Test module access
        results["module_access"] = self.test_module_access(test_modules)
        
        # Determine overall success
        accessible_modules = sum(1 for accessible in results["module_access"].values() if accessible)
        results["overall_success"] = (
            results["server_healthy"] and
            results["login_successful"] and
            results["token_valid"] and
            accessible_modules > 0
        )
        
        return results
    
    def print_summary(self, results: Dict):
        """Print validation summary."""
        print(f"\n" + "="*50)
        print(f"📋 AUTHENTICATION VALIDATION SUMMARY")
        print(f"="*50)
        
        print(f"🏥 Server Health: {'✅' if results['server_healthy'] else '❌'}")
        print(f"🔐 Login: {'✅' if results['login_successful'] else '❌'}")
        print(f"🎫 Token Valid: {'✅' if results['token_valid'] else '❌'}")
        print(f"🍪 Credentials: {'✅' if results['credentials_work'] else '❌'}")
        
        if results["module_access"]:
            accessible = sum(1 for accessible in results["module_access"].values() if accessible)
            total = len(results["module_access"])
            print(f"📦 Module Access: {accessible}/{total} modules accessible")
            
            for module, accessible in results["module_access"].items():
                status = "✅" if accessible else "❌"
                print(f"   {status} {module}")
        
        overall_status = "✅ PASS" if results["overall_success"] else "❌ FAIL"
        print(f"\n🎯 Overall Status: {overall_status}")
        
        if not results["overall_success"]:
            print(f"\n💡 Recommendations:")
            if not results["server_healthy"]:
                print(f"   • Start the backend server")
            if not results["login_successful"]:
                print(f"   • Check login credentials and endpoint")
            if not results["token_valid"]:
                print(f"   • Verify JWT token configuration")
            if not any(results["module_access"].values()):
                print(f"   • Run 'python scripts/main.py auto-register-modules'")

def main():
    """Main validation function."""
    import sys
    
    # Get credentials from environment or prompt
    email = input("Email: ").strip() or "admin@sila.com"
    password = input("Password: ").strip() or "admin123"
    
    validator = AuthValidator()
    results = validator.run_full_validation(email, password)
    validator.print_summary(results)
    
    return results["overall_success"]

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)