from db.queries import (
    count_videos,
    count_videos_with_filters,
    count_videos_with_views_gt,
    sum_views_delta,
    count_videos_with_new_views,
)


def dispatch(parsed_query):
    intent = parsed_query.intent
    filters = parsed_query.filters

    if intent == "count_videos":
        return count_videos()

    if intent == "count_videos_with_filters":
        return count_videos_with_filters(filters)

    if intent == "count_videos_with_views_gt":
        return count_videos_with_views_gt(filters.views_gt)

    if intent == "sum_views_delta":
        return sum_views_delta(filters)

    if intent == "count_videos_with_new_views":
        return count_videos_with_new_views(filters)

    raise ValueError(f"Unknown intent: {intent}")
