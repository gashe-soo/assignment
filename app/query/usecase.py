from app.query.dtos import CompanyWithTags


class QueryUsecase:
    async def get_companies_info(
        self, company_ids: list[int], locale: str
    ) -> list[CompanyWithTags]:
        # TODO: Implement this method
        raise NotImplementedError

    async def get_companies_by_tag_name(
        self, tag_name: str, locale: str
    ) -> list[CompanyWithTags]:
        # TODO: Implement this method
        raise NotImplementedError
