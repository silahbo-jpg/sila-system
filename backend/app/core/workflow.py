"""
Multi-Level Approval Workflow System

This module implements configurable approval workflows for sensitive services.
Each service can have multiple approval levels with different approvers.

As specified in the directive:
- Integrate directly into services with approval_required=True
- Create approvals table with service_request_id + level + approver_id
- Expose CLI set-approval-level command
- Create Grafana metrics for approval percentages

NOTE: Currently disabled during Prisma migration
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
# from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
# from sqlalchemy.orm import relationship, Session
# from sqlalchemy.sql import func
# from app.db.base_class import Base
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class ApprovalStatus(str, Enum):
    """Status of approval requests"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ESCALATED = "escalated"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class ApprovalLevel(str, Enum):
    """Approval levels in hierarchical order"""
    LEVEL_1 = "level_1"  # Basic approval (e.g., supervisor)
    LEVEL_2 = "level_2"  # Mid-level approval (e.g., department head)
    LEVEL_3 = "level_3"  # High-level approval (e.g., director)
    LEVEL_4 = "level_4"  # Executive approval (e.g., mayor)

# TODO: Migrate to Prisma models
# class ApprovalRequest(Base):
# class ApprovalHistory(Base):
# class ServiceApprovalConfig(Base):
# TODO: Migrate to Prisma models
"""
class ApprovalRequest(Base):
    Core approval request model
    Links service requests to approval workflow
    __tablename__ = "approval_requests"

    id = Column(Integer, primary_key=True, index=True)
    
    # Service identification
    service_request_id = Column(String(100), nullable=False, index=True)
    module_name = Column(String(100), nullable=False)
    service_name = Column(String(100), nullable=False)
    endpoint_path = Column(String(200), nullable=False)
    
    # Requester information
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    requester_name = Column(String(200))
    requester_email = Column(String(200))
    
    # Approval configuration
    approval_level = Column(SQLEnum(ApprovalLevel), nullable=False)
    level_order = Column(Integer, nullable=False)  # 1, 2, 3, 4
    is_final_level = Column(Boolean, default=False)
    
    # Current status
    status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)
    current_approver_id = Column(Integer, ForeignKey("users.id"))
    
    # Request data
    request_data = Column(JSON)  # Original service request data
    justification = Column(Text)  # Why approval is needed
    priority = Column(Integer, default=2)  # 1=low, 2=normal, 3=high, 4=urgent
    
    # Timing
    created_at = Column(DateTime, default=func.now())
    due_date = Column(DateTime)  # When approval expires
    approved_at = Column(DateTime)
    
    # Decision details
    approver_comments = Column(Text)
    rejection_reason = Column(Text)
    
    # Workflow tracking
    workflow_id = Column(String(50))  # Links related approvals
    next_level_id = Column(Integer, ForeignKey("approval_requests.id"))  # Next approval in chain
    
    # Relationships
    requester = relationship("User", foreign_keys=[requester_id])
    current_approver = relationship("User", foreign_keys=[current_approver_id])
    next_level = relationship("ApprovalRequest", remote_side=[id])
    approval_history = relationship("ApprovalHistory", back_populates="approval_request")
"""

class ApprovalWorkflowManager:
    """Temporary placeholder for workflow manager"""
    def __init__(self, db):
        self.db = db
        pass

class ApprovalHistory(Base):
    """
    History of all approval actions for audit trail
    """
    __tablename__ = "approval_history"

    id = Column(Integer, primary_key=True, index=True)
    approval_request_id = Column(Integer, ForeignKey("approval_requests.id"), nullable=False)
    
    # Action details
    action = Column(String(50), nullable=False)  # approved, rejected, escalated, etc.
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    actor_name = Column(String(200))
    
    # Action context
    comments = Column(Text)
    reason = Column(Text)
    action_data = Column(JSON)
    
    # Timing
    timestamp = Column(DateTime, default=func.now())
    
    # System context
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Relationships
    approval_request = relationship("ApprovalRequest", back_populates="approval_history")
    actor = relationship("User", foreign_keys=[actor_id])

class ServiceApprovalConfig(Base):
    """
    Configuration for service approval requirements
    """
    __tablename__ = "service_approval_configs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Service identification
    module_name = Column(String(100), nullable=False)
    service_name = Column(String(100), nullable=False)
    endpoint_path = Column(String(200), nullable=False)
    
    # Approval configuration
    requires_approval = Column(Boolean, default=False)
    approval_levels = Column(JSON)  # List of required levels and approvers
    auto_approve_threshold = Column(JSON)  # Conditions for auto-approval
    
    # Timing configuration
    default_timeout_hours = Column(Integer, default=48)
    escalation_timeout_hours = Column(Integer, default=24)
    
    # Conditional approval
    approval_conditions = Column(JSON)  # When approval is required
    exemption_conditions = Column(JSON)  # When approval can be skipped
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Unique constraint
    __table_args__ = (
        {'mysql_engine': 'InnoDB'})

class ApprovalWorkflowManager:
    """
    Manages approval workflows for services
    
    Key capabilities:
    - Configure approval levels per service
    - Process approval requests
    - Handle escalations and timeouts
    - Generate approval metrics
    """
    
    def __init__(self, db: Session):
        self.db = db
        
    def configure_service_approval(
        self,
        module_name: str,
        service_name: str,
        endpoint_path: str,
        approval_levels: List[Dict[str, Any]],
        conditions: Dict[str, Any] = None,
        timeout_hours: int = 48
    ) -> ServiceApprovalConfig:
        """
        Configure approval requirements for a service
        
        Args:
            module_name: Module containing the service
            service_name: Service identifier
            endpoint_path: API endpoint path
            approval_levels: List of approval level configurations
            conditions: When approval is required
            timeout_hours: Default approval timeout
            
        Example approval_levels:
        [
            {
                "level": "level_1",
                "approver_roles": ["supervisor", "team_lead"],
                "approver_ids": [123, 456],
                "required": True,
                "timeout_hours": 24
            },
            {
                "level": "level_2", 
                "approver_roles": ["department_head"],
                "required_for": {"amount": {"gt": 1000}},
                "timeout_hours": 48
            }
        ]
        """
        
        # Check if config already exists
        existing_config = self.db.query(ServiceApprovalConfig).filter(
            ServiceApprovalConfig.module_name == module_name,
            ServiceApprovalConfig.service_name == service_name
        ).first()
        
        if existing_config:
            # Update existing configuration
            existing_config.approval_levels = approval_levels
            existing_config.approval_conditions = conditions
            existing_config.default_timeout_hours = timeout_hours
            existing_config.requires_approval = True
            existing_config.updated_at = datetime.now()
            config = existing_config
        else:
            # Create new configuration
            config = ServiceApprovalConfig(
                module_name=module_name,
                service_name=service_name,
                endpoint_path=endpoint_path,
                requires_approval=True,
                approval_levels=approval_levels,
                approval_conditions=conditions,
                default_timeout_hours=timeout_hours
            )
            self.db.add(config)
            
        self.db.commit()
        
        logger.info(f"Configured approval for {module_name}.{service_name}")
        return config
        
    def request_approval(
        self,
        service_request_id: str,
        module_name: str,
        service_name: str,
        requester_id: int,
        request_data: Dict[str, Any],
        justification: str = None
    ) -> List[ApprovalRequest]:
        """
        Create approval request(s) for a service call
        
        Returns list of approval requests (may be multiple levels)
        """
        
        # Get service approval configuration
        config = self.db.query(ServiceApprovalConfig).filter(
            ServiceApprovalConfig.module_name == module_name,
            ServiceApprovalConfig.service_name == service_name,
            ServiceApprovalConfig.requires_approval == True
        ).first()
        
        if not config:
            raise HTTPException(
                status_code=400,
                detail=f"No approval configuration found for {module_name}.{service_name}"
            )
            
        # Check if approval is actually needed based on conditions
        if not self._check_approval_needed(config, request_data):
            return []  # No approval needed
            
        approval_requests = []
        workflow_id = f"{service_request_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create approval requests for each required level
        for level_config in config.approval_levels:
            if self._is_level_required(level_config, request_data):
                
                # Determine approvers for this level
                approvers = self._get_level_approvers(level_config)
                if not approvers:
                    logger.warning(f"No approvers found for level {level_config['level']}")
                    continue
                    
                # Create approval request
                approval_request = ApprovalRequest(
                    service_request_id=service_request_id,
                    module_name=module_name,
                    service_name=service_name,
                    endpoint_path=config.endpoint_path,
                    requester_id=requester_id,
                    approval_level=ApprovalLevel(level_config['level']),
                    level_order=self._get_level_order(level_config['level']),
                    current_approver_id=approvers[0],  # Assign to first available approver
                    request_data=request_data,
                    justification=justification,
                    workflow_id=workflow_id,
                    due_date=datetime.now() + timedelta(hours=level_config.get('timeout_hours', 48))
                )
                
                self.db.add(approval_request)
                approval_requests.append(approval_request)
                
        # Link approval requests in sequence
        if len(approval_requests) > 1:
            for i in range(len(approval_requests) - 1):
                approval_requests[i].next_level_id = approval_requests[i + 1].id
                
        # Mark the final level
        if approval_requests:
            approval_requests[-1].is_final_level = True
            
        self.db.commit()
        
        # Log approval request creation
        for req in approval_requests:
            self._log_approval_action(
                req.id,
                "request_created",
                requester_id,
                f"Approval requested for {service_name}",
                {"justification": justification}
            )
            
        logger.info(f"Created {len(approval_requests)} approval requests for {service_request_id}")
        return approval_requests
        
    def approve_request(
        self,
        approval_request_id: int,
        approver_id: int,
        comments: str = None
    ) -> bool:
        """
        Approve a specific approval request
        
        Returns True if service can proceed (all approvals complete)
        """
        
        approval_request = self.db.query(ApprovalRequest).get(approval_request_id)
        if not approval_request:
            raise HTTPException(status_code=404, detail="Approval request not found")
            
        # Verify approver authorization
        if approval_request.current_approver_id != approver_id:
            raise HTTPException(status_code=403, detail="Not authorized to approve this request")
            
        # Update approval status
        approval_request.status = ApprovalStatus.APPROVED
        approval_request.approved_at = datetime.now()
        approval_request.approver_comments = comments
        
        # Log the approval
        self._log_approval_action(
            approval_request.id,
            "approved",
            approver_id,
            f"Request approved: {approval_request.service_name}",
            {"comments": comments}
        )
        
        # Check if there are more levels to approve
        if approval_request.next_level_id:
            # Move to next approval level
            next_approval = self.db.query(ApprovalRequest).get(approval_request.next_level_id)
            if next_approval:
                next_approval.status = ApprovalStatus.PENDING
                self._log_approval_action(
                    next_approval.id,
                    "escalated_to_next_level",
                    approver_id,
                    f"Escalated to {next_approval.approval_level.value}")
                
        self.db.commit()
        
        # Check if all approvals in workflow are complete
        return self._check_workflow_complete(approval_request.workflow_id)
        
    def reject_request(
        self,
        approval_request_id: int,
        approver_id: int,
        reason: str
    ) -> bool:
        """
        Reject an approval request
        
        Returns True (rejection stops the workflow)
        """
        
        approval_request = self.db.query(ApprovalRequest).get(approval_request_id)
        if not approval_request:
            raise HTTPException(status_code=404, detail="Approval request not found")
            
        # Verify approver authorization
        if approval_request.current_approver_id != approver_id:
            raise HTTPException(status_code=403, detail="Not authorized to reject this request")
            
        # Update status
        approval_request.status = ApprovalStatus.REJECTED
        approval_request.rejection_reason = reason
        
        # Log the rejection
        self._log_approval_action(
            approval_request.id,
            "rejected",
            approver_id,
            f"Request rejected: {approval_request.service_name}",
            {"reason": reason}
        )
        
        # Reject all subsequent approvals in the workflow
        self._reject_workflow(approval_request.workflow_id, "Previous level rejected")
        
        self.db.commit()
        return True
        
    def get_pending_approvals(self, approver_id: int) -> List[ApprovalRequest]:
        """Get all pending approvals for a specific approver"""
        
        return self.db.query(ApprovalRequest).filter(
            ApprovalRequest.current_approver_id == approver_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        ).order_by(ApprovalRequest.created_at.desc()).all()
        
    def get_approval_metrics(self) -> Dict[str, Any]:
        """
        Generate approval metrics for Grafana dashboard
        
        Returns metrics like approval rates, average time, etc.
        """
        
        from sqlalchemy import func
        
        # Total requests
        total_requests = self.db.query(ApprovalRequest).count()
        
        # Status breakdown
        status_counts = self.db.query(
            ApprovalRequest.status,
            func.count(ApprovalRequest.id).label('count')
        ).group_by(ApprovalRequest.status).all()
        
        # Services requiring approval percentage
        total_services = 150  # Our total services
        services_with_approval = self.db.query(ServiceApprovalConfig).filter(
            ServiceApprovalConfig.requires_approval == True
        ).count()
        
        approval_percentage = (services_with_approval / total_services) * 100 if total_services > 0 else 0
        
        # Average approval time (for completed requests)
        avg_approval_time_query = self.db.query(
            func.avg(
                func.timestampdiff(
                    'HOUR',
                    ApprovalRequest.created_at,
                    ApprovalRequest.approved_at
                )
            ).label('avg_hours')
        ).filter(
            ApprovalRequest.status == ApprovalStatus.APPROVED,
            ApprovalRequest.approved_at.isnot(None)
        ).first()
        
        avg_approval_hours = avg_approval_time_query.avg_hours if avg_approval_time_query.avg_hours else 0
        
        return {
            "total_requests": total_requests,
            "status_breakdown": {status: count for status, count in status_counts},
            "services_requiring_approval_percentage": round(approval_percentage, 2),
            "average_approval_time_hours": round(avg_approval_hours, 2) if avg_approval_hours else 0,
            "approval_rate": self._calculate_approval_rate(),
            "pending_requests": self.db.query(ApprovalRequest).filter(
                ApprovalRequest.status == ApprovalStatus.PENDING
            ).count()
        }
        
    def _check_approval_needed(self, config: ServiceApprovalConfig, request_data: Dict) -> bool:
        """Check if approval is needed based on configured conditions"""
        
        if not config.approval_conditions:
            return True  # Always require approval if no conditions
            
        # Implement condition checking logic
        # This is a simplified version - real implementation would be more sophisticated
        for condition_key, condition_value in config.approval_conditions.items():
            if condition_key in request_data:
                if isinstance(condition_value, dict):
                    # Handle complex conditions like {"gt": 1000}
                    for operator, threshold in condition_value.items():
                        if operator == "gt" and request_data[condition_key] > threshold:
                            return True
                        elif operator == "gte" and request_data[condition_key] >= threshold:
                            return True
                        # Add more operators as needed
                elif request_data[condition_key] == condition_value:
                    return True
                    
        return False
        
    def _is_level_required(self, level_config: Dict, request_data: Dict) -> bool:
        """Check if a specific approval level is required"""
        
        if level_config.get("required", True):
            return True
            
        # Check conditional requirements
        required_for = level_config.get("required_for")
        if required_for:
            return self._check_conditions(required_for, request_data)
            
        return False
        
    def _get_level_approvers(self, level_config: Dict) -> List[int]:
        """Get list of approver IDs for a level"""
        
        approvers = []
        
        # Direct approver IDs
        if "approver_ids" in level_config:
            approvers.extend(level_config["approver_ids"])
            
        # Approvers by role (would need role-user mapping)
        if "approver_roles" in level_config:
            # This would typically query a roles/users table
            # For now, return empty list - implement based on your user/role system
            pass
            
        return approvers
        
    def _get_level_order(self, level_str: str) -> int:
        """Convert level string to numeric order"""
        level_map = {
            "level_1": 1,
            "level_2": 2,
            "level_3": 3,
            "level_4": 4
        }
        return level_map.get(level_str, 1)
        
    def _check_workflow_complete(self, workflow_id: str) -> bool:
        """Check if all approvals in a workflow are complete"""
        
        pending_approvals = self.db.query(ApprovalRequest).filter(
            ApprovalRequest.workflow_id == workflow_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        ).count()
        
        return pending_approvals == 0
        
    def _reject_workflow(self, workflow_id: str, reason: str):
        """Reject all approvals in a workflow"""
        
        pending_approvals = self.db.query(ApprovalRequest).filter(
            ApprovalRequest.workflow_id == workflow_id,
            ApprovalRequest.status == ApprovalStatus.PENDING
        ).all()
        
        for approval in pending_approvals:
            approval.status = ApprovalStatus.REJECTED
            approval.rejection_reason = reason
            
    def _calculate_approval_rate(self) -> float:
        """Calculate overall approval rate percentage"""
        
        completed_requests = self.db.query(ApprovalRequest).filter(
            ApprovalRequest.status.in_([ApprovalStatus.APPROVED, ApprovalStatus.REJECTED])
        ).count()
        
        approved_requests = self.db.query(ApprovalRequest).filter(
            ApprovalRequest.status == ApprovalStatus.APPROVED
        ).count()
        
        if completed_requests == 0:
            return 0.0
            
        return round((approved_requests / completed_requests) * 100, 2)
        
    def _check_conditions(self, conditions: Dict, data: Dict) -> bool:
        """Generic condition checker"""
        
        for key, condition in conditions.items():
            if key not in data:
                continue
                
            if isinstance(condition, dict):
                for operator, value in condition.items():
                    if operator == "gt" and data[key] <= value:
                        return False
                    elif operator == "lt" and data[key] >= value:
                        return False
                    elif operator == "eq" and data[key] != value:
                        return False
            else:
                if data[key] != condition:
                    return False
                    
        return True
        
    def _log_approval_action(
        self,
        approval_request_id: int,
        action: str,
        actor_id: int,
        comments: str = None,
        action_data: Dict = None
    ):
        """Log approval actions for audit trail"""
        
        history_entry = ApprovalHistory(
            approval_request_id=approval_request_id,
            action=action,
            actor_id=actor_id,
            comments=comments,
            action_data=action_data or {}
        )
        
        self.db.add(history_entry)