#!/usr/bin/env python3
"""
SILA Automated Service Mapping & Discovery System
=================================================

This script automatically discovers all API endpoints from FastAPI modules
in the SILA system and generates a comprehensive service mapping for testing
and frontend integration.

Compatible with SILA's modular architecture and script automation hub.
"""

import importlib
import inspect
import json
import pkgutil
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from fastapi import APIRouter

# Add the parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Configuration paths aligned with SILA project structure
MODULES_DIR = Path(__file__).resolve().parents[1] / "app" / "modules"
OUTPUT_FILE = Path(__file__).resolve().parents[1] / "modules_services.json"
BACKUP_DIR = Path(__file__).resolve().parents[1] / "reports"

def ensure_output_directories():
    """Ensure required output directories exist"""
    BACKUP_DIR.mkdir(exist_ok=True)
    print(f"📁 Output directory ready: {BACKUP_DIR}")

def discover_module_routers(module_path: str) -> List[Dict[str, Any]]:
    """
    Discover all APIRouter instances and their routes in a module.
    
    Args:
        module_path: Full import path of the module
        
    Returns:
        List of service endpoints with metadata
    """
    try:
        # Import the module
        module = importlib.import_module(module_path)
        module_services = []
        
        # Recursively search for APIRouter instances in the module
        def find_routers_recursive(obj, visited=None):
            if visited is None:
                visited = set()
                
            # Avoid infinite recursion
            if id(obj) in visited:
                return []
            visited.add(id(obj))
            
            routers = []
            
            # Check if object is an APIRouter
            if isinstance(obj, APIRouter):
                routers.append(obj)
            
            # Search in module attributes
            if hasattr(obj, '__dict__'):
                for name, attr in obj.__dict__.items():
                    if not name.startswith('_'):
                        routers.extend(find_routers_recursive(attr, visited.copy()))
            
            # Search in module members if it's a module
            if inspect.ismodule(obj):
                for name, member in inspect.getmembers(obj):
                    if not name.startswith('_') and member is not obj:
                        routers.extend(find_routers_recursive(member, visited.copy()))
            
            return routers
        
        # Find all routers in the module
        routers = find_routers_recursive(module)
        
        for router in routers:
            try:
                # Extract routes from the router
                for route in router.routes:
                    if hasattr(route, 'path') and hasattr(route, 'methods'):
                        # Clean up path formatting
                        endpoint_path = route.path
                        if not endpoint_path.startswith('/'):
                            endpoint_path = '/' + endpoint_path
                        
                        # Get route methods
                        methods = list(route.methods) if route.methods else ['GET']
                        
                        # Get function name and docstring if available
                        function_name = None
                        description = None
                        if hasattr(route, 'endpoint') and route.endpoint:
                            function_name = getattr(route.endpoint, '__name__', None)
                            description = getattr(route.endpoint, '__doc__', None)
                            if description:
                                description = description.strip().split('\n')[0]  # First line only
                        
                        module_services.append({
                            "endpoint": endpoint_path,
                            "methods": methods,
                            "function_name": function_name,
                            "description": description,
                            "router_prefix": getattr(router, 'prefix', ''),
                            "router_tags": getattr(router, 'tags', []),
                            "frontend_admin": None,
                            "frontend_citizen": None,
                            "test_status": "pending"
                        })
            except Exception as e:
                print(f"   ⚠️  Error processing router in {module_path}: {str(e)}")
                continue
        
        return module_services
        
    except Exception as e:
        print(f"   ❌ Error importing {module_path}: {str(e)}")
        return []

def discover_services() -> Dict[str, Any]:
    """
    Discover all API endpoints from FastAPI modules in the SILA system.
    
    Returns:
        Dictionary mapping module names to their services
    """
    services_map = {}
    
    print(f"🔍 Scanning modules directory: {MODULES_DIR}")
    
    if not MODULES_DIR.exists():
        print(f"❌ Modules directory not found: {MODULES_DIR}")
        return services_map
    
    # Iterate through all modules in the modules directory
    total_modules = 0
    processed_modules = 0
    
    for module_dir in MODULES_DIR.iterdir():
        if not module_dir.is_dir() or module_dir.name.startswith('__'):
            continue
            
        total_modules += 1
        module_name = module_dir.name
        
        print(f"📦 Processing module: {module_name}")
        
        # Try to discover services from the main module
        module_services = []
        
        # Check for routes in the module's routes directory
        routes_dir = module_dir / "routes"
        if routes_dir.exists():
            for route_file in routes_dir.glob("*.py"):
                if route_file.name.startswith('__'):
                    continue
                    
                route_module_name = route_file.stem
                full_module_path = f"app.modules.{module_name}.routes.{route_module_name}"
                
                print(f"   🔍 Scanning route file: {route_module_name}")
                route_services = discover_module_routers(full_module_path)
                module_services.extend(route_services)
        
        # Also check the main module __init__.py for any routers
        main_module_path = f"app.modules.{module_name}"
        main_services = discover_module_routers(main_module_path)
        module_services.extend(main_services)
        
        # Add to services map if we found any services
        if module_services:
            services_map[module_name] = {
                "display_name": module_name.capitalize().replace('_', ' '),
                "module_path": str(module_dir.relative_to(MODULES_DIR.parent.parent)),
                "total_endpoints": len(module_services),
                "services": module_services,
                "last_scanned": None,
                "scan_status": "success"
            }
            processed_modules += 1
            print(f"   ✅ Found {len(module_services)} endpoints in {module_name}")
        else:
            # Still add the module but mark it as having no endpoints
            services_map[module_name] = {
                "display_name": module_name.capitalize().replace('_', ' '),
                "module_path": str(module_dir.relative_to(MODULES_DIR.parent.parent)),
                "total_endpoints": 0,
                "services": [],
                "last_scanned": None,
                "scan_status": "no_endpoints"
            }
            print(f"   ⚠️  No endpoints found in {module_name}")
    
    print(f"📊 Scan complete: {processed_modules}/{total_modules} modules with endpoints")
    return services_map

def load_existing_config() -> Dict[str, Any]:
    """
    Load existing configuration to preserve frontend mappings and test results.
    
    Returns:
        Existing configuration dictionary or empty dict
    """
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
                print(f"📄 Loaded existing configuration with {len(existing_config)} modules")
                return existing_config
        except Exception as e:
            print(f"⚠️  Error loading existing config: {e}")
            return {}
    return {}

def merge_services(existing_config: Dict[str, Any], discovered_services: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge discovered services with existing configuration to preserve frontend mappings.
    
    Args:
        existing_config: Previously saved configuration
        discovered_services: Newly discovered services
        
    Returns:
        Merged configuration preserving important user data
    """
    merged_config = existing_config.copy()
    
    for module_name, module_data in discovered_services.items():
        if module_name in merged_config:
            # Update existing module with new endpoints
            existing_services = {
                f"{s.get('endpoint', '')}-{s.get('methods', [''])[0]}": s 
                for s in merged_config[module_name].get('services', [])
            }
            
            for new_service in module_data['services']:
                service_key = f"{new_service['endpoint']}-{new_service['methods'][0] if new_service['methods'] else 'GET'}"
                
                if service_key in existing_services:
                    # Preserve frontend mappings and test results for existing endpoints
                    existing_service = existing_services[service_key]
                    new_service['frontend_admin'] = existing_service.get('frontend_admin')
                    new_service['frontend_citizen'] = existing_service.get('frontend_citizen')
                    new_service['test_status'] = existing_service.get('test_status', 'pending')
                    new_service['last_test_result'] = existing_service.get('last_test_result')
                    new_service['last_test_time'] = existing_service.get('last_test_time')
            
            # Update module metadata but preserve user customizations
            merged_config[module_name].update({
                'services': module_data['services'],
                'total_endpoints': module_data['total_endpoints'],
                'last_scanned': module_data.get('last_scanned'),
                'scan_status': module_data.get('scan_status')
            })
            
            print(f"   🔄 Updated existing module: {module_name}")
        else:
            # Add new module
            merged_config[module_name] = module_data
            print(f"   ➕ Added new module: {module_name}")
    
    return merged_config

def save_backup(config: Dict[str, Any]):
    """Save a backup of the configuration to the reports directory"""
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"services_map_backup_{timestamp}.json"
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"💾 Backup saved: {backup_file}")
    except Exception as e:
        print(f"⚠️  Failed to save backup: {e}")

def generate_summary_report(config: Dict[str, Any]) -> str:
    """Generate a text summary report of the discovered services"""
    from datetime import datetime
    
    total_modules = len(config)
    total_endpoints = sum(mod.get('total_endpoints', 0) for mod in config.values())
    modules_with_endpoints = sum(1 for mod in config.values() if mod.get('total_endpoints', 0) > 0)
    
    # Method distribution
    method_counts = {}
    for module_data in config.values():
        for service in module_data.get('services', []):
            for method in service.get('methods', []):
                method_counts[method] = method_counts.get(method, 0) + 1
    
    report_lines = [
        "SILA Service Discovery Summary Report",
        "=" * 50,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "📊 OVERVIEW:",
        f"  • Total Modules Scanned: {total_modules}",
        f"  • Modules with Endpoints: {modules_with_endpoints}",
        f"  • Total API Endpoints: {total_endpoints}",
        "",
        "🔍 HTTP METHODS DISTRIBUTION:",
    ]
    
    for method, count in sorted(method_counts.items()):
        report_lines.append(f"  • {method}: {count} endpoints")
    
    report_lines.extend([
        "",
        "📋 MODULE BREAKDOWN:",
    ])
    
    for module_name, module_data in sorted(config.items()):
        endpoint_count = module_data.get('total_endpoints', 0)
        status = module_data.get('scan_status', 'unknown')
        status_icon = "✅" if status == "success" else "⚠️" if status == "no_endpoints" else "❌"
        
        report_lines.append(f"  {status_icon} {module_data.get('display_name', module_name)}: {endpoint_count} endpoints")
    
    return "\n".join(report_lines)

def main():
    """Main execution function"""
    print("🚀 SILA Automated Service Discovery Starting...")
    print("=" * 60)
    
    # Ensure output directories exist
    ensure_output_directories()
    
    # Discover services from modules
    print("\n🔍 DISCOVERING SERVICES...")
    discovered_services = discover_services()
    
    if not discovered_services:
        print("❌ No services discovered. Please check the module structure.")
        return
    
    # Load existing configuration to preserve frontend mappings
    print("\n📂 LOADING EXISTING CONFIGURATION...")
    existing_config = load_existing_config()
    
    # Merge discovered services with existing config
    print("\n🔄 MERGING CONFIGURATIONS...")
    merged_config = merge_services(existing_config, discovered_services)
    
    # Add timestamp
    from datetime import datetime
    for module_data in merged_config.values():
        module_data['last_scanned'] = datetime.now().isoformat()
    
    # Save backup of current config
    if existing_config:
        save_backup(existing_config)
    
    # Save to main file
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(merged_config, f, indent=2, ensure_ascii=False)
        print(f"✅ Service mapping saved: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Failed to save service mapping: {e}")
        return
    
    # Generate and save summary report
    summary_report = generate_summary_report(merged_config)
    summary_file = BACKUP_DIR / "services_discovery_summary.txt"
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_report)
        print(f"📄 Summary report saved: {summary_file}")
    except Exception as e:
        print(f"⚠️  Failed to save summary report: {e}")
    
    print("\n" + "=" * 60)
    print("✅ SERVICE DISCOVERY COMPLETE!")
    print(f"📁 Main Output: {OUTPUT_FILE}")
    print(f"📁 Summary Report: {summary_file}")
    
    # Print summary to console
    total_modules = len(merged_config)
    total_endpoints = sum(mod.get('total_endpoints', 0) for mod in merged_config.values())
    modules_with_endpoints = sum(1 for mod in merged_config.values() if mod.get('total_endpoints', 0) > 0)
    
    print(f"📊 FINAL RESULTS:")
    print(f"   • {total_modules} modules scanned")
    print(f"   • {modules_with_endpoints} modules with endpoints") 
    print(f"   • {total_endpoints} total endpoints discovered")
    
    print("\n💡 NEXT STEPS:")
    print("   1. Run test_all_services.py to test the discovered endpoints")
    print("   2. Review modules_services.json to add frontend mappings")
    print("   3. Use run_service_tests.ps1 for automated testing pipeline")

if __name__ == "__main__":
    main()