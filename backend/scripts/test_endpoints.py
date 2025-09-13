"""
Automated API Testing Script for Windows/PowerShell
📋 Complete Solution for Reliable Endpoint Testing

Optimized for Windows environments with:
- PowerShell compatibility
- Automatic server detection
- Simple dependency management
- Comprehensive HTML reporting
- No external tool dependencies
"""

import requests
import time
import sys
from datetime import datetime
from pathlib import Path

# Configuration
SERVER_URL = "http://localhost:8000"
OPENAPI_URL = f"{SERVER_URL}/openapi.json"
REPORT_FILE = "endpoint_report.html"

def check_server_ready():
    """Check if server is responsive"""
    try:
        response = requests.get(f"{SERVER_URL}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def fetch_endpoints():
    """Get all API endpoints from OpenAPI spec"""
    try:
        response = requests.get(OPENAPI_URL, timeout=10)
        response.raise_for_status()
        
        endpoints = []
        openapi_data = response.json()
        
        for path, methods in openapi_data.get("paths", {}).items():
            for method in methods.keys():
                if method.upper() in ["GET", "POST"]:
                    endpoints.append((method.upper(), path))
        
        return endpoints
    except Exception as e:
        print(f"❌ Failed to fetch endpoints: {e}")
        sys.exit(1)

def test_endpoint(method, path):
    """Test a single endpoint"""
    url = SERVER_URL + path
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json={}, timeout=10)
        
        return response.status_code
    except:
        return "Error"

def generate_html_report(results):
    """Generate HTML report without external dependencies"""
    success_count = sum(1 for r in results if r[2] == 200)
    total_count = len(results)
    
    rows = "".join(
        f"<tr><td>{method}</td><td>{path}</td><td>{status}</td></tr>"
        for method, path, status in results
    )
    
    return f"""
    <html>
    <head><title>API Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .success {{ color: green; }} .error {{ color: red; }}
    </style>
    </head>
    <body>
        <h1>API Endpoint Test Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Results: <span class="success">{success_count} passed</span>, {total_count - success_count} failed, {total_count} total</p>
        <table>
            <tr><th>Method</th><th>Endpoint</th><th>Status</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """

def main():
    print("🔍 Checking if server is running...")
    
    if not check_server_ready():
        print("❌ Server not responding. Please start the server first:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    print("✅ Server is ready")
    print("📡 Fetching endpoints...")
    
    endpoints = fetch_endpoints()
    print(f"🔎 Found {len(endpoints)} endpoints to test")
    
    results = []
    for method, path in endpoints:
        status = test_endpoint(method, path)
        results.append((method, path, status))
        print(f"   {method} {path} -> {status}")
        time.sleep(0.1)
    
    # Generate HTML report
    with open(REPORT_FILE, 'w') as f:
        f.write(generate_html_report(results))
    
    print(f"📄 Report generated: {REPORT_FILE}")

if __name__ == "__main__":
    main()