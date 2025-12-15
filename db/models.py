from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from db.base import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(BigInteger, primary_key=True)
    creator_id = Column(BigInteger, nullable=False)
    video_created_at = Column(DateTime, nullable=False)

    views_count = Column(BigInteger, nullable=False)
    likes_count = Column(BigInteger, nullable=False)
    comments_count = Column(BigInteger, nullable=False)
    reports_count = Column(BigInteger, nullable=False)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id = Column(BigInteger, primary_key=True)
    video_id = Column(BigInteger, ForeignKey("videos.id"))

    views_count = Column(BigInteger, nullable=False)
    delta_views_count = Column(BigInteger, nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
