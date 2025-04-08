import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.models import Company, CompanyTag, CompanyTranslation
from app.company.repository import CompanyRepository
from app.core.enums import Locale
from app.tag.models import Tag, TagTranslation


@pytest.mark.asyncio
async def test_it_should_delete_company_tag(
    session: AsyncSession, repository: CompanyRepository
) -> None:
    # Given
    tag = Tag(translations=[TagTranslation(locale="ko", name="태그")])
    session.add(tag)
    await session.flush()

    company = Company()
    company.translations = [CompanyTranslation(name="라인", locale=Locale.KO)]
    company.tags = [CompanyTag(tag_id=tag.id)]
    session.add(company)
    await session.flush()

    # When
    await repository.delete_tag_of_company(name="라인", tag_id=tag.id)

    # Then
    stmt = select(CompanyTag).where(
        CompanyTag.company_id == company.id, CompanyTag.tag_id == tag.id
    )
    result = await session.execute(stmt)
    deleted = result.scalar_one_or_none()
    assert deleted is None


@pytest.mark.asyncio
async def test_it_should_do_nothing_if_tag_not_connected(
    session: AsyncSession, repository: CompanyRepository
) -> None:
    # Given
    tag = Tag(translations=[TagTranslation(locale="ko", name="태그")])
    session.add(tag)
    await session.flush()

    company = Company()
    company.translations = [CompanyTranslation(name="라인", locale=Locale.KO)]
    session.add(company)
    await session.flush()

    # When
    await repository.delete_tag_of_company(name="라인", tag_id=tag.id)

    # Then
    stmt = select(CompanyTag).where(
        CompanyTag.company_id == company.id, CompanyTag.tag_id == tag.id
    )
    result = await session.execute(stmt)
    assert result.scalar_one_or_none() is None
