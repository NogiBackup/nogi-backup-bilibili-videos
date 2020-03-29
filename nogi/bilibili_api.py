import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}


def get_channel_info(member_id: int):
    return requests.get(url='https://api.bilibili.com/x/space/acc/info', headers=HEADERS, params=dict(mid=member_id, jsonp='jsonp')).json()


def search(member_id: int, page_size: int = 30, page_number: int = 1, order: str = 'pubdate', keyword: str = None):
    return requests.get(
        url='https://api.bilibili.com/x/space/arc/search',
        headers={
            'User-Agent': HEADERS['User-Agent'],
            'Origin': 'https://space.bilibili.com',
            'Referer': 'https://space.bilibili.com/{}/video'.format(member_id),
        },
        params=dict(
            mid=member_id,
            ps=page_size,
            tid=0,
            pn=page_number,
            keyword=keyword,
            order=order,
            jsonp='jsonp',
        )
    ).json()


def get_videos(member_id: int, page_num: int = 1, page_size: int = 30, keyword: str = None) -> list:
    return requests.get(
        url='https://space.bilibili.com/ajax/member/getSubmitVideos',
        headers=HEADERS,
        params=dict(mid=member_id, pagesize=page_size, tid=0, page=page_num, keyword=keyword, order='pubdate'),
    ).json()
