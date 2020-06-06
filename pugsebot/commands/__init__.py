from .about import About
from .help import Help
from .links import Links
from .memes import Memes
from .news import News
from .projects import Projects
from .say import Say
from .udemy import Udemy

command_list = [
    Udemy(), News(), Projects(), Memes(),
    Say(), About(), Help(), Links(),
]