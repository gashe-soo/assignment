import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.repository import CompanyRepository


@pytest.fixture
async def repository(session: AsyncSession) -> CompanyRepository:
    return CompanyRepository(session)
