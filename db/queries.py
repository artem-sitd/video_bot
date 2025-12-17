from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func
from db.models import Video, VideoSnapshot
from db.session import get_async_session


# -------------------------
# helpers
# -------------------------

def parse_datetime(value: str) -> datetime:
    """
    Преобразует строку из QueryPlan в aware datetime (UTC)
    """
    if len(value) == 10:  # YYYY-MM-DD
        return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:  # YYYY-MM-DD HH:MM
        return datetime.strptime(value, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)


# -------------------------
# executor
# -------------------------

async def execute_query_plan(plan: dict) -> int:
    async with get_async_session() as session:

        source = plan["source"]
        select_cfg = plan["select"]
        filters = plan.get("filters", [])

        # =====================================================
        # SOURCE: VIDEOS
        # =====================================================
        if source == "videos":
            stmt = select().select_from(Video)

            # --- aggregation ---
            if select_cfg["func"] == "count":
                column = getattr(Video, select_cfg["field"])
                if select_cfg.get("distinct"):
                    stmt = stmt.with_only_columns(func.count(column.distinct()))
                else:
                    stmt = stmt.with_only_columns(func.count(column))

            elif select_cfg["func"] == "sum":
                column = getattr(Video, select_cfg["field"])
                stmt = stmt.with_only_columns(
                    func.coalesce(func.sum(column), 0)
                )

            # --- filters ---
            for f in filters:
                field = f["field"]
                op = f["op"]
                value = f["value"]

                column = getattr(Video, field)

                if op == "between":
                    start_raw, end_raw = value
                    start_dt = parse_datetime(start_raw)
                    end_dt = parse_datetime(end_raw)

                    # если дата без времени — расширяем на весь день
                    if len(end_raw) == 10:
                        end_dt += timedelta(days=1)

                    stmt = stmt.where(
                        column >= start_dt,
                        column < end_dt
                    )

                elif op == "=":
                    stmt = stmt.where(column == value)
                elif op == ">":
                    stmt = stmt.where(column > value)
                elif op == "<":
                    stmt = stmt.where(column < value)
                elif op == ">=":
                    stmt = stmt.where(column >= value)
                elif op == "<=":
                    stmt = stmt.where(column <= value)

            result = await session.execute(stmt)
            return result.scalar() or 0

        # =====================================================
        # SOURCE: SNAPSHOTS
        # =====================================================
        if source == "snapshots":
            stmt = select().select_from(VideoSnapshot)

            # JOIN videos если нужен creator_id
            if any(f["field"] == "creator_id" for f in filters):
                stmt = stmt.join(Video, Video.id == VideoSnapshot.video_id)

            # --- aggregation ---
            if select_cfg["func"] == "sum":
                column = getattr(VideoSnapshot, select_cfg["field"])
                stmt = stmt.with_only_columns(
                    func.coalesce(func.sum(column), 0)
                )
            elif select_cfg["func"] == "count":
                stmt = stmt.with_only_columns(func.count())

            # --- filters ---
            for f in filters:
                field = f["field"]
                op = f["op"]
                value = f["value"]

                if field == "creator_id":
                    column = Video.creator_id
                else:
                    column = getattr(VideoSnapshot, field)

                if op == "between":
                    start_raw, end_raw = value
                    start_dt = parse_datetime(start_raw)
                    end_dt = parse_datetime(end_raw)

                    if len(end_raw) == 10:
                        end_dt += timedelta(days=1)

                    stmt = stmt.where(
                        column >= start_dt,
                        column < end_dt
                    )

                elif op == "=":
                    stmt = stmt.where(column == value)
                elif op == ">":
                    stmt = stmt.where(column > value)
                elif op == "<":
                    stmt = stmt.where(column < value)
                elif op == ">=":
                    stmt = stmt.where(column >= value)
                elif op == "<=":
                    stmt = stmt.where(column <= value)

            result = await session.execute(stmt)
            return result.scalar() or 0

        raise ValueError(f"Unknown source: {source}")
