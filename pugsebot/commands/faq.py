"""Defines FAQ command."""

from ..utils.command import CommandBase

MESSAGE_HEADER = "Perguntas frequentes sobre o Python:"

ASKS_AND_URL_ANSWERS = {
    "O que é Python?": (
        "https://docs.python.org/pt-br/3/faq/general.html#what-is-python"
    ),
    (
        "O Python é uma boa linguagem para quem"
        "está começando na programação agora?"
    ): (
        "https://docs.python.org/pt-br/3/faq/general.html"
        "#is-python-a-good-language-for-beginning-programmers"
    ),
    "Eu nunca programei antes. Existe um tutorial básico do Python?": (
        "https://docs.python.org/pt-br/3/tutorial/index.html#tutorial-index"
    ),
    "Quantas pessoas usam o Python?": (
        "https://docs.python.org/pt-br/3/faq/general.html"
        "#how-many-people-are-using-python"
    ),
    "Quão estável é o Python?": (
        "https://docs.python.org/pt-br/3/faq/general.html#how-stable-is-python"
    ),
    "Existem alguns livros sobre o Python?": (
        "https://wiki.python.org/moin/PortuguesePythonBooks"
    ),
    "Para o que Python é excelente?": (
        "https://docs.python.org/pt-br/3/faq/general.html"
        "#what-is-python-good-for"
    ),
    (
        "Existem padrões para a codificação ou um guia"
        "de estilo utilizado pela comunidade Python?"
    ): "https://www.python.org/dev/peps/pep-0008",
    "Como encontrar um módulo ou aplicação para realizar uma tarefa X?": (
        "https://docs.python.org/pt-br/3/faq/library.html"
        "#how-do-i-find-a-module-or-application-to-perform-task-x"
    ),
}


class FAQ(CommandBase):
    """Configure FAQ command."""

    def __init__(self):
        """Pass arguments to CommandBase init."""
        super().__init__(
            name="faq",
            help_text="Perguntas Frequentes sobre Python",
            reply_function_name="reply_text",
            schedule_interval=None,
        )

    def function(self, update=None, context=None):
        """Return a FAQ formated string about Python."""
        text = MESSAGE_HEADER + "\n"
        for ask, url_answer in ASKS_AND_URL_ANSWERS.items():
            text += '* <a href="{}">{}</a>\n'.format(url_answer, ask)
        return text
