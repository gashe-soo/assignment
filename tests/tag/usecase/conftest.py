from unittest.mock import AsyncMock

import pytest

from app.tag.repository import TagRepository
from app.tag.usecase import TagUsecase


@pytest.fixture
async def usecase() -> TagUsecase:
    return TagUsecase(repository=AsyncMock(spec=TagRepository))
