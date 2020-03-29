import time
from typing import List

from sqlalchemy import BIGINT, INT, Column, String, Table, and_, desc, null
from sqlalchemy.sql.expression import insert, select, update
from sqlalchemy.types import Integer

from nogi.db import BaseModel


class BangumiTable(BaseModel):

    def __init__(self, engine, metadata, role='reader'):
        table = Table(
            'bilibili_bangumis',
            metadata,
            # Info
            Column('id', BIGINT, primary_key=True, autoincrement=True),
            Column('av_id', BIGINT, unique=True),
            Column("member_id", INT),
            Column("member_name", String(255)),
            # Meta
            Column("title", String(255)),
            Column("subtitle", String(255), default=''),
            Column("description", String(255), default=''),
            Column("cover_url", String(255), default=''),
            Column("video_created_at", INT, default=null),
            Column("duration", INT, default=0),
            # Stat
            Column("play_count", INT, default=0),
            Column("comment_count", INT, default=0),
            Column("review_count", INT, default=0),
            # Storage
            Column('idol', String(255)),
            Column('program', String(255)),
            Column('subtitle_group', String(255)),
            Column('storage_name', String(255)),
            Column("storage_key", String(255)),
            Column('created_at', BIGINT),
            Column('updated_at', BIGINT),
            Column('deleted_at', BIGINT, default=0),
            extend_existing=True
        )
        super().__init__(engine, metadata, table, role)

    def create_video_record(self, record: dict) -> int:
        assert self.role == 'writer'
        record['created_at'] = record['updated_at'] = int(time.time() * 1000)
        return self.execute(insert(self.table, record)).rowcount

    def get_av_ids_by_member_id(self, member_id: int) -> set:
        stmt = select([self.table.c.av_id]) \
            .where(and_(self.table.c.member_id == member_id)) \
            .order_by(desc(self.table.c.updated_at))
        results = set()
        cursor = self.execute(stmt)
        row = cursor.fetchone()
        while row:
            results.add(row.av_id)
            row = cursor.fetchone()
        return results

    def get_member_id_by_av_id(self, av_id: int) -> int:
        stmt = select([self.table.c.member_id]).where(and_(self.table.c.av_id == av_id)).limit(1)
        row = self.execute(stmt).first()
        return row.member_id if row else 0

    def get_latest_inserted_av_id_by_member_id(self, member_id: int) -> dict:
        stmt = select([self.table.c.av_id, self.table.c.video_created_at, self.table.c.created_at]).where(
            and_(self.table.c.member_id == member_id)
        ).order_by(desc(self.table.c.created_at))
        row = self.execute(stmt).first()
        if row:
            return dict(av_id=row.av_id, video_created_at=row.video_created_at, created_at=row.created_at)
        return dict(av_id=0, video_created_at=0, created_at=0)

    def update_storage_key(self, av_id: int, storage_type: str, bucket: str, object_key: str) -> int:
        assert self.role == 'writer'
        stmt = update(self.table).where(and_(self.table.c.av_id == av_id)).values(
            dict(
                storage_type=storage_type,
                storage_key='{}/{}'.format(bucket, object_key),
                updated_at=int(time.time())
            )
        )
        return self.execute(stmt).rowcount
