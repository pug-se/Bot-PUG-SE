import logging

from utils import get_html_soup, bot_reply

logger = logging.getLogger('Udemy')

def get_udemy_coupons():
    text = ''
    try:
        url = 'https://couponscorpion.com/'
        soup = get_html_soup(url)
        title_list = []
        url_list = []
        for h3 in soup.findAll('h3'):
            link = h3.find('a')
            if link:
                title_list.append(link.text.strip())
                url_list.append(link.get('href').strip())

        text = "esses foram os cupons da Udemy que encontrei:\n"

        for _, url in zip(title_list, url_list):
            text += f'{url} \n'

    except Exception as error:
        logger.error(error)

    return text

def reply(reply_message):
    return bot_reply(reply_message, get_udemy_coupons())

def schedule(schedule_manager, send_message, timeout):
    def send_udemy_coupons():
        send_message(get_udemy_coupons())

    schedule_manager.add_schedule(send_udemy_coupons, timeout)
