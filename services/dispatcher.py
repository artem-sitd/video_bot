from llm.schemas import QueryPlan
from db.queries import execute_query_plan


async def dispatch_query(plan_dict: QueryPlan) -> int:
    dump = plan_dict.model_dump()
    print(dump)
    return await execute_query_plan(dump)
