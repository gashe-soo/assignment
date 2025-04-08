import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from starlette import status

from app.company.models import Company, CompanyTag, CompanyTranslation
from app.core.enums import Locale
from app.dependencies import get_db
from app.main import app
from app.tag.models import Tag, TagTranslation


@pytest_asyncio.fixture(autouse=True)
async def _override_get_db(session):
    async def _get_override():
        yield session

    app.dependency_overrides[get_db] = _get_override


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_company_name_autocomplete(client, session):
    # Given
    company1 = Company()
    company1.translations = [
        CompanyTranslation(name="주식회사 링크드코리아", locale=Locale.KO),
    ]

    company2 = Company()
    company2.translations = [
        CompanyTranslation(name="스피링크", locale=Locale.KO),
    ]
    company3 = Company()
    company3.translations = [
        CompanyTranslation(name="링드인", locale=Locale.KO),
    ]

    session.add_all([company1, company2])
    await session.commit()

    # When
    resp = await client.get(
        "/search?query=링크", headers={"x-wanted-language": "ko"}
    )

    # Then
    assert resp.status_code == status.HTTP_200_OK
    searched_companies = resp.json()
    assert searched_companies == [
        {"company_name": "주식회사 링크드코리아"},
        {"company_name": "스피링크"},
    ]


@pytest.mark.asyncio
async def test_company_search(client, session):
    # Given: 태그 3개 생성
    tag_4 = Tag()
    tag_4.translations = [
        TagTranslation(name="태그_4", locale=Locale.KO),
        TagTranslation(name="tag_4", locale=Locale.EN),
    ]
    tag_20 = Tag()
    tag_20.translations = [
        TagTranslation(name="태그_20", locale=Locale.KO),
        TagTranslation(name="tag_20", locale=Locale.EN),
    ]
    tag_16 = Tag()
    tag_16.translations = [
        TagTranslation(name="태그_16", locale=Locale.KO),
        TagTranslation(name="tag_16", locale=Locale.EN),
    ]

    session.add_all([tag_4, tag_20, tag_16])
    await session.flush()

    company = Company()
    company.translations = [
        CompanyTranslation(name="원티드랩", locale=Locale.KO),
        CompanyTranslation(name="Wantedlab", locale=Locale.EN),
    ]
    company.tags = [
        CompanyTag(tag_id=tag_4.id),
        CompanyTag(tag_id=tag_20.id),
        CompanyTag(tag_id=tag_16.id),
    ]

    session.add(company)
    await session.commit()

    # When
    resp = await client.get(
        "/companies/Wantedlab", headers={"x-wanted-language": "ko"}
    )

    # Then
    assert resp.status_code == status.HTTP_200_OK
    company = resp.json()
    assert company == {
        "company_name": "원티드랩",
        "tags": ["태그_4", "태그_20", "태그_16"],
    }


@pytest.mark.asyncio
async def test_company_search_returns_404_when_no_exist(client):
    # When
    resp = await client.get(
        "/companies/없는회사", headers={"x-wanted-language": "ko"}
    )

    # Then
    assert resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_new_company(client):
    # When
    resp = await client.post(
        "/companies",
        json={
            "company_name": {
                "ko": "라인 프레쉬",
                "tw": "LINE FRESH",
                "en": "LINE FRESH",
            },
            "tags": [
                {"tag_name": {"ko": "태그_1", "tw": "tag_1", "en": "tag_1"}},
                {"tag_name": {"ko": "태그_8", "tw": "tag_8", "en": "tag_8"}},
                {"tag_name": {"ko": "태그_15", "tw": "tag_15", "en": "tag_15"}},
            ],
        },
        headers={"x-wanted-language": "tw"},
    )

    # Then
    assert resp.status_code == status.HTTP_200_OK
    company = resp.json()
    assert company == {
        "company_name": "LINE FRESH",
        "tags": ["tag_1", "tag_8", "tag_15"],
    }


@pytest.mark.asyncio
async def test_search_tag_name(client, session):
    # Given: "タグ_22"를 가진 태그 생성 (jp locale)
    tag = Tag()
    tag.translations = [
        TagTranslation(locale=Locale.JP, name="タグ_22"),
        TagTranslation(locale=Locale.KO, name="태그_22"),
        TagTranslation(locale=Locale.EN, name="tag_22"),
    ]
    session.add(tag)
    await session.flush()

    company_names = [
        (Locale.KO, "딤딤섬 대구점"),
        (Locale.KO, "마이셀럽스"),
        (Locale.EN, "Rejoice Pregnancy"),
        (Locale.KO, "삼일제약"),
        (Locale.KO, "투게더앱스"),
    ]

    companies = []
    for locale, name in company_names:
        company = Company()
        company.translations = [
            CompanyTranslation(locale=locale, name=name),
        ]
        company.tags = [CompanyTag(tag_id=tag.id)]
        companies.append(company)

    session.add_all(companies)
    await session.commit()

    # When
    resp = await client.get(
        "/tags?query=タグ_22", headers={"x-wanted-language": "ko"}
    )

    # Then
    assert resp.status_code == status.HTTP_200_OK
    searched_companies = resp.json()
    assert sorted([c["company_name"] for c in searched_companies]) == sorted(
        [
            "딤딤섬 대구점",
            "마이셀럽스",
            "Rejoice Pregnancy",
            "삼일제약",
            "투게더앱스",
        ]
    )


@pytest.mark.asyncio
async def test_new_tag(client, session):
    tags = []
    for name in ["태그_4", "태그_16", "태그_20"]:
        tag = Tag()
        tag.translations = [
            TagTranslation(locale=Locale.KO, name=name),
            TagTranslation(locale=Locale.EN, name=name.replace("태그_", "tag_")),
        ]
        tags.append(tag)
    session.add_all(tags)
    await session.flush()

    company = Company()
    company.translations = [
        CompanyTranslation(name="원티드랩", locale=Locale.KO),
        CompanyTranslation(name="Wantedlab", locale=Locale.EN),
    ]
    company.tags = [CompanyTag(tag_id=tag.id) for tag in tags]
    session.add(company)
    await session.commit()

    # When
    resp = await client.put(
        "/companies/원티드랩/tags",
        json=[
            {"tag_name": {"ko": "태그_50", "jp": "タグ_50", "en": "tag_50"}},
            {"tag_name": {"ko": "태그_4", "tw": "tag_4", "en": "tag_4"}},
        ],
        headers={"x-wanted-language": "en"},
    )

    # Then
    assert resp.status_code == status.HTTP_200_OK
    company = resp.json()
    assert company["company_name"] == "Wantedlab"
    assert sorted(company["tags"]) == sorted(
        ["tag_4", "tag_16", "tag_20", "tag_50"]
    )


@pytest.mark.asyncio
async def test_delete_tag(client, session):
    tags = []
    for name in ["태그_4", "태그_16", "태그_20", "태그_50"]:
        tag = Tag()
        tag.translations = [
            TagTranslation(locale=Locale.KO, name=name),
            TagTranslation(locale=Locale.EN, name=name.replace("태그_", "tag_")),
        ]
        tags.append(tag)
    session.add_all(tags)
    await session.flush()

    company = Company()
    company.translations = [
        CompanyTranslation(name="원티드랩", locale=Locale.KO),
        CompanyTranslation(name="Wantedlab", locale=Locale.EN),
    ]
    company.tags = [CompanyTag(tag_id=tag.id) for tag in tags]
    session.add(company)
    await session.commit()

    # When
    resp = await client.delete(
        "/companies/원티드랩/tags/태그_16", headers={"x-wanted-language": "en"}
    )

    # Then
    assert resp.status_code == status.HTTP_200_OK
    company = resp.json()
    assert company == {
        "company_name": "Wantedlab",
        "tags": ["tag_4", "tag_20", "tag_50"],
    }
