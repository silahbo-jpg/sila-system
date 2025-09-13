# backend/tests/db/test_session.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db, async_session_factory, engine


@pytest.mark.asyncio
async def test_async_session_factory_creates_session():
    """Verifica se o async_session_factory cria uma sessão válida."""
    async with async_session_factory() as session:
        assert isinstance(session, AsyncSession)


@pytest.mark.asyncio
async def test_get_db_dependency_yields_session():
    """Verifica se o get_db gera uma sessão e consegue ser usada."""
    gen = get_db()
    session = await gen.__anext__()
    try:
        assert isinstance(session, AsyncSession)
    finally:
        # garante que o generator é fechado corretamente
        with pytest.raises(StopAsyncIteration):
            await gen.__anext__()


@pytest.mark.asyncio
async def test_engine_is_created():
    """Valida se o engine foi criado corretamente."""
    assert engine is not None
    assert str(engine.url).startswith("postgresql+asyncpg") or str(engine.url).startswith("sqlite+aiosqlite")
