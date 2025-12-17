from pydantic import BaseModel
from typing import List, Literal, Union, Optional


class Filter(BaseModel):
    field: str
    op: Literal["=", ">", "<", ">=", "<=", "between"]
    value: Union[str, int, List[str]]


class Select(BaseModel):
    type: Literal["aggregate"]
    func: Literal["count", "sum"]
    field: Literal["id", "views_count", "delta_views_count", "creator_id", "video_created_at"]
    distinct: Optional[bool] = False


class QueryPlan(BaseModel):
    source: Literal["videos", "snapshots"]
    select: Select
    filters: List[Filter] = []
    distinct: bool = False
