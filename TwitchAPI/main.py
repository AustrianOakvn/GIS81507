import argparse
import logging

from dotenv import load_dotenv

from bot import Bot

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


if __name__ == "__main__":
    # Load variables from .env file
    load_dotenv()

    # args parser to add simulation mode
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulation", action="store_true", help="Run in simulation mode")

    args = parser.parse_args()

    # print(args.simulation)

    # Load twitch chat bot
    bot = Bot(random_simulator=args.simulation)
    bot.run()
    # bot.run() is blocking and will stop execution of any below code here until stopped or closed.
