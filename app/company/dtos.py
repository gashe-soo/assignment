from pydantic import BaseModel

from app.tag.models import Tag


class NameWithLocale(BaseModel):
    name: str
    locale: str


class CreateCompanyDto(BaseModel):
    names: list[NameWithLocale] = []
    tags: list[Tag] = []


class CompanyWithLocale(BaseModel):
    locale: str
    name: str
