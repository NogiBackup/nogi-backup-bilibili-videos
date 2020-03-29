import time


def _parse_duration(duration_str: str) -> int:
    elements = duration_str.split(':')
    minutes, seconds = int(elements[0]), int(elements[1])
    return int(minutes * 60 + seconds)


def _parse_tag(title: str, tag_list: list) -> str:
    if tag_list:
        for tag in tag_list:
            if tag in title:
                return tag
    return None


def extract_channel_info(infos: dict) -> dict:
    return dict(member_id=infos['mid'], name=infos['name'], created_at=int(time.time()))


def extract_channel_total_pages(infos: dict) -> int:
    return infos['data'].get('pages', 0)


def extract_video_info(infos: dict, tags_dict: dict) -> dict:
    try:
        play_count = int(infos.get('play', 0))
    except Exception:
        play_count = 0
    try:
        comment_count = int(infos.get('comment', 0))
    except Exception:
        comment_count = 0
    try:
        review_count = int(infos.get('video_review', 0))
    except Exception:
        review_count = 0

    member_id = infos.get('mid')
    try:
        return dict(
            av_id=infos.get('aid'),  # 52703948,
            member_name=infos.get('author'),  # '千葉幽羽',
            member_id=member_id,  # 19553445,
            # Meta
            title=infos.get('title'),  # '【上行之坂】23rd 撞撞暖暖',
            subtitle=infos.get('subtitle'),  # '',
            description=infos.get('description'),  # '-',
            # 'https + //i2.hdslb.com/bfs/archive/b3d49265f5b38b11f07ad8ab84156fc8fe7e2d62.jpg',
            cover_url='https:' + infos.get('pic') if infos.get('pic') else '',
            video_created_at=infos.get('created'),  # 1558066749,
            duration=_parse_duration(infos['length']),  # '04:10',
            # Stat
            idol=_parse_tag(infos.get('title'), tags_dict.get('idols')),
            subtitle_group=_parse_tag(infos.get('title'), tags_dict.get('subtitle_groups')),
            program=_parse_tag(infos.get('title'), tags_dict.get('programs')),
            play_count=play_count,
            comment_count=comment_count,
            review_count=review_count,
        )
    except Exception:
        print('Parsing Error Records: %s', infos)
