from app.query.dtos import CompanyInfoWithLocale


class QueryRepository:
    async def get_companies_info(
        self, company_ids: list[int]
    ) -> list[CompanyInfoWithLocale]:
        # TODO: Implement this method
        raise NotImplementedError

    async def get_companies_by_tag_names(
        self, tag_name: str
    ) -> list[CompanyInfoWithLocale]:
        # TODO: Implement this method
        raise NotImplementedError
