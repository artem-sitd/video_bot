from pydantic import BaseModel
from typing import Optional

class QueryFilters(BaseModel):
    creator_id: Optional[int] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    views_gt: Optional[int] = None

class ParsedQuery(BaseModel):
    intent: str
    filters: QueryFilters
