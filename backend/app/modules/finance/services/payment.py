import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.modules.integration.adapters.bna_adapter import BNAAdapter
from app.modules.finance.models.payment import Payment
from app.modules.finance.models.transaction import Transaction
from app.core.config import settings
from app.modules.governance.models.audit_log import AuditLog

class PaymentService:
    """Serviço para processamento de pagamentos no sistema SILA.
    
    Este serviço gerencia todas as operações relacionadas a pagamentos,
    incluindo processamento de taxas municipais, multas e outros serviços
    financeiros oferecidos pela administração municipal.
    """
    
    def __init__(self, db: Session):
        """Inicializa o serviço de pagamento.
        
        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.bna_adapter = BNAAdapter(
            SECRET_KEY_PLACEHOLDER=settings.BNA_API_KEY,
            environment=settings.BNA_ENVIRONMENT
        )
    
    def create_payment(self, 
                      user_id: int,
                      amount: float, 
                      payment_type: str,
                      description: str,
                      reference_id: Optional[str] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> Payment:
        """Cria um novo registro de pagamento no sistema.
        
        Args:
            user_id: ID do usuário que está realizando o pagamento
            amount: Valor do pagamento
            payment_type: Tipo de pagamento (TAXA, MULTA, LICENCA, etc.)
            description: Descrição do pagamento
            reference_id: ID de referência externa (opcional)
            metadata: Metadados adicionais do pagamento (opcional)
            
        Returns:
            Objeto Payment criado
        """
        # Gerar referência única se não fornecida
        if not reference_id:
            reference_id = f"PMT-{uuid.uuid4().hex[:8].upper()}"
            
        # Criar o registro de pagamento
        payment = Payment(
            user_id=user_id,
            amount=amount,
            payment_type=payment_type,
            description=description,
            reference_id=reference_id,
            status="PENDING",
            metadata=metadata or {}
        )
        
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        
        # Registrar na auditoria
        AuditLog.log_action(
            db_session=self.db,
            user_id=user_id,
            action="CREATE",
            resource_type="Payment",
            resource_id=payment.id,
            details={"amount": amount, "type": payment_type}
        )
        
        return payment
    
    def process_bank_payment(self, 
                           payment_id: int, 
                           source_account: str,
                           destination_account: str = settings.MUNICIPALITY_ACCOUNT) -> Dict[str, Any]:
        """Processa um pagamento através da integração bancária.
        
        Args:
            payment_id: ID do pagamento a ser processado
            source_account: Conta bancária de origem
            destination_account: Conta bancária de destino (padrão: conta da municipalidade)
            
        Returns:
            Resultado do processamento do pagamento
        """
        # Buscar o pagamento
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            return {"success": False, "error": "Pagamento não encontrado"}
        
        # Verificar se o pagamento já foi processado
        if payment.status != "PENDING":
            return {"success": False, "error": f"Pagamento já está no status {payment.status}"}
        
        # Processar o pagamento através do adaptador BNA
        result = self.bna_adapter.process_payment(
            source_account=source_account,
            destination_account=destination_account,
            amount=payment.amount,
            description=payment.description,
            reference_id=payment.reference_id
        )
        
        # Atualizar o status do pagamento com base no resultado
        if "error" not in result:
            payment.status = "COMPLETED"
            payment.processed_at = datetime.utcnow()
            payment.transaction_id = result.get("transaction_id")
            
            # Criar registro de transação
            transaction = Transaction(
                payment_id=payment.id,
                transaction_id=result.get("transaction_id"),
                amount=payment.amount,
                source_account=source_account,
                destination_account=destination_account,
                status="COMPLETED",
                details=result
            )
            self.db.add(transaction)
        else:
            payment.status = "FAILED"
            payment.error_message = result.get("error")
        
        self.db.commit()
        self.db.refresh(payment)
        
        # Registrar na auditoria
        AuditLog.log_action(
            db_session=self.db,
            user_id=payment.user_id,
            action="PROCESS_PAYMENT",
            resource_type="Payment",
            resource_id=payment.id,
            details=result
        )
        
        return {"success": payment.status == "COMPLETED", "payment": payment, "result": result}
    
    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        """Busca um pagamento pelo ID.
        
        Args:
            payment_id: ID do pagamento
            
        Returns:
            Objeto Payment ou None se não encontrado
        """
        return self.db.query(Payment).filter(Payment.id == payment_id).first()
    
    def get_user_payments(self, user_id: int) -> List[Payment]:
        """Busca todos os pagamentos de um usuário.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Lista de objetos Payment
        """
        return self.db.query(Payment).filter(Payment.user_id == user_id).all()

