from pydantic import BaseModel


class TagNameWithLocale(BaseModel):
    name: str
    locale: str


class CreateTagDto(BaseModel):
    tag_name: list[TagNameWithLocale] = []
