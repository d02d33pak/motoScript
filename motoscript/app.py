"""
I recommend you visit the motogp website and
inspect element to understand the script better
"""

import argparse
import asyncio

import requests
from bs4 import BeautifulSoup

from downloader import download_category


def start_download(category, path):
    """ Entry Point """
    base_url = "https://motogp.com/en/photos/"
    path_by_category = {
        "gp": "events",
        "best_of": "best+of",
        "riders": "riders",
        "teams": "teams",
    }
    try:
        full_url = base_url + path_by_category[category]
        content = requests.get(full_url).text
        soup = BeautifulSoup(content, "lxml")
        asyncio.run(download_category(soup, path, category))
    except KeyError:
        print("wrong category, exiting...")
        exit(1)


def run():
    """
    categories gp, best_of, riders, teams
    can be passed as cmd line args
    """
    parser = argparse.ArgumentParser(
        description="Download photos from official MotoGP site"
    )

    parser.add_argument(
        "-c",
        "--category",
        choices=["teams", "riders", "gp", "best_of"],
        default="teams",
        help="Category of photos you want to download",
    )
    parser.add_argument(
        "-p",
        "--path",
        default="/home/d02/Downloads",
        help="Path where you want to download the photos to",
    )

    args = parser.parse_args()
    category = args.category
    path = args.path

    start_download(category, path)
