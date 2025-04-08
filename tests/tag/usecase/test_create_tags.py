from unittest.mock import AsyncMock

import pytest

from app.tag.dtos import CreateTagDto, TagNameWithLocale
from app.tag.models import Tag, TagTranslation
from app.tag.usecase import TagUsecase


@pytest.mark.asyncio
async def test_it_should_delegate_to_repository(usecase: TagUsecase) -> None:
    # Given
    dto = CreateTagDto(
        tag_name=[
            TagNameWithLocale(name="디자인", locale="ko"),
            TagNameWithLocale(name="Design", locale="en"),
        ]
    )
    expected_tag = Tag(
        id=1,
        translations=[
            TagTranslation(name="디자인", locale="ko"),
            TagTranslation(name="Design", locale="en"),
        ],
    )

    mock_repo = AsyncMock()
    mock_repo.create_tags.return_value = [expected_tag]
    usecase.repository = mock_repo

    # When
    result = await usecase.create_tags([dto])

    # Then
    mock_repo.create_tags.assert_called_once_with([dto])
    assert result == [expected_tag]
