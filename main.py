import requests

from lxml import html
from locale import str
from builtins import list, set, dict, range, print
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = 'https://showrss.info'


def login():
    login_url = "%s/login" % (BASE_URL)

    session_requests = requests.session()

    result = session_requests.get(login_url)

    tree = html.fromstring(result.text)

    TOKEN = list(
        set(tree.xpath("//input[@name='_token']/@value"))
    )[0]

    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "_token": TOKEN
    }

    result = session_requests.post(
        login_url,
        data=payload,
        headers=dict(referer=login_url)
    )

    return session_requests


def get_episodes(session_requests):
    site_url = "%s/timeline" % (BASE_URL)

    result = session_requests.get(
        site_url,
        headers=dict(referer=site_url)
    )

    current_episodes = []

    tree = html.fromstring(result.content)
    for x in range(1, 5):

        date = tree.xpath(
            "/html/body/div/div[3]/div[2]/strong[%s]" % (str(x)))

        temp = tree.xpath(
            "/html/body/div/div[3]/div[2]/ul[%s]/li[1]/a/strong[1]" % (str(x)))

        current_episode_date = date[0].text
        current_episode_title = "%s %s" % (temp[0].text, temp[0].tail.rstrip())

        current_episode = {
            'date': current_episode_date,
            'title': current_episode_title
        }
        current_episodes.append(current_episode)

    return current_episodes


def printEpisodes(episodes):
    for episode in episodes:
        print(episode['date'] + ':', episode['title'])


def main():
    session_requests = login()
    current_episodes = get_episodes(session_requests)
    printEpisodes(current_episodes)


if __name__ == "__main__":
    main()
