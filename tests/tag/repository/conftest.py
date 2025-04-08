import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.tag.repository import TagRepository


@pytest.fixture
async def repository(session: AsyncSession) -> TagRepository:
    return TagRepository(session)
