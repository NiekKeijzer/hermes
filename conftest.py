import pytest
import shutil
import datetime
from typing import Any, Generator

from django.conf import settings


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db: Any) -> None:
    pass


@pytest.fixture()
def tmp_directory() -> Generator:
    tmp_directory = settings.VAR_DIR / "tests"
    tmp_directory.mkdir(0o755, parents=True)

    yield tmp_directory
    shutil.rmtree(tmp_directory)


@pytest.fixture()
def date() -> datetime.datetime:
    return datetime.datetime(1990, 8, 9, 14, 25, 15)
