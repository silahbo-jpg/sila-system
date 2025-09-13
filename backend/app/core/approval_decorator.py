"""
Approval Integration Decorator

This decorator integrates approval workflows directly into service endpoints
as specified in the directive. Services can use @requires_approval decorator
to automatically handle multi-level approval workflows.
"""

from functools import wraps
from typing import Dict, Any, Optional, Callable, List
from fastapi import HTTPException, Depends
import uuid

from app.core.workflow import ApprovalWorkflowManager, ApprovalStatus
from app.db.session import SessionLocal  # Ou o caminho real da sua Session
from app.models.approval import ApprovalRequest  # Modelo SQLAlchemy


def requires_approval(
    levels: List[Dict[str, Any]] = None,
    conditions: Dict[str, Any] = None,
    timeout_hours: int = 48,
    auto_configure: bool = True,
):
    """
    Decorator to add approval workflow to service endpoints

    Usage:
    @requires_approval([
        {
            "level": "level_1",
            "approver_roles": ["supervisor"],
            "required": True,
            "timeout_hours": 24
        }
    ])
    def my_service_endpoint(data: MySchema, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
        # Service logic here
        return {"success": True}

    Args:
        levels: List of approval level configurations
        conditions: When approval is required (optional)
        timeout_hours: Default timeout for approvals
        auto_configure: Whether to auto-configure approval for this service
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extrair db e current_user de kwargs
            db = None
            current_user = None

            for value in kwargs.values():
                if isinstance(value, SessionLocal.__class__):  # Verifica se é sessão do SQLAlchemy
                    db = value
                elif hasattr(value, "id") and hasattr(value, "role"):  # Assume ser usuário
                    current_user = value

            if not db:
                raise HTTPException(status_code=500, detail="Database session is required for approval workflow")
            if not current_user:
                raise HTTPException(status_code=401, detail="Authentication required for approval workflow")

            # Extrair informações do serviço
            module_name = _extract_module_name(func)
            service_name = _extract_service_name(func)

            # Auto-configurar workflow se necessário
            if auto_configure and levels:
                workflow_manager = ApprovalWorkflowManager(db)
                endpoint_path = f"/api/{service_name.lower().replace('_', '-')}"
                try:
                    workflow_manager.configure_service_approval(
                        module_name=module_name,
                        service_name=service_name,
                        endpoint_path=endpoint_path,
                        approval_levels=levels,
                        conditions=conditions,
                        timeout_hours=timeout_hours,
                    )
                except Exception as e:
                    # Log e continue (config pode já existir)
                    print(f"Approval auto-configuration failed: {e}")

            # Extrair dados da requisição
            request_data = _extract_request_data(args, kwargs)

            # Gerar ID único da requisição
            service_request_id = f"{service_name}_{uuid.uuid4().hex[:8]}"
            workflow_manager = ApprovalWorkflowManager(db)

            try:
                # Criar requisições de aprovação
                approval_requests = workflow_manager.request_approval(
                    service_request_id=service_request_id,
                    module_name=module_name,
                    service_name=service_name,
                    requester_id=current_user.id,
                    request_data=request_data,
                    justification=request_data.get("justification", "Service approval required"),
                )

                if approval_requests:
                    # Aprovação necessária
                    return {
                        "status": "approval_required",
                        "message": f"This request requires approval from {len(approval_requests)} level(s)",
                        "service_request_id": service_request_id,
                        "approval_requests": [
                            {
                                "id": req.id,
                                "level": req.approval_level,
                                "status": req.status,
                                "due_date": req.due_date.isoformat() if req.due_date else None,
                                "current_approver": req.current_approver_id,
                            }
                            for req in approval_requests
                        ],
                        "next_steps": "Wait for approval or contact the assigned approver",
                    }
                else:
                    # Nenhuma aprovação necessária — execute o serviço
                    return await func(*args, **kwargs)

            except HTTPException:
                raise
            except Exception as e:
                # Em produção, não faça "fail-open" silenciosamente
                raise HTTPException(
                    status_code=500,
                    detail=f"Approval system error: {str(e)}. Service cannot proceed."
                )

        return wrapper

    return decorator


async def check_approval_status(service_request_id: str, db) -> Dict[str, Any]:
    """
    Check the status of an approval request.

    Args:
        service_request_id: ID of the service request
        db: SQLAlchemy database session

    Returns:
        Approval status information
    """
    # Usar SQLAlchemy para buscar requisições
    approval_requests = (
        db.query(ApprovalRequest)
        .filter(ApprovalRequest.service_request_id == service_request_id)
        .order_by(ApprovalRequest.level_order)
        .all()
    )

    if not approval_requests:
        raise HTTPException(status_code=404, detail="Service request not found")

    all_approved = all(req.status == ApprovalStatus.APPROVED for req in approval_requests)
    any_rejected = any(req.status == ApprovalStatus.REJECTED for req in approval_requests)

    if any_rejected:
        overall_status = "rejected"
    elif all_approved:
        overall_status = "approved"
    else:
        overall_status = "pending"

    return {
        "service_request_id": service_request_id,
        "overall_status": overall_status,
        "can_proceed": all_approved,
        "requests": [
            {
                "id": req.id,
                "level": req.approval_level,
                "status": req.status,
                "created_at": req.created_at.isoformat(),
                "due_date": req.due_date.isoformat() if req.due_date else None,
                "approved_at": req.approved_at.isoformat() if req.approved_at else None,
                "current_approver": req.current_approver_id,
                "comments": req.approver_comments,
                "rejection_reason": req.rejection_reason,
            }
            for req in approval_requests
        ],
    }


async def execute_approved_service(
    service_request_id: str,
    original_function: Callable,
    original_args: tuple,
    original_kwargs: dict,
    db,
) -> Any:
    """
    Execute a service after all approvals are complete.

    Args:
        service_request_id: ID of the approved service request
        original_function: Original service function to execute
        original_args: Original function arguments
        original_kwargs: Original function keyword arguments
        db: Database session

    Returns:
        Result of the original service function
    """
    status_info = await check_approval_status(service_request_id, db)

    if not status_info["can_proceed"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot proceed - approval status: {status_info['overall_status']}",
        )

    try:
        result = await original_function(*original_args, **original_kwargs)

        # Registrar execução bem-sucedida
        workflow_manager = ApprovalWorkflowManager(db)
        workflow_manager._log_approval_action(
            approval_request_id=status_info["requests"][0]["id"],
            action="service_executed",
            actor_id=original_kwargs.get("current_user", {}).get("id", 0),
            comments="Service executed successfully after approval",
            action_data={"service_request_id": service_request_id},
        )

        return result

    except Exception as e:
        workflow_manager = ApprovalWorkflowManager(db)
        workflow_manager._log_approval_action(
            approval_request_id=status_info["requests"][0]["id"],
            action="service_execution_failed",
            actor_id=original_kwargs.get("current_user", {}).get("id", 0),
            comments=f"Service execution failed: {str(e)}",
            action_data={"service_request_id": service_request_id, "error": str(e)},
        )
        raise


# === Funções auxiliares ===

def _extract_module_name(func: Callable) -> str:
    """Extract module name from function metadata."""
    module_path = func.__module__
    if "modules." in module_path:
        return module_path.split("modules.")[1].split(".")[0]
    return "unknown"


def _extract_service_name(func: Callable) -> str:
    """Extract service name from function name."""
    func_name = func.__name__
    prefixes = ["criar_", "obter_", "listar_", "atualizar_", "deletar_"]
    for prefix in prefixes:
        if func_name.startswith(prefix):
            func_name = func_name[len(prefix):]
            break
    return "".join(word.capitalize() for word in func_name.split("_"))


def _extract_request_data(args: tuple, kwargs: dict) -> Dict[str, Any]:
    """Extract request data from function arguments."""
    request_data = {}
    for arg in args:
        if hasattr(arg, 'dict'):
            request_data.update(arg.dict())
    for key, value in kwargs.items():
        if key not in ['db', 'current_user', 'request']:
            if hasattr(value, 'dict'):
                request_data.update(value.dict())
            elif isinstance(value, (dict, str, int, float, bool)):
                request_data[key] = value
    return request_data


# === Atalhos comuns ===

def requires_supervisor_approval(timeout_hours: int = 24):
    """Shortcut for simple supervisor approval."""
    return requires_approval([
        {
            "level": "level_1",
            "approver_roles": ["supervisor"],
            "required": True,
            "timeout_hours": timeout_hours
        }
    ])


def requires_manager_approval(timeout_hours: int = 48):
    """Shortcut for manager approval."""
    return requires_approval([
        {
            "level": "level_1",
            "approver_roles": ["supervisor"],
            "required": True,
            "timeout_hours": 24
        },
        {
            "level": "level_2",
            "approver_roles": ["manager"],
            "required": True,
            "timeout_hours": timeout_hours
        }
    ])


def requires_financial_approval(amount_threshold: int = 50000):
    """Shortcut for financial approval based on amount."""
    return requires_approval(
        levels=[
            {
                "level": "level_1",
                "approver_roles": ["financial_supervisor"],
                "required": True,
                "timeout_hours": 24
            },
            {
                "level": "level_2",
                "approver_roles": ["financial_manager"],
                "required_for": {"amount": {"gt": amount_threshold}},
                "timeout_hours": 48
            }
        ],
        conditions={"amount": {"gt": 1000}}
    )