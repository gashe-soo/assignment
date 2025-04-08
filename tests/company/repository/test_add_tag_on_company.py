import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.models import Company, CompanyTag, CompanyTranslation
from app.company.repository import CompanyRepository
from app.core.enums import Locale
from app.tag.models import Tag


@pytest.mark.asyncio
async def test_it_should_add_new_tags_to_company(
    session: AsyncSession, repository: CompanyRepository
) -> None:
    # Given
    tags = [Tag() for _ in range(3)]
    session.add_all(tags)
    await session.flush()

    company = Company()
    company_name = "라인"
    company.translations = [
        CompanyTranslation(name=company_name, locale=Locale.KO),
    ]
    company.tags = [CompanyTag(tag_id=tags[0].id)]
    session.add(company)
    await session.flush()

    # When
    await repository.add_tag_on_company(company_name, [t.id for t in tags])

    # Then
    stmt = select(CompanyTag).where(CompanyTag.company_id == company.id)
    result = await session.execute(stmt)
    added_tags = result.scalars().all()

    tag_ids = {tag.tag_id for tag in added_tags}
    assert tag_ids == {t.id for t in tags}
