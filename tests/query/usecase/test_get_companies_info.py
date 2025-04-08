import pytest

from app.query.dtos import CompanyInfoWithLocale, CompanyWithTags
from app.query.usecase import QueryUsecase


@pytest.mark.asyncio
async def test_get_companies_info_should_return_exact_locale(
    usecase: QueryUsecase,
) -> None:
    # Given
    infos = [
        CompanyInfoWithLocale(
            locale="ko",
            company_info=CompanyWithTags(id=1, name="라인", tags=["기술"]),
        ),
        CompanyInfoWithLocale(
            locale="en",
            company_info=CompanyWithTags(id=1, name="LINE", tags=["Tech"]),
        ),
        CompanyInfoWithLocale(
            locale="ko",
            company_info=CompanyWithTags(id=2, name="쿠팡", tags=["유통"]),
        ),
    ]
    usecase.repository.get_companies_info.return_value = infos

    # When
    result = await usecase.get_companies_info([1, 2], locale="ko")

    # Then
    assert len(result) == 2
    assert any(c.name == "라인" for c in result)
    assert any(c.name == "쿠팡" for c in result)


@pytest.mark.asyncio
async def test_get_companies_info_should_fallback_if_locale_missing(
    usecase: QueryUsecase,
) -> None:
    # Given
    infos = [
        CompanyInfoWithLocale(
            locale="en",
            company_info=CompanyWithTags(id=1, name="LINE", tags=["Tech"]),
        ),
        CompanyInfoWithLocale(
            locale="ko",
            company_info=CompanyWithTags(id=2, name="쿠팡", tags=["유통"]),
        ),
    ]
    usecase.repository.get_companies_info.return_value = infos

    # When
    result = await usecase.get_companies_info([1, 2], locale="ko")

    # Then
    assert len(result) == 2
    assert any(c.name == "LINE" for c in result)
    assert any(c.name == "쿠팡" for c in result)
