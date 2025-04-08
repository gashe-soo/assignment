import pytest

from app.company.dtos import NameWithLocale, TagNameWithLocales
from app.company.usecase import CompanyUsecase
from app.tag.dtos import CreateTagDto, TagNameWithLocale
from app.tag.models import Tag


@pytest.mark.asyncio
async def test_add_tag_on_company_should_create_multilingual_tags_and_add(
    usecase: CompanyUsecase,
) -> None:
    # Given
    tags = [
        TagNameWithLocales(
            names=[
                NameWithLocale(name="기술", locale="ko"),
                NameWithLocale(name="Tech", locale="en"),
            ]
        ),
        TagNameWithLocales(
            names=[
                NameWithLocale(name="디자인", locale="ko"),
                NameWithLocale(name="Design", locale="en"),
            ]
        ),
    ]

    created_tags = [Tag(), Tag()]
    usecase.tag_usecase.create_tags.return_value = created_tags

    # When
    await usecase.add_tag_on_company(name="라인", tags=tags)

    # Then
    expected_dtos = [
        CreateTagDto(
            tag_name=[
                TagNameWithLocale(name="기술", locale="ko"),
                TagNameWithLocale(name="Tech", locale="en"),
            ]
        ),
        CreateTagDto(
            tag_name=[
                TagNameWithLocale(name="디자인", locale="ko"),
                TagNameWithLocale(name="Design", locale="en"),
            ]
        ),
    ]
    usecase.tag_usecase.create_tags.assert_awaited_once_with(expected_dtos)
    usecase.repository.add_tag_on_company.assert_awaited_once_with(
        name="라인", tag_ids=[tag.id for tag in created_tags]
    )
