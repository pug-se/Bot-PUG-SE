import logging

from utils import Command, get_html_soup, UM_DIA_EM_SEGUNDOS

logger = logging.getLogger('Udemy')

class Udemy(Command):
    def __init__(self):
        name = 'udemy'
        help = 'Coleta os cupons da Udemy'
        reply_function_name = 'reply_text'
        super().__init__(
            name, help, reply_function_name,
        )

    def schedule(self):
        '''
        def send_udemy_coupons():
            bot.send_message(self.function(bot))
        bot.schedule_manager.add_schedule(
            send_udemy_coupons, 
            UM_DIA_EM_SEGUNDOS,
        )
        '''
        return False

    def function(self, update=None, context=None):
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

            text = "Esses foram os cupons da Udemy que encontrei:\n\n"

            index = 1
            for title, url in zip(title_list, url_list):
                text += f'{index}) <a href="{url}">{title}</a>\n'
                index += 1
        except Exception as error:
            logger.error(error)

        return {'update': update, 'text':text}
