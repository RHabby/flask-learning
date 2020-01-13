import requests

from app.collection.models import Collections
from app import db


def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return r
    except (requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def save_bookmark(title, image, url, base_url, description, content_type):
    check_existing = Collections.query.filter(Collections.url == url).count()
    if not check_existing:
        bookmark = Collections(title=title, image=image, url=url, base_url=base_url,
                               description=description, content_type=content_type)
        db.session.add(bookmark)
        db.session.commit()
