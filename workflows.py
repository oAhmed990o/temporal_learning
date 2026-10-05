import asyncio
from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import place_order, charge_payment, confirmation

@workflow.defn
class OrderPlacementWorkflow:
    @workflow.run
    async def run(self, order) -> str:
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
        )

        await workflow.sleep(timedelta(seconds=10))

        workflow.logger.info(f"placed={placed!r} type={type(placed)}")
        confirmed = await workflow.execute_activity(
            confirmation,
            charged,
            start_to_close_timeout=timedelta(seconds=10),
        )
        

        print(confirmed)
        return "confirmed"

        # if results:
        #     return "order succesful"

        # return "failed to purchase order"