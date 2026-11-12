class OrderRepository:
    def __init__(self, orders: dict[int, str] | None = None) -> None:
        self._orders = dict(orders) if orders is not None else {}

    def get_status(self, order_id: int) -> str | None:
        return self._orders.get(order_id)

    def cancel(self, order_id: int) -> None:
        self._orders[order_id] = "CANCELLED"