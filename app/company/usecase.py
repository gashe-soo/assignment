from app.company.dtos import CreateCompanyDto, NameWithLocale
from app.company.models import Company


class CompanyUsecase:
    def create_company(
        self, company_data: CreateCompanyDto, locale: str
    ) -> Company:
        # TODO: Implemnnt this method
        raise NotImplementedError

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
