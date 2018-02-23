# coding: utf-8

import re
import os
from typing import NamedTuple, List

import requests
import feedparser


class Comic(NamedTuple):
    title: str
    image: str
    link: str = ""
    label: str = ""


FEED_URL = "http://sinkan.net/?action_rss=true&mode=today&group=Comic"

IMAGE_PATTERN = re.compile('''https?://.*\.jpg''')

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")

whitelist = (os.environ.get("LABELS_WHITELIST") or "ジャンプ,ガンガン").split(",")


def check() -> List[Comic]:
    comics = []
    feeds = feedparser.parse(FEED_URL)
    for entry in feeds.entries:
        if not filter_label(entry.title):
            continue
        m = IMAGE_PATTERN.search(entry.description)
        image = m.group(0) if m else ""
        title = " ".join(entry.title.split(" ")[1:-1])
        label = entry.title.split(" ")[-1]
        comic = Comic(title=title, image=image, link=entry.link, label=label)
        comics.append(comic)
    return comics
    

def filter_label(title):
    for label in whitelist:
        if label in title:
            return True
    return False
        
def post_slack(comics: List[Comic]):
    if not SLACK_WEBHOOK:
        return
    for comic in comics:
        data = {
                "username": "今日の新刊",
                "icon_emoji": ":books:",
                "attachments": [
                    {
                        "thumb_url": comic.image,
                        "title": comic.title,
                        "title_link": comic.link,
                        "text": comic.label
                    }
                ]
        }
        if SLACK_CHANNEL:
            data['channel'] = SLACK_CHANNEL
        res = requests.post(SLACK_WEBHOOK, json=data)
        print(res)

def main():
    comics = check()
    post_slack(comics)


if __name__ == '__main__':
    main()
