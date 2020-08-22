"""Gets images from Hacktoon."""

import random

from utils.request import get_html_soup

URL_HACKTOON_ALL_POSTS = "https://hacktoon.com/index/"


def get_meme_image_from_url(url):
    """Get an image from a Hacktoon URL."""
    document = get_html_soup(url)
    images = document.select(".page-content img")
    for image in images:
        if image["src"].endswith(".png"):
            if image["src"].startswith("http"):
                return image["src"]
            else:
                return "https:{}".format(image["src"])
    raise ValueError()


def get_meme_url_image():
    """Get an image from Hacktoon."""
    document = get_html_soup(URL_HACKTOON_ALL_POSTS)
    links = document.select(".index-content .index-item a")
    count = 0

    while count < 10:
        random_link = random.choice(links)
        random_url = random_link["href"]
        try:
            return get_meme_image_from_url(random_url)
        except:
            count += 1

    raise Exception()
