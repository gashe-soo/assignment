from pydantic import BaseModel


class NameWithLocale(BaseModel):
    name: str
    locale: str


class CreateCompanyDto(BaseModel):
    names: list[NameWithLocale] = []
    tag_ids: list[int] = []


class TagNameWithLocales(BaseModel):
    names: list[NameWithLocale] = []


class CreateCompanyWithTagDto(BaseModel):
    names: list[NameWithLocale] = []
    tags: list[TagNameWithLocales] = []


class CompanyWithLocale(BaseModel):
    locale: str
    name: str
