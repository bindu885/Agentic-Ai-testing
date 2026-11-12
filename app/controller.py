from fastapi import FastAPI, HTTPException

from app.service import OrderCannotBeCancelled, OrderNotFound, OrderService


def create_app(service: OrderService) -> FastAPI:
    app = FastAPI(title="Order review sample")

    @app.post(
        "/orders/{order_id}/cancel",
        summary="Cancel an order that has not shipped",
        responses={
            404: {"description": "The order does not exist"},
            409: {"description": "The order has already shipped"},
        },
    )
    def cancel_order(order_id: int) -> dict[str, str]:
        try:
            status = service.cancel_order(order_id)
        except OrderNotFound as error:
            raise HTTPException(
                status_code=404,
                detail={"code": "ORDER_NOT_FOUND", "message": str(error)},
            ) from error
        except OrderCannotBeCancelled as error:
            raise HTTPException(
                status_code=409,
                detail={"code": "ORDER_ALREADY_SHIPPED", "message": str(error)},
            ) from error
        return {"status": status}

    return app