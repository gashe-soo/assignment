from pydantic import BaseModel


class CompanyWithTags(BaseModel):
    id: int
    name: str
    tags: list[str]


class CompanyInfoWithLocale(BaseModel):
    locale: str
    company_info: CompanyWithTags
