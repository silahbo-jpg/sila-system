from typing import Dict, Any, Optional, List
import logging
from sqlalchemy.orm import Session

from app.modules.address.models import Address
from app.modules.address.schemas import AddressCreate, AddressUpdate
from app.modules.address.crud import address_crud
from app.modules.integration.integration_gateway import integration_gateway

# Configuração de logging
logger = logging.getLogger("address.address_service")

async def create_address(db: Session, address_data: AddressCreate) -> Address:
    """Cria um novo endereço no sistema.
    
    Args:
        db: Sessão do banco de dados
        address_data: Dados do endereço a ser criado
        
    Returns:
        O endereço criado
    """
    logger.info(f"Criando novo endereço para o cidadão {address_data.citizen_id}")
    
    # Verificar se já existe um endereço principal para o cidadão
    if address_data.is_primary:
        existing_primary = await address_crud.get_primary_address(db, citizen_id=address_data.citizen_id)
        if existing_primary:
            # Atualizar o endereço existente para não ser mais o principal
            await address_crud.update(
                db, 
                db_obj=existing_primary, 
                obj_in={"is_primary": False}
            )
            logger.info(f"Endereço anterior marcado como não principal: ID {existing_primary.id}")
    
    # Criar o endereço no banco de dados
    address = await address_crud.create(db, obj_in=address_data)
    
    # Publicar evento de endereço criado/alterado
    if address.is_primary:
        await publish_address_changed_event(address)
    
    logger.info(f"Endereço criado com sucesso: ID {address.id}")
    return address

async def update_address(db: Session, address_id: str, address_data: AddressUpdate) -> Optional[Address]:
    """Atualiza um endereço existente.
    
    Args:
        db: Sessão do banco de dados
        address_id: ID do endereço a ser atualizado
        address_data: Dados atualizados do endereço
        
    Returns:
        O endereço atualizado ou None se não for encontrado
    """
    logger.info(f"Atualizando endereço: ID {address_id}")
    
    # Verificar se o endereço existe
    address = await address_crud.get(db, id=address_id)
    if not address:
        logger.warning(f"Endereço não encontrado: ID {address_id}")
        return None
    
    # Se estiver definindo este endereço como principal, atualizar os outros
    if address_data.is_primary and not address.is_primary:
        existing_primary = await address_crud.get_primary_address(db, citizen_id=address.citizen_id)
        if existing_primary and existing_primary.id != address_id:
            # Atualizar o endereço existente para não ser mais o principal
            await address_crud.update(
                db, 
                db_obj=existing_primary, 
                obj_in={"is_primary": False}
            )
            logger.info(f"Endereço anterior marcado como não principal: ID {existing_primary.id}")
    
    # Atualizar o endereço
    was_primary_before = address.is_primary
    updated_address = await address_crud.update(db, db_obj=address, obj_in=address_data)
    
    # Verificar se precisa publicar evento de alteração de endereço
    should_publish = (
        # Se o endereço se tornou principal
        (not was_primary_before and updated_address.is_primary) or
        # Ou se já era principal e algum campo de endereço foi alterado
        (was_primary_before and updated_address.is_primary and any([
            hasattr(address_data, "street") and address_data.street is not None,
            hasattr(address_data, "number") and address_data.number is not None,
            hasattr(address_data, "complement") and address_data.complement is not None,
            hasattr(address_data, "neighborhood") and address_data.neighborhood is not None,
            hasattr(address_data, "city") and address_data.city is not None,
            hasattr(address_data, "state") and address_data.state is not None,
            hasattr(address_data, "postal_code") and address_data.postal_code is not None,
            hasattr(address_data, "country") and address_data.country is not None
        ]))
    )
    
    if should_publish:
        await publish_address_changed_event(updated_address)
    
    logger.info(f"Endereço atualizado com sucesso: ID {address_id}")
    return updated_address

async def get_address(db: Session, address_id: str) -> Optional[Address]:
    """Obtém um endereço pelo ID.
    
    Args:
        db: Sessão do banco de dados
        address_id: ID do endereço
        
    Returns:
        O endereço ou None se não for encontrado
    """
    logger.info(f"Buscando endereço: ID {address_id}")
    address = await address_crud.get(db, id=address_id)
    
    if not address:
        logger.warning(f"Endereço não encontrado: ID {address_id}")
    else:
        logger.info(f"Endereço encontrado: ID {address_id}")
    
    return address

async def get_addresses_by_citizen(db: Session, citizen_id: str) -> List[Address]:
    """Obtém todos os endereços de um cidadão.
    
    Args:
        db: Sessão do banco de dados
        citizen_id: ID do cidadão
        
    Returns:
        Lista de endereços do cidadão
    """
    logger.info(f"Buscando endereços do cidadão: ID {citizen_id}")
    addresses = await address_crud.get_multi_by_citizen(db, citizen_id=citizen_id)
    
    logger.info(f"Encontrados {len(addresses)} endereços para o cidadão {citizen_id}")
    return addresses

async def get_primary_address(db: Session, citizen_id: str) -> Optional[Address]:
    """Obtém o endereço principal de um cidadão.
    
    Args:
        db: Sessão do banco de dados
        citizen_id: ID do cidadão
        
    Returns:
        O endereço principal ou None se não for encontrado
    """
    logger.info(f"Buscando endereço principal do cidadão: ID {citizen_id}")
    address = await address_crud.get_primary_address(db, citizen_id=citizen_id)
    
    if not address:
        logger.warning(f"Endereço principal não encontrado para o cidadão: ID {citizen_id}")
    else:
        logger.info(f"Endereço principal encontrado para o cidadão: ID {citizen_id}")
    
    return address

async def publish_address_changed_event(address: Address) -> None:
    """Publica um evento de alteração de endereço no gateway de integração.
    
    Este método é chamado quando o endereço principal de um cidadão é alterado,
    permitindo que outros módulos sejam nnnnotificados e possam atualizar
    suas informações relacionadas.
    
    Args:
        address: O endereço alterado
    """
    try:
        # Verificar se é o endereço principal
        if not address.is_primary:
            logger.debug(f"Ignorando publicação de evento para endereço não principal: ID {address.id}")
            return
        
        # Preparar payload do evento
        payload = {
            "address_id": address.id,
            "citizen_id": address.citizen_id,
            "address": {
                "street": address.street,
                "number": address.number,
                "complement": address.complement,
                "neighborhood": address.neighborhood,
                "city": address.city,
                "state": address.state,
                "postal_code": address.postal_code,
                "country": address.country,
                "is_primary": address.is_primary
            }
        }
        
        # Publicar evento no gateway de integração
        logger.info(f"Publicando evento address.changed para o cidadão {address.citizen_id}")
        await integration_gateway.publish(
            event_type="address.changed",
            payload=payload,
            source_module="address"
        )
        
        logger.info(f"Evento address.changed publicado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao publicar evento address.changed: {str(e)}")
        # Não propagar a exceção para não afetar o fluxo principal

