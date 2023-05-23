import collections

from fastapi.testclient import TestClient
from peewee import DatabaseProxy, SqliteDatabase
import pytest

from api.main import app
from ..url_shortener import bijective_encode
from ..models import database_proxy, Website

client = TestClient(app)


@pytest.fixture(autouse=True)
def resource():
    with database_proxy:
        database_proxy.create_tables([Website])
        Website.truncate_table(restart_identity=True, cascade=True)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("add/?url="+"http://facebook.com",)
    assert response.status_code == 200
    assert "url" in response.json()

    response = client.get("/")
    assert response.status_code == 200
    assert "id" in response.json()[0]
    assert "title" in response.json()[0]
    assert "url" in response.json()[0]
    assert "short_url" in response.json()[0]


def test_url_shortner():
    encoded_list = []
    for i in range(0, 9999):
        encoded_list.append(bijective_encode(i))
    assert [item for item, count in collections.Counter(encoded_list).items() if count > 1] == []


