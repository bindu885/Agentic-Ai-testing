from app.repository import OrderRepository


class OrderNotFound(ValueError):
    pass


class OrderCannotBeCancelled(ValueError):
    pass


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def cancel_order(self, order_id: int) -> str:
        status = self.repository.get_status(order_id)
        if status is None:
            raise OrderNotFound("Order not found")
        if status == "SHIPPED":
            raise OrderCannotBeCancelled("Shipped orders cannot be cancelled")
        self.repository.cancel(order_id)
        return "CANCELLED"