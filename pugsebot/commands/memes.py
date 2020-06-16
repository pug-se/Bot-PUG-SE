import random

from utils import Command, get_html_soup, UM_DIA_EM_SEGUNDOS

BASE_URL_VIDA_PROGRAMADOR = 'https://vidadeprogramador.com.br/'
URL_VIDA_PROGRAMADOR_RANDOM = BASE_URL_VIDA_PROGRAMADOR + '+rand'
URL_VIDA_PROGRAMADOR_TAG_TIRINHA = (
    BASE_URL_VIDA_PROGRAMADOR
    + 'tag-tirinhas.html'
)
URL_VIDA_PROGRAMADOR_TAG_REAL = (
    BASE_URL_VIDA_PROGRAMADOR
    + 'tag-real.html'
)
URL_VIDA_PROGRAMADOR_TAG_USUARIO = (
    BASE_URL_VIDA_PROGRAMADOR
    + 'tag-usuario.html'
)
URLS_VERIFICAR_VIDA_PROGRAMADOR = [
    URL_VIDA_PROGRAMADOR_TAG_TIRINHA,
    URL_VIDA_PROGRAMADOR_TAG_REAL,
    URL_VIDA_PROGRAMADOR_TAG_USUARIO,
]

def get_url_image_vida_programador():
    meme_found = False

    while not meme_found:
        document = get_html_soup(URL_VIDA_PROGRAMADOR_RANDOM)
        for url in URLS_VERIFICAR_VIDA_PROGRAMADOR:
            tags_found = bool(document.select(
                '.postmetadata > a[href="{}"]'.format(url)
            ))
            if tags_found:
                break

        metadata_image = document.select('article.post a img')
        meme_found = tags_found and bool(metadata_image)

    return metadata_image[0]['src']

BASE_URL_TURNOFF_US = 'https://turnoff.us'
URL_TURNOFF_US_ALL_POSTS = BASE_URL_TURNOFF_US + '/pt/all/'

def get_url_image_turnoff_us():
    document = get_html_soup(URL_TURNOFF_US_ALL_POSTS)
    random_link = random.choice(document.select('.post-link'))
    random_url = random_link['href']

    random_document = get_html_soup(BASE_URL_TURNOFF_US + random_url)
    random_image = random_document.select('.post-content img')
    return BASE_URL_TURNOFF_US + random_image[0]['src']

MEMES_IMAGES_FUNCTIONS = [
    get_url_image_vida_programador,
    get_url_image_turnoff_us,
]

class Memes(Command):
    def __init__(self):
        super().__init__(
            name='memes',
            help_text='Coleta memes de programação',
            reply_function_name='reply_photo',
            schedule_interval=UM_DIA_EM_SEGUNDOS * 2,
        )

    def function(self, update=None, context=None):
        random_image_function = random.choice(MEMES_IMAGES_FUNCTIONS)
        return random_image_function()
