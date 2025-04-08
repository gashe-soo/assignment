from app.company.dtos import CompanyWithLocale, CreateCompanyDto
from app.company.models import Company


class CompanyRepository:
    async def create_company(self, company_data: CreateCompanyDto) -> Company:
        # TODO: Implement this method
        raise NotImplementedError

    async def get_company_by_name(self, name: str) -> Company | None:
        # TODO: Implement this method
        raise NotImplementedError

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
