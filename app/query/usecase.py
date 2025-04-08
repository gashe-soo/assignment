from collections import defaultdict

from app.query.dtos import CompanyInfoWithLocale, CompanyWithTags
from app.query.repository import QueryRepository


class QueryUsecase:
    def __init__(self, repository: QueryRepository):
        self.repository = repository

    async def get_companies_info(
        self, company_ids: list[int], locale: str
    ) -> list[CompanyWithTags]:
        company_infos = await self.repository.get_companies_info(company_ids)
        return self._filter_by_locale_with_fallback(company_infos, locale)

    async def get_companies_by_tag_name(
        self, tag_name: str, locale: str
    ) -> list[CompanyWithTags]:
        company_infos = await self.repository.get_companies_by_tag_name(
            tag_name
        )
        return self._filter_by_locale_with_fallback(company_infos, locale)

    def _filter_by_locale_with_fallback(
        self, infos: list[CompanyInfoWithLocale], locale: str
    ) -> list[CompanyWithTags]:
        grouped = defaultdict(list)

        for info in infos:
            grouped[info.company_info.id].append(info)

        result: list[CompanyWithTags] = []

        for company_id, localized_infos in grouped.items():
            exact = next(
                (i for i in localized_infos if i.locale == locale), None
            )
            if exact:
                result.append(exact.company_info)
            else:
                result.append(localized_infos[0].company_info)

        return result
