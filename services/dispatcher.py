from llm.schemas import ParsedQuery
from db.queries import (
    count_videos,
    count_videos_with_views_gt,
    sum_views_delta,
    count_videos_with_new_views,
    count_snapshots
)


# маршрутизатор небходимых sql запросово
async def dispatch(query: ParsedQuery) -> int:
    match query.intent:
        case "count_videos":
            return await count_videos(query.filters)
        case "sum_views_delta":
            return await sum_views_delta(query.filters)
        case "count_videos_with_views_gt":
            return await count_videos_with_views_gt(query.filters)
        case "count_videos_with_new_views":
            return await count_videos_with_new_views(query.filters)
        case "count_snapshots":
            return await count_snapshots(query.filters)
        case _:
            raise ValueError("Unknown intent")
