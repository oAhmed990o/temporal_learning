import asyncio
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

policy = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    maximum_attempts=5,
)

with workflow.unsafe.imports_passed_through():
    from activities import place_order, charge_payment, confirmation

@workflow.defn
class OrderPlacementWorkflow:
    @workflow.run
    async def run(self, order):
        placed = await workflow.execute_activity(
            place_order,
            order,
            start_to_close_timeout=timedelta(seconds=10),
        )

        await workflow.sleep(timedelta(seconds=10))

        charged = await workflow.execute_activity(
            charge_payment,
            args=[order, placed],
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=policy
        )

        await workflow.sleep(timedelta(seconds=10))

        workflow.logger.info(f"placed={placed!r} type={type(placed)}")
        confirmed = await workflow.execute_activity(
            confirmation,
            charged,
            start_to_close_timeout=timedelta(seconds=10),
        )

        if confirmed:
            print("order succesful")
        else:
            print("failed to purchase order")