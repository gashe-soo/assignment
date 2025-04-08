import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.query.repository import QueryRepository


@pytest.fixture
async def repository(session: AsyncSession) -> QueryRepository:
    return QueryRepository(session)
