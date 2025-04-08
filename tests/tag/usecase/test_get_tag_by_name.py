from unittest.mock import AsyncMock

import pytest

from app.tag.exceptions import NotFoundTagException
from app.tag.models import Tag, TagTranslation
from app.tag.usecase import TagUsecase


@pytest.mark.asyncio
async def test_it_should_return_tag_when_locale_matches(
    usecase: TagUsecase,
) -> None:
    # Given
    tag = Tag(
        id=1,
        translations=[
            TagTranslation(name="디자인", locale="ko"),
            TagTranslation(name="Design", locale="en"),
        ],
    )

    mock_repo = AsyncMock()
    mock_repo.get_tag_by_name.return_value = tag
    usecase.repository = mock_repo

    # When
    result = await usecase.get_tag_by_name("디자인")

    # Then
    assert result is tag
    mock_repo.get_tag_by_name.assert_called_once_with("디자인")


@pytest.mark.asyncio
async def test_it_should_raise_not_found_error_if_tag_not_found(
    usecase: TagUsecase,
) -> None:
    # Given
    mock_repo = AsyncMock()
    mock_repo.get_tag_by_name.return_value = None
    usecase.repository = mock_repo

    # Expect
    with pytest.raises(NotFoundTagException):
        await usecase.get_tag_by_name("없는태그")
