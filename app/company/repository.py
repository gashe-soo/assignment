from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.company.dtos import CompanyWithLocale, CreateCompanyDto
from app.company.models import Company, CompanyTag, CompanyTranslation


class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_company(self, company_data: CreateCompanyDto) -> Company:
        company = Company()
        company.translations = [
            CompanyTranslation(
                name=name_with_locale.name, locale=name_with_locale.locale
            )
            for name_with_locale in company_data.names
        ]
        company.tags = [
            CompanyTag(tag_id=tag_id) for tag_id in company_data.tag_ids
        ]

        self.session.add(company)
        await self.session.flush()
        return company

    async def get_company_by_name(self, name: str) -> Company | None:
        stmt = (
            select(Company)
            .join(CompanyTranslation)
            .options(
                joinedload(Company.translations), joinedload(Company.tags)
            )
            .where(CompanyTranslation.name == name)
            .limit(1)
        )

        result = (await self.session.execute(stmt)).unique().scalars().first()
        return result if result else None

    async def search_companies_with_partial_name(
        self, partial: str
    ) -> list[CompanyWithLocale]:
        stmt = select(
            CompanyTranslation.locale, CompanyTranslation.name
        ).where(CompanyTranslation.name.ilike(f"%{partial}%"))

        result = (await self.session.execute(stmt)).all()

        return [
            CompanyWithLocale(locale=locale, name=name)
            for locale, name in result
        ]

    async def get_companies_by_tag_id(self, tag_id: int) -> list[Company]:
        stmt = (
            select(Company)
            .join(CompanyTag)
            .where(CompanyTag.tag_id == tag_id)
            .options(
                selectinload(Company.translations), selectinload(Company.tags)
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def add_tag_on_company(self, name: str, tag_ids: list[int]) -> None:
        stmt = (
            select(Company)
            .join(CompanyTranslation)
            .options(
                selectinload(Company.translations),
                selectinload(Company.tags).selectinload(CompanyTag.tag),
            )
            .where(CompanyTranslation.name == name)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        company = result.scalar_one_or_none()

        if not company:
            return

        existing_tag_ids = {ct.tag_id for ct in company.tags}

        new_tags = [
            CompanyTag(company_id=company.id, tag_id=tag_id)
            for tag_id in tag_ids
            if tag_id not in existing_tag_ids
        ]

        self.session.add_all(new_tags)

    async def delete_tag_of_company(self, name: str, tag_id: int) -> None:
        stmt = (
            select(Company)
            .join(CompanyTranslation)
            .where(CompanyTranslation.name == name)
            .limit(1)
        )
        result = await self.session.execute(stmt)
        company = result.scalar_one_or_none()

        if not company:
            return

        delete_stmt = delete(CompanyTag).where(
            CompanyTag.company_id == company.id, CompanyTag.tag_id == tag_id
        )
        await self.session.execute(delete_stmt)
