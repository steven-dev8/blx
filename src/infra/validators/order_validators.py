from src.schema.schemas import OrderCreate
from fastapi import status, HTTPException


def quantity_check(qnt_order: int, qnt_product: int):
    return qnt_order <= qnt_product


def additional_check(order: OrderCreate, product: int):
    address = len(order.address.strip()) >= 10
    if not address:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address length must exceed 10 characters."
            )
    if not quantity_check(order.quantity, product):
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The order quantity exceeds the avaliable stock."
            )