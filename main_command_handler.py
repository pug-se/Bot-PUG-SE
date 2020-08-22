"""Run bot command handler."""

from pugsebot.bot import PUGSEBot

from pugsebot.utils import environment

if __name__ == "__main__":
    PUGSEBot(environment.TOKEN).start()
