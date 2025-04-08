from fastapi import APIRouter, Depends, Header

from app.api.schemas import (
    AutocompleteCompanyResponse,
    CompanyResponse,
    CreateCompanyRequestDto,
    TagNameWithLocaleRequest,
)
from app.company.dtos import (
    CreateCompanyWithTagDto,
    NameWithLocale,
    TagNameWithLocales,
)
from app.company.usecase import CompanyUsecase
from app.dependencies import get_company_usecase, get_query_usecase
from app.query.usecase import QueryUsecase

router = APIRouter()


@router.get("/search", response_model=list[AutocompleteCompanyResponse])
async def autocomplete_company(
    query: str,
    x_wanted_language: str = Header(...),
    company_usecase: CompanyUsecase = Depends(get_company_usecase),
) -> list[AutocompleteCompanyResponse]:
    results = await company_usecase.get_company_names_by_partial_name(
        name=query, locale=x_wanted_language
    )
    return [AutocompleteCompanyResponse(company_name=name) for name in results]


@router.get("/companies/{company_name}", response_model=CompanyResponse)
async def get_company(
    company_name: str,
    x_wanted_language: str = Header(...),
    company_usecase: CompanyUsecase = Depends(get_company_usecase),
    query_usecase: QueryUsecase = Depends(get_query_usecase),
) -> CompanyResponse:
    company = await company_usecase.get_company_by_name(company_name)
    result = await query_usecase.get_companies_info(
        company_ids=[company.id], locale=x_wanted_language
    )
    return CompanyResponse(company_name=result[0].name, tags=result[0].tags)


@router.post("/companies", response_model=CompanyResponse)
async def create_company(
    data: CreateCompanyRequestDto,
    x_wanted_language: str = Header(...),
    company_usecase: CompanyUsecase = Depends(get_company_usecase),
    query_usecase: QueryUsecase = Depends(get_query_usecase),
) -> CompanyResponse:
    company_dto = CreateCompanyWithTagDto(
        names=[
            NameWithLocale(name=name, locale=locale)
            for locale, name in data.company_name.items()
        ],
        tags=[
            TagNameWithLocales(
                names=[
                    NameWithLocale(name=name, locale=locale)
                    for locale, name in tag.tag_name.items()
                ]
            )
            for tag in data.tags
        ],
    )
    company = await company_usecase.create_company(company_dto)
    result = await query_usecase.get_companies_info(
        company_ids=[company.id], locale=x_wanted_language
    )
    return CompanyResponse(company_name=result[0].name, tags=result[0].tags)


@router.put("/companies/{company_name}/tags", response_model=CompanyResponse)
async def add_tags(
    company_name: str,
    data: list[TagNameWithLocaleRequest],
    x_wanted_language: str = Header(...),
    company_usecase: CompanyUsecase = Depends(get_company_usecase),
    query_usecase: QueryUsecase = Depends(get_query_usecase),
) -> CompanyResponse:
    tag_list = [
        TagNameWithLocales(
            names=[
                NameWithLocale(name=name, locale=locale)
                for locale, name in tag.tag_name.items()
            ]
        )
        for tag in data
    ]
    await company_usecase.add_tag_on_company(company_name, tag_list)
    company = await company_usecase.get_company_by_name(company_name)
    result = await query_usecase.get_companies_info(
        company_ids=[company.id], locale=x_wanted_language
    )
    return CompanyResponse(company_name=result[0].name, tags=result[0].tags)


@router.delete(
    "/companies/{company_name}/tags/{tag_name}", response_model=CompanyResponse
)
async def delete_tag(
    company_name: str,
    tag_name: str,
    x_wanted_language: str = Header(...),
    company_usecase: CompanyUsecase = Depends(get_company_usecase),
    query_usecase: QueryUsecase = Depends(get_query_usecase),
) -> CompanyResponse:
    await company_usecase.delete_tag_of_company(company_name, tag_name)
    company = await company_usecase.get_company_by_name(company_name)
    result = await query_usecase.get_companies_info(
        company_ids=[company.id], locale=x_wanted_language
    )
    return CompanyResponse(company_name=result[0].name, tags=result[0].tags)


@router.get("/tags", response_model=list[CompanyResponse])
async def get_tag(
    query: str,
    x_wanted_language: str = Header(...),
    query_usecase: QueryUsecase = Depends(get_query_usecase),
) -> list[CompanyResponse]:
    result = await query_usecase.get_companies_by_tag_name(
        tag_name=query, locale=x_wanted_language
    )
    return [
        CompanyResponse(company_name=res.name, tags=res.tags) for res in result
    ]
