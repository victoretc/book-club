import os
from typing import Any, cast

import pytest
from faker import Faker

from app.testing.httpx_client import Client, Configuration
from clients.http.book_club import AuthApi, ClubsApi, UsersApi
from clients.http.book_club.models.api_models import PatchedClub, TokenObtainPairWithProperMessage, UserRegister


fake = Faker()


@pytest.fixture
def configuration() -> Configuration:
    return Configuration(base_url=cast(str, os.getenv("BASE_TEST_URL")))


@pytest.fixture
def as_anon(configuration: Configuration) -> Client:
    return Client(configuration)


@pytest.fixture
def auth_api(as_anon: Client) -> AuthApi:
    return AuthApi(as_anon)


@pytest.fixture
def anon_users_api(as_anon: Client) -> UsersApi:
    return UsersApi(as_anon)


@pytest.fixture
def user(anon_users_api: UsersApi, auth_api: AuthApi, user_request_data) -> dict[str, Any]:
    user = anon_users_api.post_api_v1_users_register_with_http_info(user_register=UserRegister(**user_request_data))

    assert user.status_code == 201

    token = auth_api.post_api_v1_auth_token_with_http_info(TokenObtainPairWithProperMessage(**user_request_data))

    return {"token": token.json()["access"], "response": user.json(), "id": user.json()["id"]}


@pytest.fixture
def as_user(user) -> Client:
    config = Configuration(
        base_url=cast(str, os.getenv("BASE_TEST_URL")),
        headers={"Authorization": f"Bearer {user['token']}", "X-Client": "testing"},
    )
    return Client(config)


@pytest.fixture(autouse=True)
def delete_user_from_db(authenticated_users_api: UsersApi):
    yield

    got = authenticated_users_api.delete_api_v1_users_me_with_http_info()
    assert got.status_code == 204


@pytest.fixture
def authenticated_users_api(as_user):
    return UsersApi(as_user)


@pytest.fixture
def authenticated_clubs_api(as_user):
    return ClubsApi(as_user)


@pytest.fixture
def anon_clubs_api(as_anon):
    return ClubsApi(as_anon)


@pytest.fixture
def club_request_data():
    return {
        "bookTitle": f"{fake.unique.name()}_{os.getpid()}",
        "bookAuthors": "string",
        "publicationYear": fake.year(),
        "description": fake.text(),
        "telegramChatLink": fake.url(),
    }


@pytest.fixture
def club(authenticated_clubs_api: ClubsApi, club_request_data):
    got = authenticated_clubs_api.post_api_v1_clubs_with_http_info(PatchedClub(**club_request_data))  # type: ignore[arg-type]
    assert got.status_code == 201
    return got
