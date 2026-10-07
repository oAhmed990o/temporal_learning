from temporalio import activity
from dataclasses import dataclass
import os
import json

FILE = "charges.json"

def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

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
    print(f"place order: {os.getpid()}")
    total_price = 0
    # just symbolic check
    if isinstance(order.card_number, str):
         for item in order.items:
            total_price += item.price

    return total_price

@activity.defn
async def charge_payment(order: Order, total_price: float) -> bool:
    data = load()

    order_id = order.order_id

    if order_id in data:
        print("ALREADY CHARGED, skipping")
        return data[order_id]

    attempts = activity.info().attempt
    print(f"charge payment | pid : {os.getpid()} | attempt no. : {attempts} | order id : {order_id} ")
    # some symbolic checks
    result = (total_price != 0 and isinstance(order.card_number, str))
    data[order_id] = result
    save(data)

    if attempts == 1:
        raise RuntimeError("simulated crash after charge")
    
    return result

@activity.defn
async def confirmation(response) -> bool:
    # ensure charge payment went well and return confirmation
    print(f"confirmation: {os.getpid()}")
    return response