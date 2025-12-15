import json
import uuid
from datetime import datetime
from db.models import Video, VideoSnapshot
from db.session import get_sync_session
from pathlib import Path


def parse_dt(value: str):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_data(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    videos = []
    snapshots = []

    for v in data["videos"]:
        video = Video(
            id=uuid.UUID(v["id"]),
            creator_id=uuid.UUID(v["creator_id"]),
            video_created_at=parse_dt(v["video_created_at"]),
            views_count=v["views_count"],
            likes_count=v["likes_count"],
            comments_count=v["comments_count"],
            reports_count=v["reports_count"],
            created_at=parse_dt(v["created_at"]),
            updated_at=parse_dt(v["updated_at"]),
        )
        videos.append(video)

        for s in v["snapshots"]:
            snapshot = VideoSnapshot(
                id=uuid.UUID(s["id"]),
                video_id=uuid.UUID(s["video_id"]),
                views_count=s["views_count"],
                likes_count=s["likes_count"],
                comments_count=s["comments_count"],
                reports_count=s["reports_count"],
                delta_views_count=s["delta_views_count"],
                delta_likes_count=s["delta_likes_count"],
                delta_comments_count=s["delta_comments_count"],
                delta_reports_count=s["delta_reports_count"],
                created_at=parse_dt(s["created_at"]),
                updated_at=parse_dt(s["updated_at"]),
            )
            snapshots.append(snapshot)

    # записываем в бд
    for db in get_sync_session():
        db.bulk_save_objects(videos)
        db.bulk_save_objects(snapshots)
        db.commit()
        db.close()


if __name__ == "__main__":
    video_path = Path(__file__).parent.parent.absolute() / "videos.json"
    load_data(str(video_path))
