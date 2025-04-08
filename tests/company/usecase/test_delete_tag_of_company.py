import pytest

from app.company.usecase import CompanyUsecase
from app.tag.models import Tag


@pytest.mark.asyncio
async def test_delete_tag_of_company_should_find_tag_and_delete(
    usecase: CompanyUsecase,
):
    # Given
    tag = Tag(id=42)
    usecase.tag_usecase.get_tag_by_name.return_value = tag

    # When
    await usecase.delete_tag_of_company(name="라인", tag_name="기술")

    # Then
    usecase.tag_usecase.get_tag_by_name.assert_awaited_once_with(name="기술")
    usecase.repository.delete_tag_of_company.assert_awaited_once_with(
        name="라인", tag_id=42
    )
