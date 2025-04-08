from unittest.mock import AsyncMock

import pytest

from app.query.repository import QueryRepository
from app.query.usecase import QueryUsecase


@pytest.fixture
async def usecase() -> QueryUsecase:
    return QueryUsecase(repository=AsyncMock(spec=QueryRepository))
