from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
        # TODO: Implement this method
        raise NotImplementedError

    async def get_companies_by_tag_id(self, tag_id: int) -> list[Company]:
        # TODO: Implement this method
        raise NotImplementedError

    async def add_tag_on_company(self, name: str, tag_ids: list[int]) -> None:
        # TODO: Implement this method
        raise NotImplementedError

    async def delete_tag_of_company(self, name: str, tag_id: int) -> None:
        # TODO: Implement this method
        raise NotImplementedError
