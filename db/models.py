from db.base import Base
import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, DateTime, ForeignKey


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )

    creator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    video_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    views_count: Mapped[int] = mapped_column(Integer, nullable=False)
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False)
    comments_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reports_count: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )

    video_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("videos.id"),
        nullable=False
    )

    views_count: Mapped[int] = mapped_column(Integer, nullable=False)
    likes_count: Mapped[int] = mapped_column(Integer, nullable=False)
    comments_count: Mapped[int] = mapped_column(Integer, nullable=False)
    reports_count: Mapped[int] = mapped_column(Integer, nullable=False)

    delta_views_count: Mapped[int] = mapped_column(Integer, nullable=False)
    delta_likes_count: Mapped[int] = mapped_column(Integer, nullable=False)
    delta_comments_count: Mapped[int] = mapped_column(Integer, nullable=False)
    delta_reports_count: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
