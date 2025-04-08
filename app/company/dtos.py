from pydantic import BaseModel


class NameWithLocale(BaseModel):
    name: str
    locale: str


class CreateCompanyDto(BaseModel):
    names: list[NameWithLocale] = []
    tag_ids: list[int] = []


class CompanyWithLocale(BaseModel):
    locale: str
    name: str
