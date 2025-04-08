from app.company.dtos import (
    CreateCompanyDto,
    CreateCompanyWithTagDto,
    NameWithLocale,
)
from app.company.models import Company
from app.company.repository import CompanyRepository
from app.tag.dtos import CreateTagDto, TagNameWithLocale
from app.tag.usecase import TagUsecase


class CompanyUsecase:
    def __init__(
        self, repository: CompanyRepository, tag_usecase: TagUsecase
    ) -> None:
        self.repository = repository
        self.tag_usecase = tag_usecase

    async def create_company(
        self, company_data: CreateCompanyWithTagDto, locale: str
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

    async def get_company_by_name(self, name: str, locale: str) -> Company:
        # TODO: Implement this method
        raise NotImplementedError

    async def get_company_names_by_partial_name(
        self, name: str, locale: str
    ) -> list[str]:
        # TODO: Implemnt this method
        raise NotImplementedError

    async def add_tag_on_company(
        self, name: str, tags: list[NameWithLocale]
    ) -> None:
        # TODO: Implement this method
        raise NotImplementedError

    async def delete_tag_of_company(
        self, name: str, tag_name: str, locale: str
    ) -> None:
        # TODO: Implement this method
        raise NotImplementedError
