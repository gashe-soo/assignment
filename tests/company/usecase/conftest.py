from unittest.mock import AsyncMock

import pytest

from app.company.repository import CompanyRepository
from app.company.usecase import CompanyUsecase
from app.tag.usecase import TagUsecase


@pytest.fixture
async def usecase() -> CompanyUsecase:
    return CompanyUsecase(
        repository=AsyncMock(spec=CompanyRepository),
        tag_usecase=AsyncMock(spec=TagUsecase),
    )
