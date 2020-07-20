"""Gets images from https://turnoff.us"""

import random

from utils.request import get_html_soup

BASE_URL_TURNOFF_US = 'https://turnoff.us'
URL_TURNOFF_US_ALL_POSTS = BASE_URL_TURNOFF_US + '/pt/all/'

def get_meme_url_image():
    """Gets an image located at https://turnoff.us"""
    
    document = get_html_soup(URL_TURNOFF_US_ALL_POSTS)
    random_link = random.choice(document.select('.post-link'))
    random_url = random_link['href']

    random_document = get_html_soup(BASE_URL_TURNOFF_US + random_url)
    random_image = random_document.select('.post-content img')
    return BASE_URL_TURNOFF_US + random_image[0]['src']
