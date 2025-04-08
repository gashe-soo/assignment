import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.dtos import CreateCompanyDto, NameWithLocale
from app.company.models import Company, CompanyTag, CompanyTranslation
from app.company.repository import CompanyRepository
from app.core.enums import Locale
from app.tag.models import Tag


@pytest.mark.asyncio
async def test_create_company(
    session: AsyncSession, repository: CompanyRepository
) -> None:
    # Given
    tags = [Tag(), Tag(), Tag()]
    session.add_all(tags)
    await session.commit()

    company_dto = CreateCompanyDto(
        names=[
            NameWithLocale(name="라인 프레쉬", locale=Locale.KO),
            NameWithLocale(name="LINE FRESH", locale=Locale.EN),
            NameWithLocale(name="LINE FRESH", locale=Locale.TW),
        ],
        tag_ids=[t.id for t in tags],
    )

    # When
    created_company = await repository.create_company(company_data=company_dto)

    # Then
    assert isinstance(created_company, Company)

    # And:
    stmt = select(Company).where(Company.id == created_company.id)
    company = (await session.execute(stmt)).scalar_one_or_none()
    assert company is not None
    assert company.id == created_company.id

    # And
    stmt = select(CompanyTranslation).where(
        CompanyTranslation.company_id == created_company.id
    )
    translations = (await session.execute(stmt)).scalars().all()
    assert len(translations) == len(company_dto.names)
    assert {t.locale: t.name for t in translations} == {
        Locale.KO: "라인 프레쉬",
        Locale.EN: "LINE FRESH",
        Locale.TW: "LINE FRESH",
    }

    # And
    stmt = select(CompanyTag).where(
        CompanyTag.company_id == created_company.id
    )
    company_tags = (await session.execute(stmt)).scalars().all()
    assert len(company_tags) == len(company_dto.tag_ids)
    assert {t.tag_id for t in company_tags} == {t.id for t in tags}
