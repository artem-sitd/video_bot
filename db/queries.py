from asyncio import Timeout
from sqlalchemy import select, func, cast, Date, Time
from sqlalchemy.sql import Select
from db.models import Video, VideoSnapshot
from llm.schemas import Filters
from db.session import get_async_session
from datetime import timedelta


def base_video_stmt(filters: Filters) -> Select:
    stmt = select(Video)

    if filters.creator_id:
        stmt = stmt.where(Video.creator_id == filters.creator_id)

    if filters.date_from:
        stmt = stmt.where(
            cast(Video.video_created_at, Date) >= filters.date_from)

    if filters.date_to:
        stmt = stmt.where(
            cast(Video.video_created_at, Date) <= filters.date_to)

    return stmt


def base_snapshot_stmt(filters: Filters) -> Select:
    stmt = select(VideoSnapshot)

    if filters.creator_id:
        stmt = stmt.join(
            Video,
            Video.id == VideoSnapshot.video_id
        ).where(Video.creator_id == filters.creator_id)

    if filters.date_from:
        stmt = stmt.where(cast(VideoSnapshot.created_at, Date) >= filters.date_from)

    if filters.date_to:
        stmt = stmt.where(cast(VideoSnapshot.created_at, Date) <= filters.date_to)

    if filters.time_from:
        stmt = stmt.where(
            cast(VideoSnapshot.created_at, Time) >= filters.time_from
        )

    if filters.time_to:
        stmt = stmt.where(
            cast(VideoSnapshot.created_at, Time) <= filters.time_to
        )

    return stmt


# для 1 и 2
async def count_videos(filters: Filters) -> int:
    async with get_async_session() as session:
        stmt = select(func.count()).select_from(
            base_video_stmt(filters).subquery())

        result = await session.execute(stmt)
        return result.scalar() or 0


# для 3
async def count_videos_with_views_gt(filters: Filters) -> int:
    async with get_async_session() as session:
        base_stmt = base_video_stmt(filters).where(
            Video.views_count > filters.views_gt)

        stmt = select(func.count()).select_from(base_stmt.subquery())
        result = await session.execute(stmt)
        return result.scalar() or 0


# для 4
async def sum_views_delta(filters: Filters) -> int:
    async with get_async_session() as session:

        # 🔹 Если вопрос про опубликованные видео-  итоговые просмотры
        if filters.date_from or filters.date_to:
            stmt = select(func.coalesce(func.sum(Video.views_count), 0))

            if filters.creator_id:
                stmt = stmt.where(Video.creator_id == filters.creator_id)

            if filters.date_from:
                stmt = stmt.where(
                    cast(Video.video_created_at, Date) >= filters.date_from
                )

            if filters.date_to:
                stmt = stmt.where(
                    cast(Video.video_created_at, Date) <= filters.date_to
                )

            result = await session.execute(stmt)
            return result.scalar() or 0

        # 🔹 Иначе —  прирост по снапшотам
        stmt = select(
            func.coalesce(func.sum(VideoSnapshot.delta_views_count), 0)
        ).select_from(
            base_snapshot_stmt(filters).subquery()
        )

        result = await session.execute(stmt)
        return result.scalar() or 0


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


async def count_snapshots(filters: Filters) -> int:
    async with get_async_session() as session:

        # Если НЕ указано views_delta — просто считаем замеры
        if filters.views_delta is None:
            stmt = select(func.count()).select_from(
                base_snapshot_stmt(filters).subquery()
            )
            result = await session.execute(stmt)
            return result.scalar() or 0

        # если указано сравнение с предыдущим замером
        prev_views = func.lag(VideoSnapshot.views_count).over(
            partition_by=VideoSnapshot.video_id,
            order_by=VideoSnapshot.created_at
        )

        subq = (
            select(
                VideoSnapshot.video_id,
                VideoSnapshot.views_count,
                prev_views.label("prev_views"),
            )
            .select_from(VideoSnapshot)
            .subquery()
        )

        conditions = [subq.c.prev_views.is_not(None)]

        if filters.views_delta == "negative":
            conditions.append(subq.c.views_count < subq.c.prev_views)

        if filters.views_delta == "positive":
            conditions.append(subq.c.views_count > subq.c.prev_views)

        stmt = select(func.count()).select_from(subq).where(*conditions)

        result = await session.execute(stmt)
        return result.scalar() or 0
