import asyncio
import uuid
from temporalio.client import Client

from activities import Order, Item

async def main():
    client = await Client.connect("localhost:7233")

    item1 = Item(
        "gold",
        4560.94
    )

    item2 = Item(
        "silver",
        280.32
    )

    jewellery_order = Order(
        "001-021",
        "ahmed",
        "1234-5678-1234-5678",
        [item1, item2]
    )

    order_placed = await client.execute_workflow(
        "OrderPlacementWorkflow",
        jewellery_order,
        id=f"order-placement-workflow-{uuid.uuid4()}",
        task_queue="order-task-queue",
    )
    print("order placed:", order_placed)

if __name__ == "__main__":
    asyncio.run(main())