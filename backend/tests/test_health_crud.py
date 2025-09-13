# tests/test_health_crud.py
import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.base import Base
from app.db.session import async_session
from app.modules.health.models.agendamento_consulta import AgendamentoConsulta
from app.modules.health.schemas import HealthCreate, HealthUpdate


@pytest.fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db():
    """Fixture that provides a database session for testing."""
    async with async_session() as session:
        # Begin a transaction
        await session.begin()
        
        try:
            yield session
            # Rollback after test
            await session.rollback()
        finally:
            await session.close()


@pytest.mark.asyncio
async def test_create_health_record(db: AsyncSession):
    """Test creating a health record."""
    cidadao_id = str(uuid4())
    health_data = HealthCreate(
        cidadao_id=cidadao_id,
        tipo_consulta="rotina",
        especialidade="clínico geral",
        data_consulta=datetime.utcnow(),
    )

    # Create a new health record
    db_health = AgendamentoConsulta(**health_data.dict())
    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)
    
    assert db_health is not None
    assert db_health.cidadao_id == cidadao_id
    assert db_health.tipo_consulta == "rotina"


@pytest.mark.asyncio
async def test_get_health_record(db: AsyncSession):
    """Test retrieving a health record by ID."""
    # Create a test record
    cidadao_id = str(uuid4())
    db_health = AgendamentoConsulta(
        cidadao_id=cidadao_id,
        tipo_consulta="urgencia",
        especialidade="cardiologia",
        data_consulta=datetime.utcnow(),
    )
    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)
    
    # Retrieve the record
    result = await db.execute(
        select(AgendamentoConsulta).where(AgendamentoConsulta.id == db_health.id)
    )
    fetched = result.scalars().first()
    
    assert fetched is not None
    assert fetched.id == db_health.id
    assert fetched.tipo_consulta == "urgencia"


@pytest.mark.asyncio
async def test_update_health_record(db: AsyncSession):
    """Test updating a health record."""
    # Create a test record
    cidadao_id = str(uuid4())
    db_health = AgendamentoConsulta(
        cidadao_id=cidadao_id,
        tipo_consulta="rotina",
        especialidade="pediatria",
        data_consulta=datetime.utcnow(),
    )
    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)
    
    # Update the record
    update_data = HealthUpdate(especialidade="neurologia")
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_health, key, value)
    
    await db.commit()
    await db.refresh(db_health)
    
    # Verify the update
    result = await db.execute(
        select(AgendamentoConsulta).where(AgendamentoConsulta.id == db_health.id)
    )
    updated = result.scalars().first()
    
    assert updated is not None
    assert updated.id == db_health.id
    assert updated.especialidade == "neurologia"


@pytest.mark.asyncio
async def test_get_health_by_cidadao(db: AsyncSession):
    """Test retrieving health records by citizen ID."""
    cidadao_id = str(uuid4())
    
    # Create test records for the same citizen
    for esp in ["dermatologia", "ortopedia"]:
        db_health = AgendamentoConsulta(
            cidadao_id=cidadao_id,
            tipo_consulta="especializada",
            especialidade=esp,
            data_consulta=datetime.utcnow(),
        )
        db.add(db_health)
    
    await db.commit()
    
    # Query records by citizen ID
    result = await db.execute(
        select(AgendamentoConsulta)
        .where(AgendamentoConsulta.cidadao_id == cidadao_id)
    )
    records = result.scalars().all()
    
    assert len(records) == 2
    assert all(r.cidadao_id == cidadao_id for r in records)


@pytest.mark.asyncio
async def test_delete_health_record(db: AsyncSession):
    """Test deleting a health record."""
    # Create a test record
    cidadao_id = str(uuid4())
    db_health = AgendamentoConsulta(
        cidadao_id=cidadao_id,
        tipo_consulta="rotina",
        especialidade="endocrinologia",
        data_consulta=datetime.utcnow(),
    )
    db.add(db_health)
    await db.commit()
    await db.refresh(db_health)
    
    # Delete the record
    await db.delete(db_health)
    await db.commit()
    
    # Verify the record is deleted
    result = await db.execute(
        select(AgendamentoConsulta).where(AgendamentoConsulta.id == db_health.id)
    )
    fetched = result.scalars().first()
    
    assert fetched is None
