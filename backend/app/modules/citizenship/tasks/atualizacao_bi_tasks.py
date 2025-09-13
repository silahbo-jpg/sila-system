"""
Background tasks for BI Update functionality.
This module handles all asynchronous tasks related to BI updates.
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.email import send_email
from app.core.logging import get_logger
from app.db.session import get_db
from app.modules.citizenship.models.atualizacao_b_i import AtualizacaoBI
from app.modules.citizenship.services.atualizacao_bi_business import BIStatus

logger = get_logger(__name__)

class BITaskHandler:
    """Handler for background tasks related to BI updates"""
    
    @staticmethod
    def send_status_notification(
        email: str,
        request_id: int,
        status: str,
        additional_info: Optional[Dict] = None
    ) -> None:
        """Send email notification about status change"""
        try:
            subject = f"Atualização do estado do seu pedido de BI #{request_id}"
            
            status_messages = {
                BIStatus.PENDING: "O seu pedido foi recebido e está em análise.",
                BIStatus.UNDER_REVIEW: "O seu pedido está a ser analisado pela nossa equipa.",
                BIStatus.APPROVED: "O seu pedido foi aprovado e está em processamento.",
                BIStatus.REJECTED: "O seu pedido foi rejeitado.",
                BIStatus.PROCESSING: "O seu documento está a ser processado.",
                BIStatus.COMPLETED: "O seu documento está pronto para levantamento.",
                BIStatus.CANCELLED: "O seu pedido foi cancelado.",
            }
            
            message = f"""
            <h2>Atualização do Estado do Pedido #{request_id}</h2>
            <p>{status_messages.get(status, 'O estado do seu pedido foi atualizado.')}</p>
            """
            
            if additional_info:
                message += "<p>Informações adicionais:</p><ul>"
                for key, value in additional_info.items():
                    message += f"<li><strong>{key}:</strong> {value}</li>"
                message += "</ul>"
                
            message += """
            <p>Para mais informações, entre em contacto com o suporte.</p>
            <p>Atenciosamente,<br>Equipa de Atendimento</p>
            """
            
            send_email(
                to_email=email,
                subject=subject,
                html_content=message,
                from_email=settings.EMAILS_FROM_EMAIL,
            )
            
        except Exception as e:
            logger.error(f"Failed to send status notification email: {str(e)}")
            # Don't raise exception to avoid breaking the main flow
    
    @classmethod
    def process_document_approval(
        cls,
        db: Session,
        request_id: int,
        background_tasks: BackgroundTasks
    ) -> None:
        """Process document approval and trigger next steps"""
        try:
            request = db.query(AtualizacaoBI).filter_by(id=request_id).first()
            if not request:
                logger.error(f"BI update request {request_id} not found")
                return
                
            # Update status to processing
            request.status = BIStatus.PROCESSING
            request.dados_adicionais["processing_started_at"] = datetime.utcnow().isoformat()
            db.commit()
            
            # Queue document generation
            background_tasks.add_task(
                cls.generate_document,
                db=db,
                request_id=request_id
            )
            
            # Send notification
            background_tasks.add_task(
                cls.send_status_notification,
                email=request.dados_adicionais.get("email"),
                request_id=request_id,
                status=BIStatus.PROCESSING
            )
            
        except Exception as e:
            logger.error(f"Error processing document approval: {str(e)}")
            db.rollback()
    
    @staticmethod
    def generate_document(db: Session, request_id: int) -> None:
        """Generate the actual document (simplified example)"""
        try:
            # In a real implementation, this would generate the actual document
            # For now, we'll just simulate the process
            import time
            time.sleep(5)  # Simulate processing time
            
            request = db.query(AtualizacaoBI).filter_by(id=request_id).with_for_update().first()
            if not request:
                return
                
            # Update with generated document info
            request.dados_adicionais["document_generated_at"] = datetime.utcnow().isoformat()
            request.status = BIStatus.COMPLETED
            db.commit()
            
        except Exception as e:
            logger.error(f"Error generating document: {str(e)}")
            db.rollback()
    
    @classmethod
    def handle_status_change(
        cls,
        db: Session,
        request_id: int,
        new_status: str,
        background_tasks: BackgroundTasks,
        user_role: str = "user",
        notes: Optional[str] = None
    ) -> None:
        """Handle status change and trigger appropriate actions"""
        try:
            request = db.query(AtualizacaoBI).filter_by(id=request_id).first()
            if not request:
                logger.error(f"BI update request {request_id} not found")
                return
                
            old_status = request.status
            request.status = new_status
            
            # Update status history
            status_history = request.dados_adicionais.get("status_history", [])
            status_history.append({
                "status": new_status,
                "timestamp": datetime.utcnow().isoformat(),
                "changed_by": user_role,
                "notes": notes
            })
            request.dados_adicionais["status_history"] = status_history
            
            # Special handling for specific status changes
            if new_status == BIStatus.APPROVED:
                background_tasks.add_task(
                    cls.process_document_approval,
                    db=db,
                    request_id=request_id,
                    background_tasks=background_tasks
                )
            
            db.commit()
            
            # Send notification
            background_tasks.add_task(
                cls.send_status_notification,
                email=request.dados_adicionais.get("email"),
                request_id=request_id,
                status=new_status,
                additional_info={
                    "old_status": old_status,
                    "notes": notes
                } if notes else None
            )
            
        except Exception as e:
            logger.error(f"Error handling status change: {str(e)}")
            db.rollback()
            raise
