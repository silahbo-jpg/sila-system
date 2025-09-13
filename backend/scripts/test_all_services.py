#!/usr/bin/env python3
"""
SILA Comprehensive Service Testing System
=========================================

Tests all discovered API endpoints and generates detailed HTML reports.
Harmonized with SILA's automation hub and project structure.
"""

import json
import requests
import time
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from urllib.parse import urljoin

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Configuration aligned with SILA project
SERVER_URL = "http://localhost:8000"
SERVICES_FILE = Path(__file__).resolve().parents[1] / "modules_services.json"
REPORT_FILE = Path(__file__).resolve().parents[1] / "services_test_report.html"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

class ServiceTester:
    """Comprehensive service testing with intelligent error handling"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SILA-Service-Tester/1.0',
            'Accept': 'application/json',
        })
        self.test_results = {}
        self.start_time = datetime.now()
        
    def load_services_config(self) -> Optional[Dict[str, Any]]:
        """Load services configuration from JSON file"""
        if not SERVICES_FILE.exists():
            print(f"❌ Services file not found: {SERVICES_FILE}")
            print("💡 Run generate_services_map.py first to create the services map")
            return None
            
        try:
            with open(SERVICES_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"📄 Loaded configuration with {len(config)} modules")
                return config
        except Exception as e:
            print(f"❌ Error loading services file: {e}")
            return None

    def check_server_ready(self) -> bool:
        """Check if the SILA server is ready and responsive"""
        endpoints_to_check = ["/docs", "/health", "/ping", "/api/v1"]
        
        for endpoint in endpoints_to_check:
            try:
                response = self.session.get(f"{SERVER_URL}{endpoint}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ Server ready (verified via {endpoint})")
                    return True
            except:
                continue
        
        print("❌ Server not responding on any known endpoints")
        return False

    def test_endpoint(self, method: str, endpoint: str, module_name: str) -> Tuple[str, str, Dict[str, Any]]:
        """Test a single endpoint with intelligent handling"""
        url = urljoin(SERVER_URL, endpoint.lstrip('/'))
        
        # Enhanced skip logic for SILA system
        skip_patterns = [
            '/internal/',  # Internal endpoints may require special auth
            '/{id}',       # Endpoints with path parameters
            '/id',         # ID-based endpoints without specific ID
        ]
        
        if any(pattern in endpoint for pattern in skip_patterns):
            return "SKIP", "Requires parameters or internal access", {}
        
        if method.upper() not in ['GET', 'HEAD', 'OPTIONS']:
            return "SKIP", f"Non-GET method ({method}) - manual testing required", {}
        
        # Perform the test with retries
        for attempt in range(MAX_RETRIES):
            try:
                start_time = time.time()
                
                if method.upper() == 'HEAD':
                    response = self.session.head(url, timeout=REQUEST_TIMEOUT)
                elif method.upper() == 'OPTIONS':
                    response = self.session.options(url, timeout=REQUEST_TIMEOUT)
                else:
                    response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                
                response_time = round((time.time() - start_time) * 1000, 2)
                
                # Analyze response
                status_info = {
                    'status_code': response.status_code,
                    'response_time_ms': response_time,
                    'content_type': response.headers.get('content-type', 'unknown'),
                    'content_length': len(response.content),
                    'attempt': attempt + 1
                }
                
                if response.status_code < 400:
                    return "SUCCESS", f"{response.status_code} ({response_time}ms)", status_info
                elif response.status_code in [401, 403]:
                    return "AUTH_REQUIRED", f"{response.status_code} - Authentication required ({response_time}ms)", status_info
                elif response.status_code == 404:
                    return "NOT_FOUND", f"404 - Endpoint not found ({response_time}ms)", status_info
                elif response.status_code in [422, 400]:
                    return "VALIDATION_ERROR", f"{response.status_code} - Validation error ({response_time}ms)", status_info
                else:
                    return "WARNING", f"{response.status_code} ({response_time}ms)", status_info
                    
            except requests.exceptions.Timeout:
                if attempt == MAX_RETRIES - 1:
                    return "ERROR", f"Timeout after {REQUEST_TIMEOUT}s (tried {MAX_RETRIES} times)", {}
            except requests.exceptions.ConnectionError:
                if attempt == MAX_RETRIES - 1:
                    return "ERROR", "Connection refused - server may be down", {}
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    return "ERROR", f"Unexpected error: {str(e)}", {}
            
            # Brief pause between retries
            time.sleep(0.5)
        
        return "ERROR", "Max retries exceeded", {}

    def test_all_services(self, services_config: Dict[str, Any]) -> Dict[str, Any]:
        """Test all services and return comprehensive results"""
        print("🧪 Starting comprehensive service testing...")
        results = {}
        
        total_endpoints = sum(
            len(module_data.get('services', [])) 
            for module_data in services_config.values()
        )
        
        tested_count = 0
        
        for module_name, module_data in services_config.items():
            print(f"   📋 Testing module: {module_name}")
            module_results = []
            
            for service in module_data.get('services', []):
                endpoint = service['endpoint']
                method = service['methods'][0] if service['methods'] else 'GET'
                
                tested_count += 1
                print(f"      [{tested_count}/{total_endpoints}] {method} {endpoint}")
                
                status, message, details = self.test_endpoint(method, endpoint, module_name)
                
                result = {
                    'endpoint': endpoint,
                    'method': method,
                    'status': status,
                    'message': message,
                    'details': details,
                    'function_name': service.get('function_name'),
                    'description': service.get('description'),
                    'router_prefix': service.get('router_prefix', ''),
                    'router_tags': service.get('router_tags', []),
                    'frontend_admin': service.get('frontend_admin'),
                    'frontend_citizen': service.get('frontend_citizen'),
                    'test_timestamp': datetime.now().isoformat()
                }
                
                module_results.append(result)
                
                # Brief pause between requests
                time.sleep(0.1)
            
            results[module_name] = {
                'display_name': module_data.get('display_name', module_name),
                'module_path': module_data.get('module_path', ''),
                'services': module_results,
                'total_tested': len(module_results)
            }
        
        return results

    def update_services_config(self, services_config: Dict[str, Any], test_results: Dict[str, Any]):
        """Update the services configuration with test results"""
        try:
            for module_name, module_data in services_config.items():
                if module_name in test_results:
                    test_module = test_results[module_name]
                    
                    # Update each service with test results
                    for i, service in enumerate(module_data.get('services', [])):
                        if i < len(test_module['services']):
                            test_result = test_module['services'][i]
                            service['test_status'] = test_result['status']
                            service['last_test_result'] = test_result['message']
                            service['last_test_time'] = test_result['test_timestamp']
                            service['test_details'] = test_result['details']
            
            # Save updated configuration
            with open(SERVICES_FILE, 'w', encoding='utf-8') as f:
                json.dump(services_config, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Updated services configuration with test results")
            
        except Exception as e:
            print(f"⚠️  Failed to update services config: {e}")

    def generate_html_report(self, test_results: Dict[str, Any]) -> Path:
        """Generate comprehensive HTML test report"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = datetime.now() - self.start_time
        
        # Calculate statistics
        stats = self._calculate_statistics(test_results)
        
        # Generate CSS and JavaScript
        css_styles = self._generate_css()
        javascript = self._generate_javascript()
        
        # Generate module sections
        module_sections = self._generate_module_sections(test_results)
        
        # Main HTML template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SILA Service Test Report</title>
    {css_styles}
</head>
<body>
    <div class="container">
        <header>
            <h1>🏛️ SILA Service Test Report</h1>
            <div class="header-info">
                <p><strong>Generated:</strong> {now}</p>
                <p><strong>Server:</strong> {SERVER_URL}</p>
                <p><strong>Duration:</strong> {duration.total_seconds():.1f} seconds</p>
            </div>
        </header>
        
        <div class="summary">
            {self._generate_summary_cards(stats)}
        </div>
        
        <div class="filters">
            <button class="filter-btn active" onclick="filterResults('all')">All ({stats['total']})</button>
            <button class="filter-btn" onclick="filterResults('SUCCESS')">Success ({stats['success']})</button>
            <button class="filter-btn" onclick="filterResults('AUTH_REQUIRED')">Auth Required ({stats['auth_required']})</button>
            <button class="filter-btn" onclick="filterResults('WARNING')">Warnings ({stats['warning']})</button>
            <button class="filter-btn" onclick="filterResults('ERROR')">Errors ({stats['error']})</button>
            <button class="filter-btn" onclick="filterResults('SKIP')">Skipped ({stats['skip']})</button>
        </div>
        
        {module_sections}
        
        <footer>
            <p>Generated by SILA Automated Testing System | {now}</p>
            <p>Part of SILA's comprehensive automation hub</p>
        </footer>
    </div>
    {javascript}
</body>
</html>"""
        
        # Ensure reports directory exists
        REPORTS_DIR.mkdir(exist_ok=True)
        
        # Save report
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Also save timestamped copy
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamped_report = REPORTS_DIR / f"service_test_report_{timestamp}.html"
        with open(timestamped_report, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return REPORT_FILE

    def _calculate_statistics(self, test_results: Dict[str, Any]) -> Dict[str, int]:
        """Calculate testing statistics"""
        stats = {
            'total': 0, 'success': 0, 'auth_required': 0, 
            'warning': 0, 'error': 0, 'skip': 0, 'not_found': 0, 'validation_error': 0
        }
        
        for module_data in test_results.values():
            for service in module_data['services']:
                stats['total'] += 1
                status = service['status'].lower()
                if status == 'success':
                    stats['success'] += 1
                elif status == 'auth_required':
                    stats['auth_required'] += 1
                elif status == 'warning':
                    stats['warning'] += 1
                elif status == 'error':
                    stats['error'] += 1
                elif status == 'skip':
                    stats['skip'] += 1
                elif status == 'not_found':
                    stats['not_found'] += 1
                elif status == 'validation_error':
                    stats['validation_error'] += 1
        
        return stats

    def _generate_css(self) -> str:
        """Generate CSS styles for the report"""
        return """<style>
            * { box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; color: #333; }
            .container { max-width: 1400px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
            h1 { color: #2c3e50; margin-bottom: 10px; }
            .header-info { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; }
            .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
            .stat-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .stat-number { font-size: 28px; font-weight: bold; margin: 10px 0; }
            .stat-total { border-left: 4px solid #2196F3; }
            .stat-success { border-left: 4px solid #4CAF50; }
            .stat-auth { border-left: 4px solid #FF9800; }
            .stat-warning { border-left: 4px solid #FF5722; }
            .stat-error { border-left: 4px solid #F44336; }
            .stat-skip { border-left: 4px solid #9E9E9E; }
            .filters { display: flex; gap: 10px; margin: 20px 0; flex-wrap: wrap; }
            .filter-btn { padding: 10px 15px; border: 1px solid #ddd; background: white; border-radius: 5px; cursor: pointer; transition: all 0.3s; }
            .filter-btn.active, .filter-btn:hover { background: #2c3e50; color: white; }
            .module-section { margin: 25px 0; }
            .module-header { background: #2c3e50; color: white; padding: 15px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
            .module-stats { font-size: 14px; opacity: 0.9; }
            .services-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            .services-table th, .services-table td { padding: 12px; border: 1px solid #ddd; text-align: left; }
            .services-table th { background: #34495e; color: white; position: sticky; top: 0; }
            .service-row { transition: background-color 0.3s; }
            .service-row:hover { background-color: #f5f5f5; }
            .status-SUCCESS { background-color: #e8f5e9; }
            .status-AUTH_REQUIRED { background-color: #fff3e0; }
            .status-WARNING { background-color: #ffebee; }
            .status-ERROR { background-color: #ffebee; }
            .status-SKIP { background-color: #f5f5f5; }
            .status-NOT_FOUND { background-color: #fce4ec; }
            .status-VALIDATION_ERROR { background-color: #fff8e1; }
            .status-badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
            .badge-SUCCESS { background: #4CAF50; color: white; }
            .badge-AUTH_REQUIRED { background: #FF9800; color: white; }
            .badge-WARNING { background: #FF5722; color: white; }
            .badge-ERROR { background: #F44336; color: white; }
            .badge-SKIP { background: #9E9E9E; color: white; }
            .badge-NOT_FOUND { background: #E91E63; color: white; }
            .badge-VALIDATION_ERROR { background: #FFC107; color: black; }
            .endpoint-details { font-family: 'Courier New', monospace; font-size: 14px; }
            .method-badge { padding: 2px 6px; border-radius: 3px; font-size: 11px; font-weight: bold; margin-right: 5px; }
            .method-GET { background: #28a745; color: white; }
            .method-POST { background: #007bff; color: white; }
            .method-PUT { background: #ffc107; color: black; }
            .method-DELETE { background: #dc3545; color: white; }
            footer { margin-top: 40px; text-align: center; color: #6c757d; font-size: 14px; padding-top: 20px; border-top: 1px solid #eee; }
            .hidden { display: none; }
        </style>"""

    def _generate_javascript(self) -> str:
        """Generate JavaScript for interactive features"""
        return """<script>
            function filterResults(status) {
                const rows = document.querySelectorAll('.service-row');
                const buttons = document.querySelectorAll('.filter-btn');
                
                // Update button states
                buttons.forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
                
                // Show/hide rows
                rows.forEach(row => {
                    if (status === 'all' || row.classList.contains('status-' + status)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }
            
            // Add click handlers for expandable details
            document.addEventListener('DOMContentLoaded', function() {
                const detailRows = document.querySelectorAll('.detail-toggle');
                detailRows.forEach(row => {
                    row.addEventListener('click', function() {
                        const details = this.nextElementSibling;
                        if (details && details.classList.contains('service-details')) {
                            details.style.display = details.style.display === 'none' ? '' : 'none';
                        }
                    });
                });
            });
        </script>"""

    def _generate_summary_cards(self, stats: Dict[str, int]) -> str:
        """Generate summary statistics cards"""
        return f"""
            <div class="stat-card stat-total">
                <div class="stat-label">Total Endpoints</div>
                <div class="stat-number">{stats['total']}</div>
            </div>
            <div class="stat-card stat-success">
                <div class="stat-label">Successful</div>
                <div class="stat-number">{stats['success']}</div>
            </div>
            <div class="stat-card stat-auth">
                <div class="stat-label">Auth Required</div>
                <div class="stat-number">{stats['auth_required']}</div>
            </div>
            <div class="stat-card stat-warning">
                <div class="stat-label">Warnings</div>
                <div class="stat-number">{stats['warning']}</div>
            </div>
            <div class="stat-card stat-error">
                <div class="stat-label">Errors</div>
                <div class="stat-number">{stats['error']}</div>
            </div>
            <div class="stat-card stat-skip">
                <div class="stat-label">Skipped</div>
                <div class="stat-number">{stats['skip']}</div>
            </div>
        """

    def _generate_module_sections(self, test_results: Dict[str, Any]) -> str:
        """Generate HTML for module sections"""
        sections = []
        
        for module_name, module_data in test_results.items():
            # Calculate module statistics
            module_stats = self._calculate_statistics({module_name: module_data})
            
            # Generate service rows
            service_rows = []
            for service in module_data['services']:
                status = service['status']
                status_icon = self._get_status_icon(status)
                method_class = f"method-{service['method']}"
                
                details = service.get('details', {})
                response_time = details.get('response_time_ms', 'N/A')
                
                service_rows.append(f"""
                <tr class="service-row status-{status}">
                    <td><span class="method-badge {method_class}">{service['method']}</span></td>
                    <td class="endpoint-details">{service['endpoint']}</td>
                    <td><span class="status-badge badge-{status}">{status_icon} {status}</span></td>
                    <td>{service['message']}</td>
                    <td>{response_time}ms</td>
                    <td>{service.get('description', 'N/A')}</td>
                    <td>{service.get('frontend_admin') or 'Not set'}</td>
                    <td>{service.get('frontend_citizen') or 'Not set'}</td>
                </tr>
                """)
            
            sections.append(f"""
            <div class="module-section">
                <div class="module-header">
                    <h3>{module_data['display_name']} ({module_name})</h3>
                    <div class="module-stats">
                        {module_stats['success']}/{module_stats['total']} successful
                    </div>
                </div>
                <table class="services-table">
                    <thead>
                        <tr>
                            <th>Method</th>
                            <th>Endpoint</th>
                            <th>Status</th>
                            <th>Details</th>
                            <th>Response Time</th>
                            <th>Description</th>
                            <th>Admin Frontend</th>
                            <th>Citizen Frontend</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(service_rows)}
                    </tbody>
                </table>
            </div>
            """)
        
        return ''.join(sections)

    def _get_status_icon(self, status: str) -> str:
        """Get appropriate icon for status"""
        icons = {
            'SUCCESS': '✅',
            'AUTH_REQUIRED': '🔐',
            'WARNING': '⚠️',
            'ERROR': '❌',
            'SKIP': '⏭️',
            'NOT_FOUND': '🔍',
            'VALIDATION_ERROR': '📝'
        }
        return icons.get(status, '❓')
    
    def save_test_results(self, test_results: Dict[str, Any]) -> Path:
        """Save test results to JSON file for dashboard"""
        output_file = Path(__file__).resolve().parents[1] / "services_test_report.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(test_results, f, indent=2, ensure_ascii=False)
            return output_file
        except Exception as e:
            print(f"❌ Error saving test results: {e}")
            return None

def main():
    """Main execution function"""
    print("🚀 SILA Comprehensive Service Testing Starting...")
    print("=" * 70)
    
    tester = ServiceTester()
    
    # Load services configuration
    print("\n📂 LOADING SERVICES CONFIGURATION...")
    services_config = tester.load_services_config()
    if not services_config:
        return
    
    # Check server availability
    print("\n🌐 CHECKING SERVER AVAILABILITY...")
    if not tester.check_server_ready():
        print("❌ Server is not responding. Please start the server first.")
        print("💡 Try: python -m uvicorn app.main:app --reload")
        return
    
    # Run comprehensive tests
    print("\n🧪 RUNNING COMPREHENSIVE SERVICE TESTS...")
    test_results = tester.test_all_services(services_config)
    
    if not test_results:
        print("❌ No test results generated")
        return
    
    # Update services configuration with results
    print("\n💾 UPDATING SERVICES CONFIGURATION...")
    tester.update_services_config(services_config, test_results)
    
    # Generate HTML report
    print("\n📄 GENERATING COMPREHENSIVE REPORT...")
    report_path = tester.generate_html_report(test_results)
    
    # Save test results for dashboard
    print("\n💾 SAVING RESULTS FOR DASHBOARD...")
    results_file = tester.save_test_results(test_results)
    if results_file:
        print(f"💾 Test results saved: {results_file}")
    
    print("\n" + "=" * 70)
    print("✅ COMPREHENSIVE TESTING COMPLETE!")
    print(f"📄 Main Report: {report_path}")
    print(f"📁 Additional Reports: {REPORTS_DIR}")
    if 'results_file' in locals() and results_file:
        print(f"💾 JSON Results: {results_file}")
    
    # Print summary
    stats = tester._calculate_statistics(test_results)
    print(f"\n📊 FINAL RESULTS:")
    print(f"   • {stats['total']} endpoints tested")
    print(f"   • {stats['success']} successful")
    print(f"   • {stats['auth_required']} require authentication")
    print(f"   • {stats['warning']} warnings")
    print(f"   • {stats['error']} errors")
    print(f"   • {stats['skip']} skipped")
    
    success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
    print(f"   • {success_rate:.1f}% success rate")
    
    print(f"\n💡 Open {report_path} in your browser to view the detailed report")

if __name__ == "__main__":
    main()