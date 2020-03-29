import os
import time

from fire import Fire
import toml
from tqdm import tqdm

from nogi.db import create_engine_and_metadata
from nogi.db.bangumi import BangumiTable
from nogi.middleware.updater import Updater


def create_db_connection():
    connection_string = 'mysql://{username}:{password}@{host}:3306/{db_name}?binary_prefix=True&charset=utf8mb4'.format(
        username=os.environ['MYSQL_USERNAME'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ.get('MYSQL_DB_HOST', '127.0.0.1'),
        db_name=os.environ.get('MYSQL_DB_NAME', 'nogi_backup')
    )
    engine, metadata = create_engine_and_metadata(connection_string)
    if not engine.dialect.has_table(engine, 'bilibili_bangumis'):
        metadata.create_all()
    return engine, metadata


class CommandLine:

    def __init__(self, channel_config_path: str = None):
        engine, metadata = create_db_connection()
        self.bangumi_table = BangumiTable(engine, metadata, role='writer')

        if channel_config_path and os.path.isfile(channel_config_path):
            self.channels = toml.load(channel_config_path)['channels']
        else:
            self.channels = toml.load(
                os.path.abspath(os.path.join(os.path.dirname(__file__), 'target_channels.toml'))
            )['channels']

    def recreate_table(self):
        self.bangumi_table.metadata.drop_all()
        self.bangumi_table.metadata.create_all()

    def update_channel_videos(self, member_id: int = None):
        if member_id:
            Updater(
                member_id=member_id,
                channel_config=self.channels[str(member_id)],
                bangumi_table=self.bangumi_table).update()
        else:
            for member_id in tqdm(self.channels):
                Updater(
                    member_id=member_id,
                    channel_config=self.channels[str(member_id)],
                    bangumi_table=self.bangumi_table).update()
            time.sleep(5)


if __name__ == "__main__":
    Fire(CommandLine)
