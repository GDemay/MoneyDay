from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.stock import create_random_stock


def test_create_stock(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "CompanyX", "ticker": "CMPX"}
    response = client.post(
        f"{settings.API_V1_STR}/stocks/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["ticker"] == data["ticker"]
    assert "id" in content


def test_read_stock(client: TestClient, db: Session) -> None:
    stock = create_random_stock(db)
    response = client.get(
        f"{settings.API_V1_STR}/stocks/{stock.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == stock.name
    assert content["ticker"] == stock.ticker
    assert content["id"] == stock.id


def test_read_stock_not_found(client: TestClient) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/stocks/999",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Stock not found"


def test_read_stocks(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_stock(db)
    create_random_stock(db)
    response = client.get(
        f"{settings.API_V1_STR}/stocks/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_stock(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    stock = create_random_stock(db)
    data = {"name": "Updated Company", "ticker": "UPDC"}
    response = client.put(
        f"{settings.API_V1_STR}/stocks/{stock.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["ticker"] == data["ticker"]
    assert content["id"] == stock.id


def test_update_stock_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Nonexistent Corp", "ticker": "NONE"}
    response = client.put(
        f"{settings.API_V1_STR}/stocks/999",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Stock not found"


def test_delete_stock(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    stock = create_random_stock(db)
    response = client.delete(
        f"{settings.API_V1_STR}/stocks/{stock.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Stock deleted successfully"


def test_delete_stock_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/stocks/999",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Stock not found"
