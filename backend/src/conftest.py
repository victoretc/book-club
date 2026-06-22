import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

import allure
import pytest
from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from dotenv import load_dotenv
from faker import Faker

from clients.http.book_club.models.api_models import UserRegister


fake = Faker()

pytest_plugins = ["users.fixtures"]


def allure_logger(config: pytest.Config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: pytest.FixtureDef, request: pytest.FixtureRequest) -> Generator[None, Any, None]:
    yield
    logger: AllureReporter = allure_logger(request.config)
    item: pytest.Item = logger.get_last_item()  # type:ignore [no-untyped-call]
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    if call.when == "call":
        test_name = item.name.replace("test_", "").replace("_", " ").capitalize()
        allure.dynamic.title(test_name)  # type: ignore[no-untyped-call]


@pytest.fixture
def user_request_data() -> dict[Any, Any]:
    username = f"{fake.unique.user_name()}_{os.getpid()}"
    password = fake.password()

    return UserRegister(username=username, password=password).model_dump()


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    env_file = Path(__file__).parent / "env" / ".env"

    if Path.exists(env_file):
        load_dotenv(env_file)
    else:
        raise FileNotFoundError(f"Env файл {env_file} не найден")
