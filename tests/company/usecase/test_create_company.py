from unittest.mock import AsyncMock

import pytest

from app.company.dtos import (
    CreateCompanyDto,
    CreateCompanyWithTagDto,
    NameWithLocale,
    TagNameWithLocales,
)
from app.company.models import Company
from app.company.repository import CompanyRepository
from app.company.usecase import CompanyUsecase
from app.tag.dtos import CreateTagDto, TagNameWithLocale
from app.tag.models import Tag


@pytest.mark.asyncio
async def test_it_should_create_tags_and_company(
    usecase: CompanyUsecase,
) -> None:
    # Given
    mock_repo = AsyncMock(spec=CompanyRepository)
    usecase.repository = mock_repo

    tag_names_1 = [
        NameWithLocale(name="기술", locale="ko"),
        NameWithLocale(name="Tech", locale="en"),
    ]
    tag1 = Tag(id=1)

    tag_names_2 = [
        NameWithLocale(name="정보통신", locale="ko"),
        NameWithLocale(name="IT", locale="en"),
    ]
    tag2 = Tag(id=2)
    usecase.tag_usecase.create_tags.return_value = [tag1, tag2]

    company = Company(id=1)
    mock_repo.create_company.return_value = company

    dto = CreateCompanyWithTagDto(
        names=[
            NameWithLocale(name="라인", locale="ko"),
            NameWithLocale(name="LINE", locale="en"),
        ],
        tags=[
            TagNameWithLocales(names=tag_names_1),
            TagNameWithLocales(names=tag_names_2),
        ],
    )

    # When
    result = await usecase.create_company(company_data=dto)

    # Then
    usecase.tag_usecase.create_tags.assert_awaited_once()
    expected_tag_dto = [
        CreateTagDto(
            tag_name=[
                TagNameWithLocale(name=tag.name, locale=tag.locale)
                for tag in tag_names_1
            ]
        ),
        CreateTagDto(
            tag_name=[
                TagNameWithLocale(name=tag.name, locale=tag.locale)
                for tag in tag_names_2
            ]
        ),
    ]
    usecase.tag_usecase.create_tags.assert_awaited_with(expected_tag_dto)

    expected_company_dto = CreateCompanyDto(
        names=dto.names,
        tag_ids=[
            tag.id for tag in usecase.tag_usecase.create_tags.return_value
        ],
    )
    mock_repo.create_company.assert_awaited_with(expected_company_dto)
    assert result == company
