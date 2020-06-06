from .about import About
from .memes import Memes
from .news import News
from .projects import Projects
from .say import Say
from .udemy import Udemy

command_list = [
    Udemy(), News(), Projects(), Memes(),
    Say(), About(),
]
