#!/usr/bin/env python3
"""
Approval Level Configuration CLI

This script manages approval configurations for SILA services as specified in the directive.
Allows setting approval levels for services and configuring approver hierarchies.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.workflow import ApprovalWorkflowManager, ServiceApprovalConfig

class ApprovalLevelManager:
    """Manages service approval level configurations"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.workflow_manager = ApprovalWorkflowManager(self.db)
        
    def set_service_approval(
        self,
        module: str,
        service: str,
        levels: List[Dict[str, Any]],
        conditions: Dict[str, Any] = None,
        timeout: int = 48
    ) -> bool:
        """
        Set approval configuration for a service
        
        Args:
            module: Module name (e.g., 'finance', 'citizenship')
            service: Service name (e.g., 'PagamentoTaxa')
            levels: List of approval level configurations
            conditions: When approval is required
            timeout: Default timeout in hours
        """
        print(f"🔧 Setting approval levels for {module}.{service}")
        
        try:
            # Convert service name to endpoint path
            service_slug = ''.join(['_'+c.lower() if c.isupper() else c for c in service]).lstrip('_')
            endpoint_path = f"/api/{service_slug.replace('_', '-')}"
            
            # Configure approval
            config = self.workflow_manager.configure_service_approval(
                module_name=module,
                service_name=service,
                endpoint_path=endpoint_path,
                approval_levels=levels,
                conditions=conditions,
                timeout_hours=timeout
            )
            
            print(f"✅ Configured {len(levels)} approval levels")
            for i, level in enumerate(levels, 1):
                level_name = level['level']
                approvers = level.get('approver_ids', [])
                roles = level.get('approver_roles', [])
                print(f"   Level {i} ({level_name}): {len(approvers)} direct approvers, {len(roles)} roles")
                
            return True
            
        except Exception as e:
            print(f"❌ Error setting approval levels: {str(e)}")
            return False
            
    def list_approval_configs(self) -> List[ServiceApprovalConfig]:
        """List all services with approval configurations"""
        
        configs = self.db.query(ServiceApprovalConfig).filter(
            ServiceApprovalConfig.requires_approval == True
        ).order_by(ServiceApprovalConfig.module_name, ServiceApprovalConfig.service_name).all()
        
        print(f"📋 Services with Approval Requirements ({len(configs)}):")
        print("=" * 80)
        
        current_module = None
        for config in configs:
            if config.module_name != current_module:
                current_module = config.module_name
                print(f"\n🏛️ {current_module.upper()} MODULE:")
                
            levels_count = len(config.approval_levels) if config.approval_levels else 0
            timeout = config.default_timeout_hours
            
            print(f"   📋 {config.service_name}")
            print(f"      Endpoint: {config.endpoint_path}")
            print(f"      Levels: {levels_count}")
            print(f"      Timeout: {timeout}h")
            
            if config.approval_levels:
                for level in config.approval_levels:
                    level_name = level['level']
                    required = "Required" if level.get('required', True) else "Conditional"
                    print(f"      - {level_name}: {required}")
                    
        return configs
        
    def remove_approval(self, module: str, service: str) -> bool:
        """Remove approval requirement from a service"""
        
        print(f"🗑️ Removing approval requirement for {module}.{service}")
        
        try:
            config = self.db.query(ServiceApprovalConfig).filter(
                ServiceApprovalConfig.module_name == module,
                ServiceApprovalConfig.service_name == service
            ).first()
            
            if not config:
                print(f"⚠️ No approval configuration found for {module}.{service}")
                return False
                
            config.requires_approval = False
            self.db.commit()
            
            print(f"✅ Removed approval requirement for {service}")
            return True
            
        except Exception as e:
            print(f"❌ Error removing approval: {str(e)}")
            return False
            
    def create_preset_configurations(self):
        """Create preset approval configurations for common sensitive services"""
        
        print("🏗️ Creating preset approval configurations for sensitive services...")
        
        # High-value financial services (Level 2 approval)
        financial_services = [
            {
                "module": "finance",
                "service": "MicroCredito",
                "levels": [
                    {
                        "level": "level_1",
                        "approver_roles": ["financial_supervisor"],
                        "required": True,
                        "timeout_hours": 24
                    },
                    {
                        "level": "level_2", 
                        "approver_roles": ["financial_manager"],
                        "required_for": {"amount": {"gt": 50000}},  # > 50,000 AOA
                        "timeout_hours": 48
                    }
                ],
                "conditions": {"amount": {"gt": 10000}},  # Only require approval for > 10,000 AOA
                "timeout": 48
            }
        ]
        
        # Citizenship document services (Level 1 approval)
        citizenship_services = [
            {
                "module": "citizenship",
                "service": "EmissaoPassaporte",
                "levels": [
                    {
                        "level": "level_1",
                        "approver_roles": ["citizenship_supervisor"],
                        "required": True,
                        "timeout_hours": 48
                    }
                ],
                "timeout": 72
            }
        ]
        
        # Commercial licensing (Level 3 approval for large businesses)
        commercial_services = [
            {
                "module": "commercial",
                "service": "LicencaIndustrial",
                "levels": [
                    {
                        "level": "level_1",
                        "approver_roles": ["commercial_supervisor"],
                        "required": True,
                        "timeout_hours": 24
                    },
                    {
                        "level": "level_2",
                        "approver_roles": ["commercial_manager"],
                        "required": True,
                        "timeout_hours": 48
                    },
                    {
                        "level": "level_3",
                        "approver_roles": ["municipal_director"],
                        "required_for": {"business_type": {"eq": "industrial"}},
                        "timeout_hours": 72
                    }
                ],
                "timeout": 120
            }
        ]
        
        # Urban planning (Level 2 approval for construction)
        urban_services = [
            {
                "module": "urbanism", 
                "service": "LicencaConstrucao",
                "levels": [
                    {
                        "level": "level_1",
                        "approver_roles": ["urban_planner"],
                        "required": True,
                        "timeout_hours": 48
                    },
                    {
                        "level": "level_2",
                        "approver_roles": ["urban_director"],
                        "required_for": {"construction_area": {"gt": 500}},  # > 500 m²
                        "timeout_hours": 72
                    }
                ],
                "conditions": {"construction_area": {"gt": 100}},  # Only for > 100 m²
                "timeout": 96
            }
        ]
        
        # Combine all preset configurations
        all_presets = financial_services + citizenship_services + commercial_services + urban_services
        
        success_count = 0
        for preset in all_presets:
            try:
                if self.set_service_approval(**preset):
                    success_count += 1
            except Exception as e:
                print(f"❌ Error creating preset for {preset['module']}.{preset['service']}: {str(e)}")
                
        print(f"✅ Created {success_count}/{len(all_presets)} preset approval configurations")
        
    def generate_approval_report(self):
        """Generate comprehensive approval configuration report"""
        
        print("📊 Generating Approval Configuration Report...")
        print("=" * 60)
        
        # Get metrics from workflow manager
        metrics = self.workflow_manager.get_approval_metrics()
        
        print("📈 APPROVAL METRICS:")
        print(f"   Total Requests: {metrics['total_requests']}")
        print(f"   Pending Requests: {metrics['pending_requests']}")
        print(f"   Services Requiring Approval: {metrics['services_requiring_approval_percentage']}%")
        print(f"   Average Approval Time: {metrics['average_approval_time_hours']} hours")
        print(f"   Overall Approval Rate: {metrics['approval_rate']}%")
        
        print("\n📋 STATUS BREAKDOWN:")
        for status, count in metrics['status_breakdown'].items():
            percentage = (count / metrics['total_requests'] * 100) if metrics['total_requests'] > 0 else 0
            print(f"   {status.title()}: {count} ({percentage:.1f}%)")
            
        # Configuration summary
        configs = self.db.query(ServiceApprovalConfig).all()
        
        print(f"\n🔧 CONFIGURATION SUMMARY:")
        print(f"   Total Services with Config: {len(configs)}")
        
        active_configs = [c for c in configs if c.requires_approval]
        print(f"   Active Approval Requirements: {len(active_configs)}")
        
        # Group by module
        module_counts = {}
        for config in active_configs:
            module_counts[config.module_name] = module_counts.get(config.module_name, 0) + 1
            
        print("\n📦 BY MODULE:")
        for module, count in sorted(module_counts.items()):
            print(f"   {module}: {count} services")
            
        # Level analysis
        level_usage = {"level_1": 0, "level_2": 0, "level_3": 0, "level_4": 0}
        for config in active_configs:
            if config.approval_levels:
                for level in config.approval_levels:
                    level_name = level.get('level')
                    if level_name in level_usage:
                        level_usage[level_name] += 1
                        
        print("\n🏛️ APPROVAL LEVEL USAGE:")
        for level, count in level_usage.items():
            print(f"   {level.replace('_', ' ').title()}: {count} services")
            
    def test_approval_flow(self, module: str, service: str, test_data: Dict[str, Any]):
        """Test approval flow for a service with sample data"""
        
        print(f"🧪 Testing approval flow for {module}.{service}")
        
        try:
            # Create a test approval request
            approval_requests = self.workflow_manager.request_approval(
                service_request_id=f"TEST_{module}_{service}_001",
                module_name=module,
                service_name=service,
                requester_id=99999,  # Test user ID
                request_data=test_data,
                justification="Testing approval flow"
            )
            
            if not approval_requests:
                print("✅ No approval required for this request")
                return True
                
            print(f"📋 Created {len(approval_requests)} approval requests:")
            
            for req in approval_requests:
                print(f"   🎫 ID: {req.id}")
                print(f"      Level: {req.approval_level.value}")
                print(f"      Status: {req.status.value}")
                print(f"      Approver: {req.current_approver_id}")
                print(f"      Due: {req.due_date.strftime('%Y-%m-%d %H:%M') if req.due_date else 'No deadline'}")
                
            print(f"\n💡 This is a test - approvals created but not executed")
            print(f"   Use the web interface or API to complete approvals")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description="SILA Approval Level Management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Set approval level
    set_parser = subparsers.add_parser('set', help='Set approval levels for a service')
    set_parser.add_argument('module', help='Module name')
    set_parser.add_argument('service', help='Service name')
    set_parser.add_argument('--config', required=True, help='JSON file with approval configuration')
    
    # List configurations
    list_parser = subparsers.add_parser('list', help='List all approval configurations')
    
    # Remove approval
    remove_parser = subparsers.add_parser('remove', help='Remove approval requirement')
    remove_parser.add_argument('module', help='Module name')
    remove_parser.add_argument('service', help='Service name')
    
    # Create presets
    preset_parser = subparsers.add_parser('create-presets', help='Create preset approval configurations')
    
    # Generate report
    report_parser = subparsers.add_parser('report', help='Generate approval configuration report')
    
    # Test approval flow
    test_parser = subparsers.add_parser('test', help='Test approval flow for a service')
    test_parser.add_argument('module', help='Module name')
    test_parser.add_argument('service', help='Service name')
    test_parser.add_argument('--data', required=True, help='JSON file with test data')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    manager = ApprovalLevelManager()
    
    try:
        if args.command == 'set':
            config_file = Path(args.config)
            if not config_file.exists():
                print(f"❌ Configuration file not found: {config_file}")
                sys.exit(1)
                
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            success = manager.set_service_approval(
                args.module,
                args.service,
                config['levels'],
                config.get('conditions'),
                config.get('timeout', 48)
            )
            sys.exit(0 if success else 1)
            
        elif args.command == 'list':
            manager.list_approval_configs()
            
        elif args.command == 'remove':
            success = manager.remove_approval(args.module, args.service)
            sys.exit(0 if success else 1)
            
        elif args.command == 'create-presets':
            manager.create_preset_configurations()
            
        elif args.command == 'report':
            manager.generate_approval_report()
            
        elif args.command == 'test':
            data_file = Path(args.data)
            if not data_file.exists():
                print(f"❌ Test data file not found: {data_file}")
                sys.exit(1)
                
            with open(data_file, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
                
            success = manager.test_approval_flow(args.module, args.service, test_data)
            sys.exit(0 if success else 1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
    finally:
        manager.db.close()

if __name__ == "__main__":
    main()