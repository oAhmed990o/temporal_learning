import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow
import os

with workflow.unsafe.imports_passed_through():
    from workflows import OrderPlacementWorkflow
    from activities import place_order, charge_payment, confirmation

async def main():
    client = await Client.connect("localhost:7233")

    order_worker = Worker(
        client,
        task_queue="order-task-queue",
        workflows=[OrderPlacementWorkflow],
        activities=[place_order, charge_payment, confirmation],
    )

    print(f"order worker started: {os.getpid()}")

    await asyncio.gather(
        order_worker.run(),
    )

if __name__ == "__main__":
    asyncio.run(main())