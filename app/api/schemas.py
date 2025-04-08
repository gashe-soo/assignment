from pydantic import BaseModel


class CompanyNameWithLocales(BaseModel):
    ko: str
    en: str
    tw: str | None = None
    jp: str | None = None


class TagNameWithLocaleRequest(BaseModel):
    tag_name: dict[str, str]


class CreateCompanyRequestDto(BaseModel):
    company_name: dict[str, str]
    tags: list[TagNameWithLocaleRequest]


class CompanyResponse(BaseModel):
    company_name: str
    tags: list[str]


class AutocompleteCompanyResponse(BaseModel):
    company_name: str
