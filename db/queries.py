from sqlalchemy import select, func
from sqlalchemy.sql import Select
from db.models import Video, VideoSnapshot
from llm.schemas import Filters
from db.session import get_async_session


def base_video_stmt(filters: Filters) -> Select:
    stmt = select(Video)

    if filters.creator_id:
        stmt = stmt.where(Video.creator_id == filters.creator_id)

    if filters.date_from:
        stmt = stmt.where(Video.video_created_at >= filters.date_from)

    if filters.date_to:
        stmt = stmt.where(Video.video_created_at <= filters.date_to)

    return stmt


def base_snapshot_stmt(filters: Filters) -> Select:
    stmt = select(VideoSnapshot)

    if filters.creator_id:
        stmt = stmt.join(
            Video,
            Video.id == VideoSnapshot.video_id
        ).where(Video.creator_id == filters.creator_id)

    if filters.date_from:
        stmt = stmt.where(VideoSnapshot.created_at >= filters.date_from)

    if filters.date_to:
        stmt = stmt.where(VideoSnapshot.created_at <= filters.date_to)

    return stmt


# для 1 и 2
async def count_videos(filters: Filters) -> int:
    async with get_async_session() as session:
        stmt = select(func.count()).select_from(
            base_video_stmt(filters).subquery()
        )

        result = await session.execute(stmt)
        return result.scalar() or 0


# для 3
async def count_videos_with_views_gt(filters: Filters) -> int:
    async with get_async_session() as session:
        base_stmt = base_video_stmt(filters).where(
            Video.views_count > filters.views_gt
        )

        stmt = select(func.count()).select_from(base_stmt.subquery())

        result = await session.execute(stmt)
        return result.scalar() or 0


# для 4
async def sum_views_delta(filters: Filters) -> int:
    async with get_async_session() as session:
        stmt = select(
            func.coalesce(func.sum(VideoSnapshot.delta_views_count), 0)
        ).select_from(
            base_snapshot_stmt(filters).subquery()
        )

        result = await session.execute(stmt)
        return result.scalar()


# для 5
async def count_videos_with_new_views(filters: Filters) -> int:
    async with get_async_session() as session:
        base_stmt = base_snapshot_stmt(filters).where(
            VideoSnapshot.delta_views_count > 0
        )

        stmt = select(
            func.count(func.distinct(VideoSnapshot.video_id))
        ).select_from(base_stmt.subquery())

        result = await session.execute(stmt)
        return result.scalar() or 0
