from app.controller import create_app
from app.repository import OrderRepository
from app.service import OrderService

app = create_app(OrderService(OrderRepository({1: "PENDING", 2: "SHIPPED"})))