import pytest

from app.query.dtos import CompanyInfoWithLocale, CompanyWithTags
from app.query.usecase import QueryUsecase


@pytest.mark.asyncio
async def test_it_should_return_company_info(
    usecase: QueryUsecase,
):
    # Given
    infos = [
        CompanyInfoWithLocale(
            locale="ko",
            company_info=CompanyWithTags(id=1, name="라인", tags=["IT"]),
        ),
        CompanyInfoWithLocale(
            locale="ko",
            company_info=CompanyWithTags(id=2, name="쿠팡", tags=["IT"]),
        ),
    ]
    usecase.repository.get_companies_by_tag_name.return_value = infos

    # When
    result = await usecase.get_companies_by_tag_name("IT", locale="ko")

    # Then
    assert len(result) == 2
    assert any(c.name == "라인" for c in result)
    assert any(c.name == "쿠팡" for c in result)


@pytest.mark.asyncio
async def test_it_should_return_company_info_if_not_supported_multi_language(
    usecase: QueryUsecase,
):
    # Given
    infos = [
        CompanyInfoWithLocale(
            locale="jp",
            company_info=CompanyWithTags(id=1, name="ライン株式会社", tags=["テック"]),
        ),
        CompanyInfoWithLocale(
            locale="en",
            company_info=CompanyWithTags(
                id=2, name="Coupang", tags=["Logistics"]
            ),
        ),
    ]
    usecase.repository.get_companies_by_tag_name.return_value = infos

    # When
    result = await usecase.get_companies_by_tag_name("Tech", locale="ko")

    # Then
    assert len(result) == 2
    assert any(c.name == "ライン株式会社" for c in result)
    assert any(c.name == "Coupang" for c in result)
