import logging

from utils import get_html_soup, bot_reply

logger = logging.getLogger('News')

def get_python_news():
    text = ''
    try:
        url = 'https://www.python.org/blogs/'
        soup = get_html_soup(url)

        h3 = soup.find('h3', {'class': 'event-title'})
        link = h3.find('a')
        title = link.text.strip()
        url = link.get('href').strip()
        text = 'A notícia mais quente sobre Python:\n'
        text += f'<a href="{url}">{title}</a>'
    except Exception as error:
        logger.error(error)

    return text

def reply(reply_message):
    return bot_reply(reply_message, get_python_news())

def schedule(schedule_manager, send_message, timeout):
    def send_news():
        send_message(get_python_news())

    schedule_manager.add_schedule(send_news, timeout)
