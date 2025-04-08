from app.company.dtos import (
    CreateCompanyDto,
    CreateCompanyWithTagDto,
    TagNameWithLocales,
)
from app.company.exceptions import NotFoundCompanyException
from app.company.models import Company
from app.company.repository import CompanyRepository
from app.core.database import transactional
from app.tag.dtos import CreateTagDto, TagNameWithLocale
from app.tag.usecase import TagUsecase


class CompanyUsecase:
    def __init__(
        self, repository: CompanyRepository, tag_usecase: TagUsecase
    ) -> None:
        self.repository = repository
        self.tag_usecase = tag_usecase

    @transactional
    async def create_company(
        self, company_data: CreateCompanyWithTagDto
    ) -> Company:
        tag_dtos = [
            CreateTagDto(
                tag_name=[
                    TagNameWithLocale(name=name.name, locale=name.locale)
                    for name in tag_name_with_locales.names
                ]
            )
            for tag_name_with_locales in company_data.tags
        ]

        tags = await self.tag_usecase.create_tags(tag_dtos)

        company_dto = CreateCompanyDto(
            names=company_data.names,
            tag_ids=[tag.id for tag in tags],
        )
        company = await self.repository.create_company(company_dto)
        return company

    async def get_company_by_name(self, name: str) -> Company:
        company = await self.repository.get_company_by_name(name)
        if not company:
            raise NotFoundCompanyException(
                message=f"Company with name {name} not found."
            )
        return company

    async def get_company_names_by_partial_name(
        self, name: str, locale: str
    ) -> list[str]:
        companies_with_locale = (
            await self.repository.search_companies_with_partial_name(
                partial=name
            )
        )
        return [
            company_with_local.name
            for company_with_local in companies_with_locale
            if company_with_local.locale == locale
        ]

    @transactional
    async def add_tag_on_company(
        self, name: str, tags: list[TagNameWithLocales]
    ) -> None:
        tag_dtos = [
            CreateTagDto(
                tag_name=[
                    TagNameWithLocale(
                        name=tag_name.name, locale=tag_name.locale
                    )
                    for tag_name in tag_name_with_locale.names
                ]
            )
            for tag_name_with_locale in tags
        ]
        created_tags = await self.tag_usecase.create_tags(tag_dtos)
        tag_ids = [tag.id for tag in created_tags]
        await self.repository.add_tag_on_company(name=name, tag_ids=tag_ids)

    @transactional
    async def delete_tag_of_company(self, name: str, tag_name: str) -> None:
        tag = await self.tag_usecase.get_tag_by_name(name=tag_name)
        await self.repository.delete_tag_of_company(name=name, tag_id=tag.id)
