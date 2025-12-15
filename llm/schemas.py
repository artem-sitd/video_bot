from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class Intent(str, Enum):
    count_videos = "count_videos"
    sum_views_delta = "sum_views_delta"
    count_videos_with_views_gt = "count_videos_with_views_gt"
    count_videos_with_new_views = "count_videos_with_new_views"


class Filters(BaseModel):
    creator_id: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    views_gt: Optional[int] = None


class ParsedQuery(BaseModel):
    intent: Intent
    filters: Filters
