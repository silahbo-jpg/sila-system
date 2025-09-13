#!/usr/bin/env python3
"""
Batch Update System for SILA Services

This script provides mass update capabilities with rollback protection as specified in the directive:
- Operate directly over service metadata (services_metadata table)
- Allow filtering by module, field, condition
- Guarantee rollback automation if failures occur
- Support operations like: batch-update finance --field fee --increase 10%

Example usage:
python batch_update.py finance --field fee --increase 10%
python batch_update.py health --field timeout --set 30
python batch_update.py all --field active --set true --condition "created_at > '2024-01-01'"
"""

import sys
import json
import argparse
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
import re

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Text, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class ServiceMetadata(Base):
    """
    Service metadata table for batch operations
    This table stores metadata for all SILA services that can be batch updated
    """
    __tablename__ = "services_metadata"

    id = Column(Integer, primary_key=True, index=True)
    
    # Service identification
    module_name = Column(String(100), nullable=False)
    service_name = Column(String(100), nullable=False)
    service_key = Column(String(100), nullable=False)
    endpoint_path = Column(String(200), nullable=False)
    
    # Service configuration (updatable fields)
    active = Column(Boolean, default=True)
    timeout_seconds = Column(Integer, default=30)
    max_retries = Column(Integer, default=3)
    rate_limit_per_minute = Column(Integer, default=60)
    
    # Financial configurations
    fee_amount = Column(Integer, default=0)  # In AOA cents
    fee_currency = Column(String(3), default="AOA")
    
    # Operational settings
    requires_approval = Column(Boolean, default=False)
    approval_timeout_hours = Column(Integer, default=48)
    auto_execute = Column(Boolean, default=True)
    
    # Feature flags
    feature_flags = Column(JSON)  # Flexible feature configuration
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_batch_update = Column(DateTime)
    
    # Version tracking for rollbacks
    version = Column(Integer, default=1)
    
    # Custom properties (JSON)
    custom_properties = Column(JSON)

class BatchUpdateLog(Base):
    """
    Log of batch update operations for audit and rollback
    """
    __tablename__ = "batch_update_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Operation identification
    operation_id = Column(String(50), nullable=False, index=True)
    operation_type = Column(String(50), nullable=False)  # update, rollback, etc.
    
    # Target specification
    target_module = Column(String(100))
    target_services = Column(JSON)  # List of affected service IDs
    filter_conditions = Column(JSON)  # Original filter conditions
    
    # Operation details
    field_name = Column(String(100))
    operation = Column(String(50))  # set, increase, decrease, multiply, etc.
    old_values = Column(JSON)  # Before values for rollback
    new_values = Column(JSON)  # After values
    
    # Execution details
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    status = Column(String(20), default="running")  # running, completed, failed, rolled_back
    
    # Error handling
    error_message = Column(Text)
    affected_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    
    # Rollback information
    can_rollback = Column(Boolean, default=True)
    rollback_operation_id = Column(String(50))  # Links to rollback operation
    
    # Audit
    executed_by = Column(String(100))
    execution_context = Column(JSON)

@dataclass
class BatchOperation:
    """Represents a batch update operation"""
    operation_id: str
    target_module: str
    field_name: str
    operation: str  # set, increase, decrease, multiply, etc.
    value: Union[str, int, float, bool]
    filter_conditions: Dict[str, Any]
    dry_run: bool = False

class BatchUpdateManager:
    """
    Manages batch update operations with rollback protection
    
    Key features:
    - Transaction-based operations
    - Automatic rollback on failures
    - Detailed logging and audit trail
    - Flexible filtering and conditions
    """
    
    def __init__(self, database_url: str = "postgresql://sila_user:sila_password@localhost:5432/sila_db"):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def execute_batch_update(self, operation: BatchOperation) -> Dict[str, Any]:
        """
        Execute a batch update operation with full rollback protection
        
        Args:
            operation: BatchOperation configuration
            
        Returns:
            Results including affected count, success status, rollback info
        """
        
        db = self.SessionLocal()
        operation_start = datetime.now()
        
        try:
            logger.info(f"Starting batch operation: {operation.operation_id}")
            
            # Create operation log
            log_entry = BatchUpdateLog(
                operation_id=operation.operation_id,
                operation_type="batch_update",
                target_module=operation.target_module,
                field_name=operation.field_name,
                operation=operation.operation,
                filter_conditions=operation.filter_conditions,
                executed_by="batch_script"
            )
            db.add(log_entry)
            db.flush()
            
            # Get target services with filtering
            target_services = self._get_filtered_services(db, operation)
            
            if not target_services:
                logger.warning("No services match the filter criteria")
                log_entry.status = "completed"
                log_entry.completed_at = datetime.now()
                log_entry.affected_count = 0
                db.commit()
                return {
                    "success": True,
                    "affected_count": 0,
                    "message": "No services matched filter criteria"
                }
            
            logger.info(f"Found {len(target_services)} services to update")
            
            # Store old values for rollback
            old_values = {}
            for service in target_services:
                old_values[service.id] = {
                    "field": operation.field_name,
                    "old_value": getattr(service, operation.field_name, None),
                    "version": service.version
                }
            
            # Execute updates in transaction
            if operation.dry_run:
                logger.info("DRY RUN MODE - No actual changes will be made")
                new_values = self._simulate_updates(target_services, operation)
                
                db.rollback()  # Rollback dry run transaction
                
                return {
                    "success": True,
                    "dry_run": True,
                    "affected_count": len(target_services),
                    "preview": new_values,
                    "message": "Dry run completed - no changes made"
                }
            else:
                # Actual update execution
                new_values = {}
                failed_updates = []
                
                for service in target_services:
                    try:
                        old_value = getattr(service, operation.field_name)
                        new_value = self._calculate_new_value(old_value, operation)
                        
                        setattr(service, operation.field_name, new_value)
                        service.version += 1
                        service.last_batch_update = operation_start
                        service.updated_at = operation_start
                        
                        new_values[service.id] = {
                            "service_name": service.service_name,
                            "old_value": old_value,
                            "new_value": new_value
                        }
                        
                        db.flush()  # Check for constraint violations
                        
                    except Exception as e:
                        failed_updates.append({
                            "service_id": service.id,
                            "service_name": service.service_name,
                            "error": str(e)
                        })
                        logger.error(f"Failed to update {service.service_name}: {str(e)}")
                
                # Check if any updates failed
                if failed_updates:
                    logger.error(f"{len(failed_updates)} updates failed - rolling back transaction")
                    db.rollback()
                    
                    # Log the failure
                    log_entry.status = "failed"
                    log_entry.error_message = f"{len(failed_updates)} services failed to update"
                    log_entry.failed_count = len(failed_updates)
                    log_entry.completed_at = datetime.now()
                    
                    # Create new session for logging (previous was rolled back)
                    log_db = self.SessionLocal()
                    log_db.merge(log_entry)
                    log_db.commit()
                    log_db.close()
                    
                    return {
                        "success": False,
                        "error": "Some updates failed - transaction rolled back",
                        "failed_updates": failed_updates,
                        "rollback_performed": True
                    }
                
                # All updates successful - commit transaction
                log_entry.status = "completed"
                log_entry.completed_at = datetime.now()
                log_entry.affected_count = len(target_services)
                log_entry.old_values = old_values
                log_entry.new_values = new_values
                log_entry.target_services = [s.id for s in target_services]
                
                db.commit()
                
                logger.info(f"Batch update completed successfully: {len(target_services)} services updated")
                
                return {
                    "success": True,
                    "operation_id": operation.operation_id,
                    "affected_count": len(target_services),
                    "updated_services": new_values,
                    "can_rollback": True,
                    "message": f"Successfully updated {len(target_services)} services"
                }
                
        except Exception as e:
            logger.error(f"Batch update failed: {str(e)}")
            logger.error(traceback.format_exc())
            
            db.rollback()
            
            # Log the error
            log_entry.status = "failed"
            log_entry.error_message = str(e)
            log_entry.completed_at = datetime.now()
            
            # Create new session for error logging
            log_db = self.SessionLocal()
            log_db.merge(log_entry)
            log_db.commit()
            log_db.close()
            
            return {
                "success": False,
                "error": str(e),
                "rollback_performed": True
            }
        finally:
            db.close()
            
    def rollback_operation(self, operation_id: str) -> Dict[str, Any]:
        """
        Rollback a previously executed batch operation
        
        Args:
            operation_id: ID of operation to rollback
            
        Returns:
            Rollback results
        """
        
        db = self.SessionLocal()
        rollback_start = datetime.now()
        
        try:
            # Find the original operation
            original_log = db.query(BatchUpdateLog).filter(
                BatchUpdateLog.operation_id == operation_id,
                BatchUpdateLog.status == "completed"
            ).first()
            
            if not original_log:
                return {
                    "success": False,
                    "error": f"Operation {operation_id} not found or cannot be rolled back"
                }
                
            if not original_log.can_rollback:
                return {
                    "success": False,
                    "error": f"Operation {operation_id} is marked as non-rollbackable"
                }
                
            logger.info(f"Rolling back operation: {operation_id}")
            
            # Create rollback log entry
            rollback_id = f"{operation_id}_ROLLBACK_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            rollback_log = BatchUpdateLog(
                operation_id=rollback_id,
                operation_type="rollback",
                target_module=original_log.target_module,
                field_name=original_log.field_name,
                operation="rollback",
                executed_by="batch_script",
                rollback_operation_id=operation_id
            )
            db.add(rollback_log)
            
            # Get services that were updated in original operation
            service_ids = original_log.target_services
            if not service_ids:
                return {
                    "success": False,
                    "error": "No target services found in original operation"
                }
                
            services = db.query(ServiceMetadata).filter(
                ServiceMetadata.id.in_(service_ids)
            ).all()
            
            # Restore old values
            restored_count = 0
            old_values = original_log.old_values or {}
            
            for service in services:
                if str(service.id) in old_values:
                    old_data = old_values[str(service.id)]
                    old_value = old_data["old_value"]
                    
                    setattr(service, original_log.field_name, old_value)
                    service.version += 1
                    service.updated_at = rollback_start
                    
                    restored_count += 1
                    
            # Mark original operation as rolled back
            original_log.rollback_operation_id = rollback_id
            
            # Complete rollback log
            rollback_log.status = "completed"
            rollback_log.completed_at = rollback_start
            rollback_log.affected_count = restored_count
            
            db.commit()
            
            logger.info(f"Rollback completed: {restored_count} services restored")
            
            return {
                "success": True,
                "rollback_id": rollback_id,
                "original_operation": operation_id,
                "restored_count": restored_count,
                "message": f"Successfully rolled back {restored_count} services"
            }
            
        except Exception as e:
            logger.error(f"Rollback failed: {str(e)}")
            db.rollback()
            
            return {
                "success": False,
                "error": f"Rollback failed: {str(e)}"
            }
        finally:
            db.close()
            
    def _get_filtered_services(self, db: Session, operation: BatchOperation) -> List[ServiceMetadata]:
        """Get services based on filter conditions"""
        
        query = db.query(ServiceMetadata)
        
        # Filter by module
        if operation.target_module != "all":
            query = query.filter(ServiceMetadata.module_name == operation.target_module)
            
        # Apply additional filter conditions
        for field, condition in operation.filter_conditions.items():
            if hasattr(ServiceMetadata, field):
                column = getattr(ServiceMetadata, field)
                
                if isinstance(condition, dict):
                    # Handle complex conditions
                    for operator, value in condition.items():
                        if operator == "gt":
                            query = query.filter(column > value)
                        elif operator == "lt":
                            query = query.filter(column < value)
                        elif operator == "eq":
                            query = query.filter(column == value)
                        elif operator == "ne":
                            query = query.filter(column != value)
                        elif operator == "in":
                            query = query.filter(column.in_(value))
                        elif operator == "like":
                            query = query.filter(column.like(f"%{value}%"))
                else:
                    # Simple equality
                    query = query.filter(column == condition)
                    
        return query.all()
        
    def _calculate_new_value(self, old_value: Any, operation: BatchOperation) -> Any:
        """Calculate new value based on operation type"""
        
        if operation.operation == "set":
            return self._convert_value(operation.value, type(old_value))
            
        elif operation.operation == "increase":
            if isinstance(old_value, (int, float)):
                if isinstance(operation.value, str) and operation.value.endswith("%"):
                    # Percentage increase
                    percentage = float(operation.value[:-1]) / 100
                    return old_value + (old_value * percentage)
                else:
                    # Absolute increase
                    return old_value + float(operation.value)
            else:
                raise ValueError(f"Cannot increase non-numeric value: {old_value}")
                
        elif operation.operation == "decrease":
            if isinstance(old_value, (int, float)):
                if isinstance(operation.value, str) and operation.value.endswith("%"):
                    # Percentage decrease
                    percentage = float(operation.value[:-1]) / 100
                    return old_value - (old_value * percentage)
                else:
                    # Absolute decrease
                    return old_value - float(operation.value)
            else:
                raise ValueError(f"Cannot decrease non-numeric value: {old_value}")
                
        elif operation.operation == "multiply":
            if isinstance(old_value, (int, float)):
                return old_value * float(operation.value)
            else:
                raise ValueError(f"Cannot multiply non-numeric value: {old_value}")
                
        else:
            raise ValueError(f"Unknown operation: {operation.operation}")
            
    def _convert_value(self, value: Any, target_type: type) -> Any:
        """Convert value to target type"""
        
        if target_type == bool:
            if isinstance(value, str):
                return value.lower() in ("true", "1", "yes", "on")
            return bool(value)
        elif target_type == int:
            return int(float(value))  # Handle "10.0" -> 10
        elif target_type == float:
            return float(value)
        else:
            return str(value)
            
    def _simulate_updates(self, services: List[ServiceMetadata], operation: BatchOperation) -> Dict[str, Any]:
        """Simulate updates for dry run mode"""
        
        simulated = {}
        
        for service in services:
            old_value = getattr(service, operation.field_name)
            new_value = self._calculate_new_value(old_value, operation)
            
            simulated[service.id] = {
                "service_name": service.service_name,
                "module": service.module_name,
                "field": operation.field_name,
                "old_value": old_value,
                "new_value": new_value,
                "change": self._describe_change(old_value, new_value)
            }
            
        return simulated
        
    def _describe_change(self, old_value: Any, new_value: Any) -> str:
        """Describe the change between old and new values"""
        
        if isinstance(old_value, (int, float)) and isinstance(new_value, (int, float)):
            if new_value > old_value:
                diff = new_value - old_value
                percentage = (diff / old_value * 100) if old_value != 0 else 0
                return f"+{diff} (+{percentage:.1f}%)"
            elif new_value < old_value:
                diff = old_value - new_value
                percentage = (diff / old_value * 100) if old_value != 0 else 0
                return f"-{diff} (-{percentage:.1f}%)"
            else:
                return "No change"
        else:
            return f"{old_value} -> {new_value}"
            
    def list_operations(self, limit: int = 20) -> List[BatchUpdateLog]:
        """List recent batch operations"""
        
        db = self.SessionLocal()
        try:
            operations = db.query(BatchUpdateLog).order_by(
                BatchUpdateLog.started_at.desc()
            ).limit(limit).all()
            
            return operations
        finally:
            db.close()
            
    def initialize_sample_data(self):
        """Initialize sample service metadata for testing"""
        
        db = self.SessionLocal()
        try:
            # Check if data already exists
            if db.query(ServiceMetadata).count() > 0:
                logger.info("Sample data already exists")
                return
                
            logger.info("Initializing sample service metadata...")
            
            # Sample services from different modules
            sample_services = [
                # Health services
                {"module": "health", "service": "AgendamentoConsulta", "fee": 500, "timeout": 30},
                {"module": "health", "service": "SolicitacaoExame", "fee": 1000, "timeout": 60},
                
                # Finance services  
                {"module": "finance", "service": "PagamentoTaxa", "fee": 200, "timeout": 45},
                {"module": "finance", "service": "MicroCredito", "fee": 5000, "timeout": 120, "approval": True},
                
                # Education services
                {"module": "education", "service": "MatriculaEscolar", "fee": 0, "timeout": 30},
                {"module": "education", "service": "BolsaEstudo", "fee": 1000, "timeout": 90, "approval": True},
                
                # Commercial services
                {"module": "commercial", "service": "AlvaraComercial", "fee": 10000, "timeout": 180, "approval": True},
                {"module": "commercial", "service": "LicencaIndustrial", "fee": 50000, "timeout": 300, "approval": True},
            ]
            
            for service_data in sample_services:
                service = ServiceMetadata(
                    module_name=service_data["module"],
                    service_name=service_data["service"],
                    service_key=service_data["service"],
                    endpoint_path=f"/api/{service_data['service'].lower().replace('_', '-')}",
                    fee_amount=service_data["fee"],
                    timeout_seconds=service_data["timeout"],
                    requires_approval=service_data.get("approval", False),
                    active=True
                )
                db.add(service)
                
            db.commit()
            logger.info(f"Created {len(sample_services)} sample services")
            
        finally:
            db.close()

def main():
    parser = argparse.ArgumentParser(description="SILA Batch Update System with Rollback Protection")
    parser.add_argument("target_module", help="Target module name or 'all'")
    
    # Operation type
    operation_group = parser.add_mutually_exclusive_group(required=True)
    operation_group.add_argument("--set", metavar="VALUE", help="Set field to specific value")
    operation_group.add_argument("--increase", metavar="VALUE", help="Increase field by value (supports %)")
    operation_group.add_argument("--decrease", metavar="VALUE", help="Decrease field by value (supports %)")
    operation_group.add_argument("--multiply", metavar="VALUE", help="Multiply field by value")
    
    # Target field
    parser.add_argument("--field", required=True, help="Field name to update")
    
    # Filtering
    parser.add_argument("--condition", help="Filter condition (e.g., 'fee_amount > 1000')")
    
    # Operation control
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without executing")
    
    # Management commands
    parser.add_argument("--rollback", metavar="OPERATION_ID", help="Rollback a previous operation")
    parser.add_argument("--list-operations", action="store_true", help="List recent operations")
    parser.add_argument("--init-sample", action="store_true", help="Initialize sample data")
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = BatchUpdateManager()
    
    try:
        if args.init_sample:
            manager.initialize_sample_data()
            return
            
        if args.list_operations:
            operations = manager.list_operations()
            
            print("📋 Recent Batch Operations:")
            print("=" * 80)
            
            for op in operations:
                status_icon = "✅" if op.status == "completed" else "❌" if op.status == "failed" else "🔄"
                print(f"{status_icon} {op.operation_id}")
                print(f"   Type: {op.operation_type}")
                print(f"   Target: {op.target_module}")
                print(f"   Field: {op.field_name}")
                print(f"   Started: {op.started_at}")
                print(f"   Status: {op.status}")
                print(f"   Affected: {op.affected_count}")
                if op.error_message:
                    print(f"   Error: {op.error_message}")
                print()
                
            return
            
        if args.rollback:
            result = manager.rollback_operation(args.rollback)
            
            if result["success"]:
                print(f"✅ Rollback successful: {result['message']}")
            else:
                print(f"❌ Rollback failed: {result['error']}")
                
            return
            
        # Determine operation type and value
        if args.set:
            operation_type = "set"
            value = args.set
        elif args.increase:
            operation_type = "increase"
            value = args.increase
        elif args.decrease:
            operation_type = "decrease"
            value = args.decrease
        elif args.multiply:
            operation_type = "multiply"
            value = args.multiply
        else:
            print("❌ No operation specified")
            return
            
        # Parse filter conditions
        filter_conditions = {}
        if args.condition:
            # Simple condition parser (can be enhanced)
            match = re.match(r"(\w+)\s*(>|<|=|!=)\s*(.+)", args.condition)
            if match:
                field, operator, val = match.groups()
                
                # Try to convert value to appropriate type
                try:
                    if val.lower() in ("true", "false"):
                        val = val.lower() == "true"
                    elif val.isdigit():
                        val = int(val)
                    elif "." in val and val.replace(".", "").isdigit():
                        val = float(val)
                except ValueError:
                    pass  # Keep as string
                    
                op_map = {">": "gt", "<": "lt", "=": "eq", "!=": "ne"}
                filter_conditions[field] = {op_map.get(operator, "eq"): val}
                
        # Create operation
        operation_id = f"BATCH_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        operation = BatchOperation(
            operation_id=operation_id,
            target_module=args.target_module,
            field_name=args.field,
            operation=operation_type,
            value=value,
            filter_conditions=filter_conditions,
            dry_run=args.dry_run
        )
        
        # Execute operation
        result = manager.execute_batch_update(operation)
        
        if result["success"]:
            if result.get("dry_run"):
                print(f"🧪 DRY RUN PREVIEW:")
                print(f"   Would affect {result['affected_count']} services")
                print(f"   Operation: {operation_type} {args.field} = {value}")
                
                if "preview" in result:
                    print(f"\\n📋 Changes Preview:")
                    for service_id, changes in result["preview"].items():
                        print(f"   {changes['service_name']} ({changes['module']})")
                        print(f"      {changes['field']}: {changes['change']}")
                        
            else:
                print(f"✅ Batch update successful!")
                print(f"   Operation ID: {result['operation_id']}")
                print(f"   Affected services: {result['affected_count']}")
                print(f"   Rollback available: {result.get('can_rollback', False)}")
                
                if result["affected_count"] < 10:  # Show details for small batches
                    print(f"\\n📋 Updated Services:")
                    for service_id, changes in result["updated_services"].items():
                        print(f"   {changes['service_name']}")
                        print(f"      {args.field}: {changes['old_value']} -> {changes['new_value']}")
        else:
            print(f"❌ Batch update failed: {result['error']}")
            if result.get("rollback_performed"):
                print("🔄 Transaction was automatically rolled back")
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()