import logging
import os

import requests
from config import COMMAND_HANDLER_ROUTE, CONTROL_KEYS
from datamodel import GameStatus, Player
from twitchio.ext import commands
from twitchio.message import Message

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.command_prefix = os.environ.get("COMMAND_PREFIX")
        super().__init__(
            token=os.environ.get("ACCESS_TOKEN"),
            prefix=os.environ.get("COMMAND_PREFIX"),
            initial_channels=[os.environ.get("CHANNEL")],
        )

        # TODO: if new game is started, then clear player_list and next_game_queue
        # player_list is a dictionary of twitch_id: Player
        # self.player_list = {'964201114': Player(twitch_id='964201114', username='damtien440', player_team='player_1')}
        self.player_list = {}
        self.next_game_queue = {}

        self.game = GameStatus(
            game_id=None, game_status=None, character_1=None, character_2=None
        )

        # TODO: Init API for whispering

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        logger.info("Bot is logged in as %s", self.nick)
        logger.info("User ID: %s", self.user_id)

    async def event_message(self, message: Message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        # logger.info(
        #     "%s (%s): %s", message.author.name, message.author.id, message.content
        # )

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        if isinstance(message.content, str) and message.content.startswith("?"):
            logger.info("Received command")
            await self.handle_commands(message)

            # TODO: add game status check here to initiate game

            return

        logger.info("Usual chat")

        if message.author.id not in self.player_list:
            return

        action_key = self._get_action_key(message)
        if action_key is None:
            return

        logger.info("There is an action key")

        response = self._send_action_key_to_gameapi(
            action_key, self.player_list[message.author.id]
        )

        logger.info("Sent action key to game backend")

        self._update_game_status(response.json())

        # TODO: If the game ended, then output the result to chat,
        # and remove the players from the player_list, procede to the next game

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"Hello {ctx.author.name}!")

    @staticmethod
    def _get_action_key(message: Message) -> str or None:
        """Check if message contains a valid action key"""
        action_key = message.content[0].lower()

        if action_key in CONTROL_KEYS:
            return action_key

        return None

    @staticmethod
    def _send_action_key_to_gameapi(action_key: str, player: Player):
        """Send action key to API"""
        status = send_to_api(
            COMMAND_HANDLER_ROUTE, {player.player_team: {"actions": action_key}}
        )

        return status

    def _update_game_status(self, game_status):
        """Update game status"""
        self.game.game_status = game_status["game_status"]
        self.game.character_1.hp = game_status["character_1"]["hp"]
        self.game.character_1.energy = game_status["character_1"]["energy"]
        self.game.character_2.hp = game_status["character_2"]["hp"]
        self.game.character_2.energy = game_status["character_2"]["energy"]


def send_to_api(endpoint, json_content):
    """Send json content to API"""
    response = requests.post(endpoint, json=json_content)
    logger.info("Response from API: %s", response)
    return response
