from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.company.models import Company, CompanyTag
from app.query.dtos import CompanyInfoWithLocale, CompanyWithTags
from app.tag.models import Tag, TagTranslation


class QueryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_companies_info(
        self, company_ids: list[int]
    ) -> list[CompanyInfoWithLocale]:
        stmt = (
            select(Company)
            .where(Company.id.in_(company_ids))
            .options(
                selectinload(Company.translations),
                selectinload(Company.tags)
                .selectinload(CompanyTag.tag)
                .selectinload(Tag.translations),
            )
        )

        companies = (await self.session.execute(stmt)).unique().scalars().all()
        return self.make_companies_into_company_info(companies)

    async def get_companies_by_tag_name(
        self, tag_name: str
    ) -> list[CompanyInfoWithLocale]:
        tag_stmt = (
            select(Tag)
            .join(TagTranslation)
            .options(selectinload(Tag.translations))
            .where(TagTranslation.name == tag_name)
        )
        tag_result = await self.session.execute(tag_stmt)
        tag = tag_result.scalars().first()

        if not tag:
            return []

        company_stmt = (
            select(Company)
            .join(CompanyTag)
            .where(CompanyTag.tag_id == tag.id)
            .options(
                selectinload(Company.translations),
                selectinload(Company.tags)
                .selectinload(CompanyTag.tag)
                .selectinload(Tag.translations),
            )
        )
        companies = (
            (await self.session.execute(company_stmt)).unique().scalars().all()
        )

        return self.make_companies_into_company_info(companies)

    def make_companies_into_company_info(
        self, companies: list[Company]
    ) -> list[CompanyInfoWithLocale]:
        result: list[CompanyInfoWithLocale] = []

        for company in companies:
            for translation in company.translations:
                tag_names = []
                for ct in company.tags:
                    tag = ct.tag
                    tag_name: str | None = next(
                        (
                            t.name
                            for t in tag.translations
                            if t.locale == translation.locale
                        ),
                        None,
                    )
                    if tag_name:
                        tag_names.append(tag_name)

                result.append(
                    CompanyInfoWithLocale(
                        locale=translation.locale,
                        company_info=CompanyWithTags(
                            id=company.id,
                            name=translation.name,
                            tags=tag_names,
                        ),
                    )
                )

        return result
