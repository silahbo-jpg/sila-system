#!/usr/bin/env python3
"""
Enable Observability CLI Tool for SILA System

This CLI tool enables and manages the complete observability stack including:
- OpenTelemetry tracing
- Prometheus metrics
- Grafana dashboards
- Health monitoring
- Alert configurations

Usage:
    python enable_observability.py --dashboard national
    python enable_observability.py --enable-tracing --jaeger-endpoint http://localhost:14268
    python enable_observability.py --status
"""

import argparse
import subprocess
import os
import sys
import yaml
import json
from pathlib import Path
import time
import requests
from typing import Dict, List, Optional

class ObservabilityManager:
    """Manages the SILA observability stack"""
    
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.monitoring_dir = self.base_dir / "monitoring"
        self.backend_dir = self.base_dir / "backend"
        
    def enable_observability(
        self, 
        dashboard_type: str = "national",
        enable_tracing: bool = True,
        jaeger_endpoint: str = "http://localhost:14268",
        prometheus_port: int = 8001,
        grafana_url: str = "http://localhost:3000"
    ):
        """
        Enable complete observability stack
        
        Args:
            dashboard_type: Type of dashboard (national, municipal, local)
            enable_tracing: Whether to enable OpenTelemetry tracing
            jaeger_endpoint: Jaeger collector endpoint
            prometheus_port: Port for Prometheus metrics
            grafana_url: Grafana dashboard URL
        """
        
        print("🚀 Enabling SILA Observability Stack...")
        
        # Step 1: Validate environment
        self._validate_environment()
        
        # Step 2: Start monitoring infrastructure
        self._start_monitoring_stack()
        
        # Step 3: Configure OpenTelemetry
        if enable_tracing:
            self._configure_tracing(jaeger_endpoint)
            
        # Step 4: Configure Prometheus metrics
        self._configure_metrics(prometheus_port)
        
        # Step 5: Setup Grafana dashboards
        self._setup_grafana_dashboards(dashboard_type, grafana_url)
        
        # Step 6: Configure alerts
        self._configure_alerts()
        
        # Step 7: Validate setup
        self._validate_observability_setup()
        
        print("✅ Observability stack enabled successfully!")
        self._print_access_info()
        
    def _validate_environment(self):
        """Validate that required components are available"""
        print("🔍 Validating environment...")
        
        # Check Docker is available
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            print("  ✓ Docker is available")
        except subprocess.CalledProcessError:
            print("  ❌ Docker is not available. Please install Docker.")
            sys.exit(1)
            
        # Check monitoring directory exists
        if not self.monitoring_dir.exists():
            print("  ❌ Monitoring directory not found. Creating...")
            self.monitoring_dir.mkdir(parents=True, exist_ok=True)
            
        # Check backend directory exists
        if not self.backend_dir.exists():
            print("  ❌ Backend directory not found.")
            sys.exit(1)
            
        print("  ✓ Environment validation passed")
        
    def _start_monitoring_stack(self):
        """Start the monitoring infrastructure using Docker Compose"""
        print("🐳 Starting monitoring stack...")
        
        compose_file = self.monitoring_dir / "docker-compose.monitoring.yml"
        
        if not compose_file.exists():
            print(f"  ❌ Docker Compose file not found: {compose_file}")
            sys.exit(1)
            
        try:
            # Start the monitoring stack
            subprocess.run([
                "docker-compose", 
                "-f", str(compose_file), 
                "up", "-d"
            ], check=True, cwd=self.monitoring_dir)
            
            print("  ✓ Monitoring stack started")
            
            # Wait for services to be ready
            self._wait_for_services()
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to start monitoring stack: {e}")
            sys.exit(1)
            
    def _configure_tracing(self, jaeger_endpoint: str):
        """Configure OpenTelemetry tracing"""
        print("📊 Configuring OpenTelemetry tracing...")
        
        # Create or update configuration
        config = {
            "tracing": {
                "enabled": True,
                "service_name": "sila-system",
                "jaeger_endpoint": jaeger_endpoint,
                "sampling_rate": 0.1
            }
        }
        
        config_file = self.backend_dir / "app" / "core" / "tracing_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
            
        print(f"  ✓ Tracing configuration written to {config_file}")
        
    def _configure_metrics(self, prometheus_port: int):
        """Configure Prometheus metrics collection"""
        print("📈 Configuring Prometheus metrics...")
        
        # Update backend configuration to enable metrics endpoint
        config = {
            "metrics": {
                "enabled": True,
                "port": prometheus_port,
                "path": "/monitoring/metrics/prometheus"
            }
        }
        
        config_file = self.backend_dir / "app" / "core" / "metrics_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config, f)
            
        print(f"  ✓ Metrics configuration written to {config_file}")
        
    def _setup_grafana_dashboards(self, dashboard_type: str, grafana_url: str):
        """Setup Grafana dashboards"""
        print("📊 Setting up Grafana dashboards...")
        
        # Wait for Grafana to be ready
        if not self._wait_for_grafana(grafana_url):
            print("  ❌ Grafana is not ready")
            return
            
        # Import dashboards
        dashboards_dir = self.monitoring_dir / "grafana" / "dashboards"
        dashboard_files = [
            "sila-overview.json",
            "sila-performance.json", 
            "sila-business.json"
        ]
        
        for dashboard_file in dashboard_files:
            dashboard_path = dashboards_dir / dashboard_file
            if dashboard_path.exists():
                self._import_grafana_dashboard(grafana_url, dashboard_path)
            else:
                print(f"  ⚠️  Dashboard file not found: {dashboard_file}")
                
        print(f"  ✓ Grafana dashboards configured for {dashboard_type} deployment")
        
    def _configure_alerts(self):
        """Configure alerting rules"""
        print("🚨 Configuring alerts...")
        
        # Reload Prometheus configuration
        try:
            response = requests.post("http://localhost:9090/-/reload")
            if response.status_code == 200:
                print("  ✓ Prometheus configuration reloaded")
            else:
                print(f"  ⚠️  Failed to reload Prometheus: {response.status_code}")
        except requests.exceptions.RequestException:
            print("  ⚠️  Prometheus not accessible for configuration reload")
            
    def _validate_observability_setup(self):
        """Validate that observability components are working"""
        print("🔍 Validating observability setup...")
        
        validations = [
            ("Prometheus", "http://localhost:9090/-/healthy", "Prometheus is healthy"),
            ("Grafana", "http://localhost:3000/api/health", "Grafana is accessible"),
            ("Jaeger", "http://localhost:16686", "Jaeger UI is accessible"),
            ("AlertManager", "http://localhost:9093/-/healthy", "AlertManager is healthy")
        ]
        
        for name, url, description in validations:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"  ✓ {description}")
                else:
                    print(f"  ⚠️  {name} returned status {response.status_code}")
            except requests.exceptions.RequestException:
                print(f"  ❌ {name} is not accessible at {url}")
                
    def _wait_for_services(self):
        """Wait for monitoring services to be ready"""
        print("  ⏳ Waiting for services to be ready...")
        time.sleep(30)  # Give services time to start
        
    def _wait_for_grafana(self, grafana_url: str, timeout: int = 120) -> bool:
        """Wait for Grafana to be ready"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{grafana_url}/api/health", timeout=5)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(5)
        return False
        
    def _import_grafana_dashboard(self, grafana_url: str, dashboard_path: Path):
        """Import a dashboard into Grafana"""
        try:
            with open(dashboard_path, 'r') as f:
                dashboard_json = json.load(f)
                
            # Prepare dashboard for import
            import_data = {
                "dashboard": dashboard_json["dashboard"],
                "overwrite": True,
                "inputs": []
            }
            
            # Import dashboard via Grafana API
            response = requests.post(
                f"{grafana_url}/api/dashboards/import",
                json=import_data,
                auth=('admin', 'admin123'),  # Default credentials
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"  ✓ Dashboard imported: {dashboard_path.name}")
            else:
                print(f"  ⚠️  Failed to import dashboard {dashboard_path.name}: {response.text}")
                
        except Exception as e:
            print(f"  ❌ Error importing dashboard {dashboard_path.name}: {e}")
            
    def _print_access_info(self):
        """Print access information for monitoring services"""
        print("\n🎯 Access Information:")
        print("  📊 Grafana Dashboard: http://localhost:3000 (admin/admin123)")
        print("  📈 Prometheus: http://localhost:9090")
        print("  🔍 Jaeger Tracing: http://localhost:16686")
        print("  🚨 AlertManager: http://localhost:9093")
        print("  📊 SILA Metrics: http://localhost:8001/monitoring/metrics/prometheus")
        print("  ❤️  Health Checks: http://localhost:8000/monitoring/health/")
        
    def get_status(self):
        """Get status of observability components"""
        print("📊 SILA Observability Stack Status:")
        
        services = [
            ("Prometheus", "http://localhost:9090/-/healthy"),
            ("Grafana", "http://localhost:3000/api/health"), 
            ("Jaeger", "http://localhost:16686"),
            ("AlertManager", "http://localhost:9093/-/healthy"),
            ("SILA Backend", "http://localhost:8000/monitoring/health/")
        ]
        
        for name, url in services:
            try:
                response = requests.get(url, timeout=5)
                status = "🟢 Running" if response.status_code == 200 else f"🟡 Issues ({response.status_code})"
            except requests.exceptions.RequestException:
                status = "🔴 Not Accessible"
                
            print(f"  {name}: {status}")
            
    def stop_observability(self):
        """Stop the observability stack"""
        print("🛑 Stopping observability stack...")
        
        compose_file = self.monitoring_dir / "docker-compose.monitoring.yml"
        
        try:
            subprocess.run([
                "docker-compose",
                "-f", str(compose_file),
                "down"
            ], check=True, cwd=self.monitoring_dir)
            
            print("✅ Observability stack stopped")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to stop observability stack: {e}")

def main():
    parser = argparse.ArgumentParser(description="SILA Observability Stack Manager")
    
    parser.add_argument(
        "--dashboard", 
        choices=["national", "municipal", "local"], 
        default="national",
        help="Type of dashboard deployment"
    )
    
    parser.add_argument(
        "--enable-tracing",
        action="store_true",
        help="Enable OpenTelemetry tracing"
    )
    
    parser.add_argument(
        "--jaeger-endpoint",
        default="http://localhost:14268",
        help="Jaeger collector endpoint"
    )
    
    parser.add_argument(
        "--prometheus-port",
        type=int,
        default=8001,
        help="Port for Prometheus metrics"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Check status of observability components"
    )
    
    parser.add_argument(
        "--stop",
        action="store_true",
        help="Stop the observability stack"
    )
    
    args = parser.parse_args()
    
    manager = ObservabilityManager()
    
    if args.status:
        manager.get_status()
    elif args.stop:
        manager.stop_observability()
    else:
        manager.enable_observability(
            dashboard_type=args.dashboard,
            enable_tracing=args.enable_tracing,
            jaeger_endpoint=args.jaeger_endpoint,
            prometheus_port=args.prometheus_port
        )

if __name__ == "__main__":
    main()