from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.company.repository import CompanyRepository
from app.company.usecase import CompanyUsecase
from app.core.database import get_db
from app.query.repository import QueryRepository
from app.query.usecase import QueryUsecase
from app.tag.repository import TagRepository
from app.tag.usecase import TagUsecase


async def get_company_usecase(
    session: AsyncSession = Depends(get_db),
) -> CompanyUsecase:
    return CompanyUsecase(
        repository=CompanyRepository(session),
        tag_usecase=TagUsecase(repository=TagRepository(session=session)),
    )


async def get_query_usecase(
    session: AsyncSession = Depends(get_db),
) -> QueryUsecase:
    return QueryUsecase(repository=QueryRepository(session=session))
