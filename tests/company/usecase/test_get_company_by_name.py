import pytest

from app.company.exceptions import NotFoundCompanyException
from app.company.models import Company, CompanyTranslation
from app.company.usecase import CompanyUsecase


@pytest.mark.asyncio
async def test_get_company_by_name_should_return_company(
    usecase: CompanyUsecase,
):
    # Given
    company = Company(id=1)
    company.translations = [
        CompanyTranslation(name="라인", locale="ko"),
        CompanyTranslation(name="LINE", locale="en"),
    ]

    usecase.repository.get_company_by_name.return_value = company

    # When
    result = await usecase.get_company_by_name(name="라인")

    # Then
    assert result is company
    usecase.repository.get_company_by_name.assert_awaited_once_with("라인")


@pytest.mark.asyncio
async def test_get_company_by_name_should_raise_if_no_company_matches(
    usecase: CompanyUsecase,
):
    # Given
    usecase.repository.get_company_by_name.return_value = []

    # Expect
    with pytest.raises(NotFoundCompanyException):
        await usecase.get_company_by_name(name="라인")
