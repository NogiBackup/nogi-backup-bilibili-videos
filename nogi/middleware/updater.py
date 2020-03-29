import time
import traceback
from typing import List

from tqdm import tqdm

from nogi import bilibili_api, parsers
from nogi.db.bangumi import BangumiTable


class Updater:

    def __init__(self, member_id: int, channel_config: dict, bangumi_table: BangumiTable):
        self.member_id = member_id
        self.channel_config = channel_config
        self.table = bangumi_table
        self.latest_video_in_db = self.table.get_latest_inserted_av_id_by_member_id(member_id)

    def _extract_page(self, page: List[dict]) -> List[dict]:
        results = []
        do_continue = True
        for raw_record in page:
            record = parsers.extract_video_info(raw_record, self.channel_config['tags'])
            record['created_at'] = record['updated_at'] = int(time.time() * 1000)
            if record['video_created_at'] > self.latest_video_in_db['video_created_at']:
                results.append(record)
            else:
                do_continue = False
                break
        return dict(records=results, do_continue=do_continue)

    def update(self):
        current_page = bilibili_api.search(self.member_id)
        total_count = current_page['data']['page']['count']
        total_pages = current_page['data']['page']['ps']

        current_page_number = current_page['data']['page']['pn']
        do_continue = True
        inserted_record = 0
        while do_continue:
            page_result = self._extract_page(current_page['data']['list']['vlist'])
            if not page_result['records']:
                break

            for record in tqdm(page_result['records']):
                try:
                    inserted_record += self.table.create_video_record(record)
                except Exception:
                    print(traceback.format_exc())
            if page_result['do_continue'] and inserted_record < total_count and current_page_number < total_pages:
                current_page_number += 1
                current_page = bilibili_api.search(member_id=self.member_id, page_number=current_page_number)
            else:
                break

        return inserted_record
