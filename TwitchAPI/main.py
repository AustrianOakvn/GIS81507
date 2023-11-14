import logging

from dotenv import load_dotenv

from bot import Bot


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


if __name__ == "__main__":
    # Load variables from .env file
    load_dotenv()

    # Load twitch chat bot
    bot = Bot()
    bot.run()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.
