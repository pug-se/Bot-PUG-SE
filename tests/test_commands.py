import unittest

from telegram.message import Message
from telegram.update import Update

from commands.about import About
from commands.faq import FAQ
from commands.links import Links
from commands.news import News
from commands.projects import Projects
from commands.say import Say
from commands.udemy import Udemy
from commands.help import Help
from commands.book import Book


def mock_update(message_text):
    """Mock a python-telegram-bot update object."""
    message = Message(0, from_user=None, date=None, chat=0, text=message_text)
    return Update(0, message=message)


def mock_reply_method(update=None, content=None):
    """Mock a reply method."""
    return mock_update(content)


class TestAbout(unittest.TestCase):
    """Test about functionalities."""

    def test_function(self):
        """Test about function."""
        result = About().function()
        self.assertIn("comunidade", result)
        self.assertIn("contribuir", result)


class TestBook(unittest.TestCase):
    """Test book functionalities."""

    def test_function(self):
        """Test book function."""
        result = Book().function()
        self.assertIn("Livro", result)
        self.assertIn("gratuito", result)
        self.assertIn("https://www.packtpub.com/free-learning", result)


class TestLinks(unittest.TestCase):
    """Test links functionalities."""

    def test_function(self):
        """Test links function."""
        result = Links().function()
        self.assertIn("links", result)
        self.assertIn("Python", result)


class TestMemes(unittest.TestCase):
    """Test memes functionalities."""

    def test_get_url_image_vida_programador(self):
        """Test get_url_image_vida_programador."""
        pass

    def test_get_url_image_turnoff_us(self):
        """Test get_url_image_turnoff."""
        pass

    def test_get_random_meme_image(self):
        """Test get_random_meme_image."""
        pass


class TestNews(unittest.TestCase):
    """Test news functionalities."""

    def test_function(self):
        """Test news function."""
        result = News().function()
        self.assertIn("notícia", result)
        self.assertIn("http", result)


class TestProjects(unittest.TestCase):
    """Test projects functionalities."""

    def test_function(self):
        """Test projects function."""
        result = Projects().function()
        self.assertIn("projetos", result)
        self.assertIn("http", result)


class TestSay(unittest.TestCase):
    """Test say functionalities."""

    def test_function(self):
        """Test say function."""
        result = Say().function()
        self.assertEqual("", result)

        result = Say().function(mock_update("test"))
        self.assertEqual("test", result)


class TestUdemy(unittest.TestCase):
    """Test udemy functionalities."""

    def test_function(self):
        """Test udemy function."""
        result = Udemy().function()
        self.assertIn("Udemy", result)
        self.assertIn("http", result)


class TestFAQ(unittest.TestCase):
    """Test FAQ functionalities."""

    def test_function(self):
        """Test FAQ function."""
        result = FAQ().function()
        self.assertIn("O que é Python?", result)
        self.assertIn("https://www.python.org/dev/peps/pep-0008", result)


class TestHelp(unittest.TestCase):
    """Test help functionalities."""

    def test_function(self):
        """Test help function."""
        result = Help().function()
        self.assertIn("/help", result)
        self.assertIn("/udemy", result)
        self.assertIn("/news", result)
