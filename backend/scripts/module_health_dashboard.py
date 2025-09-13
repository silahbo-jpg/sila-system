#!/usr/bin/env python3
"""
SILA Module Health Dashboard
===========================

Creates an automated system to verify all 150 services across 25+ modules, ensuring each endpoint is:
✅ Technically discoverable (exists in code)
✅ Functionally operational (returns proper HTTP responses)
✅ Properly mapped to frontend interfaces (admin + citizen portals)
✅ Documented in the central service catalog

Part of the Complete Module Health Verification System as described in truman_try.txt
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configuration
SERVICES_FILE = Path(__file__).resolve().parents[1] / "modules_services.json"
TEST_RESULTS_FILE = Path(__file__).resolve().parents[1] / "services_test_report.json"
DASHBOARD_FILE = Path(__file__).resolve().parents[1] / "module_health_dashboard.html"

def load_expected_services() -> Dict[str, Any]:
    """Load expected services from the central catalog"""
    if not SERVICES_FILE.exists():
        print(f"❌ Services catalog not found: {SERVICES_FILE}")
        return {}
    
    try:
        with open(SERVICES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading services catalog: {e}")
        return {}

def load_test_results() -> Dict[str, Any]:
    """Load actual test results from latest test run"""
    if not TEST_RESULTS_FILE.exists():
        print(f"⚠️ Test results not found: {TEST_RESULTS_FILE}")
        return {}
    
    try:
        with open(TEST_RESULTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading test results: {e}")
        return {}

def analyze_module_health(expected_services: Dict[str, Any], test_results: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Compare expected vs actual service status"""
    health_data = []
    
    for module_name, expected_data in expected_services.items():
        # Get expected services count
        expected_count = len(expected_data.get('services', []))
        
        # Get discovered services from test results
        test_data = test_results.get(module_name, {})
        discovered_services = test_data.get('services', [])
        discovered_count = len(discovered_services)
        
        # Count functional services
        functional_count = sum(1 for s in discovered_services 
                             if s.get('status') == 'SUCCESS')
        
        # Count services with frontend mappings
        admin_mapped = sum(1 for s in expected_data.get('services', [])
                          if s.get('frontend_admin'))
        citizen_mapped = sum(1 for s in expected_data.get('services', [])
                            if s.get('frontend_citizen'))
        
        # Calculate health status
        if discovered_count == 0:
            status = "❌ Not Discovered"
        elif discovered_count < expected_count:
            status = "⚠️ Partial Discovery"
        elif functional_count < discovered_count:
            status = "⚠️ Functional Issues"
        elif admin_mapped < expected_count or citizen_mapped < expected_count:
            status = "⚠️ Mapping Incomplete"
        else:
            status = "✅ Healthy"
        
        health_data.append({
            'Module': module_name,
            'Display Name': expected_data.get('display_name', ''),
            'Expected Services': expected_count,
            'Discovered Services': discovered_count,
            'Functional Services': functional_count,
            'Admin Mapped': admin_mapped,
            'Citizen Mapped': citizen_mapped,
            'Status': status
        })
    
    return health_data

def generate_dashboard(health_data: List[Dict[str, Any]]) -> Path:
    """Generate comprehensive HTML dashboard"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(health_data)
    
    # Calculate totals
    total_expected = df['Expected Services'].sum()
    total_discovered = df['Discovered Services'].sum()
    total_functional = df['Functional Services'].sum()
    total_admin_mapped = df['Admin Mapped'].sum()
    total_citizen_mapped = df['Citizen Mapped'].sum()
    
    # Generate module rows
    module_rows = ""
    for _, row in df.iterrows():
        status_class = "healthy" if row['Status'] == "✅ Healthy" else "warning" if "⚠️" in row['Status'] else "critical"
        
        module_rows += f"""
        <tr class="{status_class}">
            <td>{row['Module']}</td>
            <td>{row['Display Name']}</td>
            <td>{row['Expected Services']}</td>
            <td>{row['Discovered Services']}</td>
            <td>{row['Functional Services']}</td>
            <td>{row['Admin Mapped']}</td>
            <td>{row['Citizen Mapped']}</td>
            <td class="status-cell">{row['Status']}</td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Module Health Dashboard</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; color: #333; }}
            .container {{ max-width: 1600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee; }}
            h1 {{ color: #2c3e50; margin-bottom: 10px; }}
            
            .summary {{ display: flex; justify-content: space-around; margin: 20px 0; flex-wrap: wrap; }}
            .stat-box {{ background: #f8f9fa; padding: 15px; border-radius: 6px; text-align: center; min-width: 150px; margin: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            .stat-total {{ border-left: 4px solid #2196F3; }}
            .stat-discovered {{ border-left: 4px solid #4CAF50; }}
            .stat-functional {{ border-left: 4px solid #FF9800; }}
            .stat-mapped {{ border-left: 4px solid #9C27B0; }}
            .stat-number {{ font-size: 24px; font-weight: bold; margin: 5px 0; }}
            
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; }}
            th, td {{ padding: 12px 15px; border: 1px solid #ddd; text-align: center; }}
            th {{ background-color: #2c3e50; color: white; position: sticky; top: 0; }}
            
            tr.healthy {{ background-color: #e8f5e9; }}
            tr.warning {{ background-color: #fff8e1; }}
            tr.critical {{ background-color: #ffebee; }}
            
            .status-cell {{ font-weight: bold; }}
            .healthy .status-cell {{ color: #4CAF50; }}
            .warning .status-cell {{ color: #FF9800; }}
            .critical .status-cell {{ color: #F44336; }}
            
            .footer {{ margin-top: 30px; text-align: center; color: #6c757d; font-size: 14px; }}
            
            @media (max-width: 1200px) {{
                .container {{ padding: 10px; }}
                table {{ font-size: 12px; }}
                th, td {{ padding: 8px 10px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Module Health Dashboard</h1>
                <p><b>Generated:</b> {now}</p>
                <p><b>Catalog:</b> {SERVICES_FILE.name}</p>
            </header>
            
            <div class="summary">
                <div class="stat-box stat-total">
                    <div class="stat-label">Expected Services</div>
                    <div class="stat-number">{total_expected}</div>
                </div>
                <div class="stat-box stat-discovered">
                    <div class="stat-label">Discovered</div>
                    <div class="stat-number">{total_discovered}</div>
                </div>
                <div class="stat-box stat-functional">
                    <div class="stat-label">Functional</div>
                    <div class="stat-number">{total_functional}</div>
                </div>
                <div class="stat-box stat-mapped">
                    <div class="stat-label">Admin Mapped</div>
                    <div class="stat-number">{total_admin_mapped}</div>
                </div>
                <div class="stat-box stat-mapped">
                    <div class="stat-label">Citizen Mapped</div>
                    <div class="stat-number">{total_citizen_mapped}</div>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Module ID</th>
                        <th>Display Name</th>
                        <th>Expected</th>
                        <th>Discovered</th>
                        <th>Functional</th>
                        <th>Admin Mapped</th>
                        <th>Citizen Mapped</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {module_rows}
                </tbody>
            </table>
            
            <div class="footer">
                <p>Dashboard generated by SILA Health Monitoring System | {now}</p>
                <p>✅ Healthy: All services discovered, functional, and properly mapped</p>
                <p>⚠️ Warning: Partial discovery, functional issues, or incomplete mapping</p>
                <p>❌ Critical: No services discovered or major issues</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(DASHBOARD_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return DASHBOARD_FILE

def main():
    """Main function to generate health dashboard"""
    print("📊 Generating Module Health Dashboard...")
    print("=" * 60)
    
    # Load expected services and test results
    expected_services = load_expected_services()
    if not expected_services:
        return
    
    test_results = load_test_results()
    if not test_results:
        print("⚠️ No test results found. Run test_all_services.py first.")
        return
    
    # Analyze module health
    health_data = analyze_module_health(expected_services, test_results)
    
    # Generate dashboard
    dashboard_path = generate_dashboard(health_data)
    
    print("=" * 60)
    print(f"✅ Health dashboard generated: {dashboard_path}")
    
    # Print summary
    total_modules = len(health_data)
    healthy_modules = sum(1 for m in health_data if m['Status'] == '✅ Healthy')
    
    print(f"📈 Summary: {healthy_modules}/{total_modules} modules fully healthy")

if __name__ == "__main__":
    main()