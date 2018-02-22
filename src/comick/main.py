# coding: utf-8

import re
from typing import NamedTuple, List
import feedparser


class Comic(NamedTuple):
    title: str
    image: str
    link: str=""


FEED_URL = "http://sinkan.net/?action_rss=true&mode=today&group=Comic"

IMAGE_PATTERN = re.compile('''https?://.*\.jpg''')

whitelist = {
    "ジャンプコミックス",
    "電撃コミックス",
    "ビッグコミックス",
    "アクションコミックス",
    "バンブーコミックス",
    "ガンガンコミックス",
}


def check() -> List[Comic]:
    comics = []
    feeds = feedparser.parse(FEED_URL)
    for entry in feeds.entries:
        if not filter_label(entry.title):
            continue
        m = IMAGE_PATTERN.search(entry.description)
        image = m.group(0) if m else ""
        title = entry.title.split(" ")[1:-1]
        comic = Comic(title=title, image=image)
        comics.append(comic)
    return comics
    

def filter_label(title):
    for label in whitelist:
        if label in title:
            return True
    return False
        

def main():
    comics = check()
    print(comics)


if __name__ == '__main__':
    main()
