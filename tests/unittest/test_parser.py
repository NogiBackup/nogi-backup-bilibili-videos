import os

import toml

from nogi import parsers
from tests import mockdata

PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../target_channels.toml')
CHANNEL_CONFIG = toml.load(os.path.abspath(PATH))


def test_extract_video_info():
    test_member_id = mockdata.VIDEO_INFO.get('mid')
    result = parsers.extract_video_info(mockdata.VIDEO_INFO, CHANNEL_CONFIG['channels'][str(test_member_id)]['tags'])
    assert result == {
        'av_id': 97265693,
        'member': '千葉幽羽',
        'member_id': 19553445,
        # Meta
        'title': '【乃木坂去哪儿】【终】EP20  艺人新宠的体育项目，竟然要从4期生中选出国家队替补！？ 后篇 & 未公开映像 200317【上行之坂字幕组】',
        'subtitle': '',
        'description': '',
        'cover_url': 'https://i0.hdslb.com/bfs/archive/ffc4a99b5597fc4b2a190163dc06eee422e6d381.jpg',
        'video_created_at': 1584541362,
        'duration': 1895,
        # Stat
        'idol': '乃木坂',
        'subtitle_group': '上行之坂',
        'program': '乃木坂去哪儿',
        'play_count': 19369,
        'comment_count': 92,
        'review_count': 779,
    }
