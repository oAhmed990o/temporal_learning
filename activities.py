from temporalio import activity
from dataclasses import dataclass
import os

@dataclass
class Item:
    item_name: str
    price: float

@dataclass
class Order:
    order_id: str
    client_name: str
    card_number: str
    items: list[Item]

@activity.defn
async def place_order(order: Order) -> float:
    print(f"place order start: {os.getpid()}")
    total_price = 0
    # just symbolic check
    if isinstance(order.card_number, str):
         for item in order.items:
            total_price += item.price

    print(f"place order end: {os.getpid()}")
    return total_price

@activity.defn
async def charge_payment(order: Order, total_price: float) -> bool:
    # some symbolic checks
    print(f"charge payment: {os.getpid()}")
    return (total_price != 0 and isinstance(order.card_number, str))

@activity.defn
async def confirmation(response) -> bool:
    # ensure charge payment went well and return confirmation
    print(f"confirmation: {os.getpid()}")
    return response