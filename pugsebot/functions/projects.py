import logging

from utils import get_json, bot_reply

logger = logging.getLogger('projects')

def get_projects():
    repo_url = 'http://api.github.com/orgs/pug-se/repos'
    text = 'Os projetos da comunidade estão no '
    text += f'<a href="{repo_url}">GitHub</a>\n\n'

    url = 'https://api.github.com/orgs/pug-se/repos'
    info_dict = get_json(url)
    i = 1
    for info in info_dict:
        name = info['name']
        description = info['description']
        url = info['html_url']
        text += f'{i}) <a href="{url}">{name}</a>: {description}\n'
        i += 1
    return text

def reply(reply_text):
    return bot_reply(reply_text, get_projects())
