import pytest

from fastapi.testclient import TestClient
from app.tests.conftest import SessionTesting


def test_assert_true(db: SessionTesting, client: TestClient):
    assert True
