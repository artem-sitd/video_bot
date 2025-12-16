from pydantic import BaseModel
from typing import Literal
from datetime import date
from enum import Enum
from datetime import time


class Intent(str, Enum):
    count_videos = "count_videos"
    sum_views_delta = "sum_views_delta"
    count_videos_with_views_gt = "count_videos_with_views_gt"
    count_videos_with_new_views = "count_videos_with_new_views"
    count_snapshots = "count_snapshots"


class Filters(BaseModel):
    creator_id: str | None
    date_from: date | None
    date_to: date | None
    time_from: time | None = None
    time_to: time | None = None
    views_gt: int | None
    views_delta: Literal["positive", "negative"] | None = None


class ParsedQuery(BaseModel):
    intent: Intent
    filters: Filters
