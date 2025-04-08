import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.models import Company, CompanyTranslation
from app.company.repository import CompanyRepository


@pytest.mark.asyncio
async def test_it_should_return_company_when_company_exists(
    session: AsyncSession,
    repository: CompanyRepository,
) -> None:
    # Given
    company = Company()
    company.translations = [
        CompanyTranslation(name="Test Company", locale="EN"),
        CompanyTranslation(name="Test Company", locale="TW"),
        CompanyTranslation(name="테스트", locale="KO"),
    ]
    session.add(company)
    await session.commit()

    # When
    for name, locale in [
        ("Test Company", "EN"),
        ("Test Company", "TW"),
        ("테스트", "KO"),
    ]:
        found_company = await repository.get_company_by_name(name=name)

        # Then
        assert found_company is not None
        assert isinstance(found_company, Company)
        assert found_company.id == company.id
        name_dict = {t.locale: t.name for t in found_company.translations}
        assert name_dict[locale] == name


@pytest.mark.asyncio
async def test_it_should_return_none_when_company_does_not_exist(
    repository: CompanyRepository,
) -> None:
    # Given
    name = "non_existent_company"

    # When
    company = await repository.get_company_by_name(name=name)

    # Then
    assert company is None
