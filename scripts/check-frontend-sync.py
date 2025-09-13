#!/usr/bin/env python3
"""
Frontend-Backend Synchronization Diagnostic Script

This script verifies that the backend services are properly synchronized 
with the frontend, ensuring all services are accessible and properly translated.

Based on the specifications from truman_try.txt for automated verification.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import httpx
from pydantic import BaseModel


class ServiceCheck(BaseModel):
    """Result of a service check"""
    service_id: str
    name: str
    accessible: bool = False
    has_translations: bool = False
    has_route: bool = False
    errors: List[str] = []


class SyncReport(BaseModel):
    """Complete synchronization report"""
    total_services: int
    accessible_services: int
    translated_services: int
    routed_services: int
    errors: List[str] = []
    service_checks: List[ServiceCheck] = []
    success_rate: float = 0.0


class FrontendSyncChecker:
    """Main checker class for frontend-backend synchronization"""
    
    def __init__(self, backend_url: str = "http://localhost:8000", frontend_path: Optional[str] = None):
        self.backend_url = backend_url.rstrip('/')
        self.frontend_path = Path(frontend_path) if frontend_path else Path(__file__).parent.parent / "frontend"
        self.locale_path = self.frontend_path / "src" / "locales"
        self.routes_path = self.frontend_path / "src" / "routes"
        
    async def check_backend_health(self) -> bool:
        """Check if backend is running and accessible"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/ping", timeout=5.0)
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Backend health check failed: {e}")
            return False
    
    async def fetch_services(self) -> List[Dict[str, Any]]:
        """Fetch all services from the backend API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/api/services", timeout=10.0)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("services", [])
                else:
                    print(f"❌ Failed to fetch services: HTTP {response.status_code}")
                    return []
        except Exception as e:
            print(f"❌ Error fetching services: {e}")
            return []
    
    def load_translations(self, language: str) -> Dict[str, Any]:
        """Load translation file for a specific language"""
        translation_file = self.locale_path / f"{language}.json"
        if translation_file.exists():
            try:
                with open(translation_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error loading {language} translations: {e}")
        return {}
    
    def check_service_translation(self, service_id: str, service_name: str) -> bool:
        """Check if service has translations in both languages"""
        en_translations = self.load_translations("en")
        pt_translations = self.load_translations("pt")
        
        # Check various possible translation keys
        possible_keys = [
            f"services.{service_id}",
            f"services.{service_id}.name",
            f"service.{service_id}",
            service_name.lower().replace(" ", "_")
        ]
        
        en_found = any(key in en_translations for key in possible_keys)
        pt_found = any(key in pt_translations for key in possible_keys)
        
        return en_found and pt_found
    
    def check_service_route(self, service_id: str) -> bool:
        """Check if service has a corresponding route in the frontend"""
        if not self.routes_path.exists():
            return False
            
        # Look for route files that might correspond to this service
        route_patterns = [
            f"{service_id}.tsx",
            f"{service_id}.jsx",
            f"{service_id}/index.tsx",
            f"{service_id}/index.jsx",
            f"{service_id.replace('_', '-')}.tsx",
            f"{service_id.replace('_', '-')}.jsx",
        ]
        
        for pattern in route_patterns:
            if (self.routes_path / pattern).exists():
                return True
                
        # Also check in subdirectories
        for subdir in self.routes_path.iterdir():
            if subdir.is_dir():
                for pattern in route_patterns:
                    if (subdir / pattern).exists():
                        return True
                        
        return False
    
    async def check_role_based_visibility(self) -> bool:
        """Check if role-based service visibility is working correctly"""
        try:
            # Test different role endpoints
            role_tests = [
                ("citizen", "?role=citizen"),
                ("staff", "?role=staff"),
                ("admin", "?role=admin")
            ]
            
            async with httpx.AsyncClient() as client:
                for role_name, query_param in role_tests:
                    try:
                        response = await client.get(
                            f"{self.backend_url}/api/services{query_param}", 
                            timeout=5.0
                        )
                        if response.status_code == 200:
                            data = response.json()
                            services_count = len(data.get("services", []))
                            print(f"✅ Role '{role_name}' can access {services_count} services")
                        else:
                            print(f"⚠️ Role '{role_name}' test failed: HTTP {response.status_code}")
                    except Exception as e:
                        print(f"❌ Role '{role_name}' test error: {e}")
                        
                # Test user permissions endpoint
                try:
                    response = await client.get(f"{self.backend_url}/api/services/user/permissions")
                    if response.status_code == 200:
                        print("✅ User permissions endpoint accessible")
                        return True
                    else:
                        print(f"⚠️ User permissions endpoint failed: HTTP {response.status_code}")
                except Exception as e:
                    print(f"❌ User permissions endpoint error: {e}")
                        
        except Exception as e:
            print(f"❌ Role-based visibility check failed: {e}")
            
        return False
    
    async def check_service_accessibility(self, service: Dict[str, Any]) -> bool:
        """Check if service endpoint is accessible"""
        api_endpoint = service.get("api_endpoint", "")
        if not api_endpoint:
            return False
            
        try:
            # Remove /api prefix if present since we'll add the full URL
            endpoint = api_endpoint.replace("/api", "")
            full_url = f"{self.backend_url}/api{endpoint}"
            
            async with httpx.AsyncClient() as client:
                # Try different HTTP methods that might be supported
                for method in ["GET", "POST"]:
                    try:
                        response = await client.request(method, full_url, timeout=5.0)
                        # Consider it accessible if we get anything other than 404
                        if response.status_code != 404:
                            return True
                    except httpx.HTTPStatusError:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Error checking accessibility for {service.get('id', 'unknown')}: {e}")
            
        return False
        """Check if service endpoint is accessible"""
        api_endpoint = service.get("api_endpoint", "")
        if not api_endpoint:
            return False
            
        try:
            # Remove /api prefix if present since we'll add the full URL
            endpoint = api_endpoint.replace("/api", "")
            full_url = f"{self.backend_url}/api{endpoint}"
            
            async with httpx.AsyncClient() as client:
                # Try different HTTP methods that might be supported
                for method in ["GET", "POST"]:
                    try:
                        response = await client.request(method, full_url, timeout=5.0)
                        # Consider it accessible if we get anything other than 404
                        if response.status_code != 404:
                            return True
                    except httpx.HTTPStatusError:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Error checking accessibility for {service.get('id', 'unknown')}: {e}")
            
        return False
    
    async def check_individual_service(self, service: Dict[str, Any]) -> ServiceCheck:
        """Perform comprehensive check on a single service"""
        service_id = service.get("id", "")
        service_name = service.get("name", "")
        
        check = ServiceCheck(
            service_id=service_id,
            name=service_name
        )
        
        # Check accessibility
        check.accessible = await self.check_service_accessibility(service)
        if not check.accessible:
            check.errors.append("Service endpoint not accessible")
        
        # Check translations
        check.has_translations = self.check_service_translation(service_id, service_name)
        if not check.has_translations:
            check.errors.append("Missing translations in en.json or pt.json")
        
        # Check routes
        check.has_route = self.check_service_route(service_id)
        if not check.has_route:
            check.errors.append("No corresponding frontend route found")
        
        return check
    
    async def run_full_check(self, verbose: bool = False) -> SyncReport:
        """Run the complete synchronization check"""
        print("🔍 Starting Frontend-Backend Synchronization Check...")
        print(f"Backend URL: {self.backend_url}")
        print(f"Frontend Path: {self.frontend_path}")
        print()
        
        report = SyncReport(
            total_services=0,
            accessible_services=0,
            translated_services=0,
            routed_services=0
        )
        
        # Check backend health first
        if not await self.check_backend_health():
            report.errors.append("Backend is not accessible")
            return report
            
        print("✅ Backend is accessible")
        
        # Fetch services
        services = await self.fetch_services()
        if not services:
            report.errors.append("No services found or unable to fetch services")
            return report
            
        print(f"📊 Found {len(services)} services to check")
        report.total_services = len(services)
        
        # Check each service
        for i, service in enumerate(services, 1):
            service_id = service.get("id", f"service_{i}")
            if verbose:
                print(f"🔍 Checking service {i}/{len(services)}: {service_id}")
                
            check = await self.check_individual_service(service)
            report.service_checks.append(check)
            
            # Update counters
            if check.accessible:
                report.accessible_services += 1
            if check.has_translations:
                report.translated_services += 1
            if check.has_route:
                report.routed_services += 1
                
            if verbose and check.errors:
                for error in check.errors:
                    print(f"  ⚠️ {error}")
        
        # Calculate success rate
        if report.total_services > 0:
            fully_synced = sum(
                1 for check in report.service_checks 
                if check.accessible and check.has_translations and check.has_route
            )
            report.success_rate = (fully_synced / report.total_services) * 100
        
        return report
    
    def print_report(self, report: SyncReport):
        """Print the synchronization report"""
        print("\n" + "="*80)
        print("📋 FRONTEND-BACKEND SYNCHRONIZATION REPORT")
        print("="*80)
        
        print(f"📊 Total Services: {report.total_services}")
        print(f"🌐 Accessible Services: {report.accessible_services}/{report.total_services}")
        print(f"🌍 Translated Services: {report.translated_services}/{report.total_services}")
        print(f"🛣️ Routed Services: {report.routed_services}/{report.total_services}")
        print(f"✅ Success Rate: {report.success_rate:.1f}%")
        
        if report.errors:
            print("\n❌ Global Errors:")
            for error in report.errors:
                print(f"  • {error}")
        
        # Group services by status
        fully_synced = []
        partially_synced = []
        not_synced = []
        
        for check in report.service_checks:
            if check.accessible and check.has_translations and check.has_route:
                fully_synced.append(check)
            elif check.accessible or check.has_translations or check.has_route:
                partially_synced.append(check)
            else:
                not_synced.append(check)
        
        if fully_synced:
            print(f"\n✅ Fully Synchronized Services ({len(fully_synced)}):")
            for check in fully_synced:
                print(f"  • {check.service_id}: {check.name}")
        
        if partially_synced:
            print(f"\n⚠️ Partially Synchronized Services ({len(partially_synced)}):")
            for check in partially_synced:
                status = []
                if check.accessible:
                    status.append("✓ Accessible")
                if check.has_translations:
                    status.append("✓ Translated")
                if check.has_route:
                    status.append("✓ Routed")
                print(f"  • {check.service_id}: {check.name} ({', '.join(status)})")
                if check.errors:
                    for error in check.errors:
                        print(f"    ❌ {error}")
        
        if not_synced:
            print(f"\n❌ Not Synchronized Services ({len(not_synced)}):")
            for check in not_synced:
                print(f"  • {check.service_id}: {check.name}")
                for error in check.errors:
                    print(f"    ❌ {error}")
        
        print("\n" + "="*80)
        
        # Overall status
        if report.success_rate >= 90:
            print("🎉 EXCELLENT: Frontend and backend are well synchronized!")
        elif report.success_rate >= 70:
            print("👍 GOOD: Most services are synchronized, minor issues to fix.")
        elif report.success_rate >= 50:
            print("⚠️ ATTENTION: Several synchronization issues need to be addressed.")
        else:
            print("🚨 CRITICAL: Major synchronization problems detected!")


async def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Check frontend-backend synchronization for SILA system"
    )
    parser.add_argument(
        "--backend-url",
        default="http://localhost:8000",
        help="Backend URL (default: http://localhost:8000)"
    )
    parser.add_argument(
        "--frontend-path",
        help="Path to frontend directory (default: ../frontend)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--output",
        help="Save report to JSON file"
    )
    
    args = parser.parse_args()
    
    # Create checker
    checker = FrontendSyncChecker(
        backend_url=args.backend_url,
        frontend_path=args.frontend_path
    )
    
    # Run check
    try:
        report = await checker.run_full_check(verbose=args.verbose)
        checker.print_report(report)
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report.dict(), f, indent=2, ensure_ascii=False)
            print(f"\n💾 Report saved to {args.output}")
        
        # Exit with appropriate code
        sys.exit(0 if report.success_rate >= 70 else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())