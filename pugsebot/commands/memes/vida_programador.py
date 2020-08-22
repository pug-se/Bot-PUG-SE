"""Get images from vidadeprogramador."""

from ...utils.request import get_html_soup

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

def get_meme_url_image():
    """Get an image from vidadeprogramador."""
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
