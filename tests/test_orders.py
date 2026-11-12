import pytest
from fastapi.testclient import TestClient

from app.controller import create_app
from app.labels import add_label
from app.repository import OrderRepository
from app.service import OrderService


@pytest.fixture
def order_api():
    repository = OrderRepository({1: "PENDING", 2: "SHIPPED"})
    with TestClient(create_app(OrderService(repository))) as client:
        yield client, repository


def test_cancel_pending_order(order_api):
    client, repository = order_api
    response = client.post("/orders/1/cancel")
    assert response.status_code == 200
    assert response.json() == {"status": "CANCELLED"}
    assert repository.get_status(1) == "CANCELLED"


def test_shipped_order_cannot_be_cancelled(order_api):
    client, repository = order_api
    response = client.post("/orders/2/cancel")
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "ORDER_ALREADY_SHIPPED"
    assert repository.get_status(2) == "SHIPPED"


def test_missing_order_uses_standard_error_schema(order_api):
    client, repository = order_api
    response = client.post("/orders/999/cancel")
    assert response.status_code == 404
    assert response.json()["detail"] == {
        "code": "ORDER_NOT_FOUND", "message": "Order not found",
    }
    assert repository.get_status(999) is None


def test_cancel_endpoint_is_documented(order_api):
    client, _repository = order_api
    operation = client.get("/openapi.json").json()["paths"]["/orders/{order_id}/cancel"]["post"]
    assert operation["summary"] == "Cancel an order that has not shipped"
    assert {"200", "404", "409"} <= operation["responses"].keys()


def test_default_labels_are_not_shared():
    assert add_label("first") == ["first"]
    assert add_label("second") == ["second"]


def test_existing_labels_are_updated():
    labels = ["first"]
    assert add_label("second", labels) is labels
    assert labels == ["first", "second"]