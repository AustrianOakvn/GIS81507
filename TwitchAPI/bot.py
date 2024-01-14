from dataclasses import asdict
import json
import random
from typing import List, Dict
import logging
import os
import threading
from time import sleep

import requests
from twitchio.ext import commands
from twitchio.message import Message

from config import COMMAND_HANDLER_ROUTE, MAPPING_P1, MAPPING_P2, NUM_PLAYERS, STATUS_JSON_ADDRESS
from datamodel import GameStatus, Player
from components.databases.bet_db import BetDatabase
from components.bet.bet_system import BetSystem
from datamodel import Character

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, random_simulator=False):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.command_prefix = os.environ.get("COMMAND_PREFIX")
        super().__init__(
            token=os.environ.get("ACCESS_TOKEN"),
            prefix=os.environ.get("COMMAND_PREFIX"),
            initial_channels=[os.environ.get("CHANNEL")],
        )

        self.random_simulator = random_simulator

        # if new game is started, then clear player_list and next_game_queue

        # Bet database & system
        self.bet_db = BetDatabase()
        self.bet_system = BetSystem(self.bet_db)

        # player_list is a dictionary of twitch_id: Player
        # self.player_list = {'964201114': Player(twitch_id='964201114', username='damtien440', player_team='player_1')}
        self.player_list: Dict[str, Player] = {}
        self.next_game_queue: Dict[str, Player] = {}

        self.game = GameStatus(
           game_state="finish", p1_stats=Character(0, 0), p2_stats=Character(0, 0)
        )

        self.p1_commands = []
        self.p2_commands = []

        # start a thread checking game status every 0.5 seconds
        ping_thread = threading.Thread(target=self._send_command)
        ping_thread.start()

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

        if isinstance(message.content, str) and message.content.startswith(
            self.command_prefix
        ):
            # logger.info("Received command")
            await self.handle_commands(message)
            return

        # logger.info("Usual chat")

        if message.author.id not in self.player_list:
            return

        action_key = self._get_action_key(message, self.player_list[message.author.id].player_team == "player_1")
        if action_key is None:
            return

        # logger.info("There is an action key")

        self._collect_command(
            action_key, self.player_list[message.author.id]
        )

        # logger.info("Sent action key to game backend")


    @commands.command()
    async def balance(self, ctx: commands.Context):
        """Check balance function. Invoked when users say "?balance"

        Args:
            ctx (commands.Context): Chat context
        """
        logger.debug("Player %s sent check balance command.", ctx.author.name)

        current_balance = self.bet_system.get_balance(ctx.author.id, ctx.author.name)
        await ctx.send(f"User {ctx.author.name} has {current_balance} in balance.")

    @commands.command()
    async def bet(self, ctx: commands.Context):
        """Bet function. Invoked when users say "?bet amount"

        Args:
            ctx (commands.Context): Chat context
        """
        logger.info("Player %s sent bet command.", ctx.author.name)
        parts: List[str] = str(ctx.message.content).split()

        ### BEGIN OF COMMAND CHECK ###
        valid = True
        # Check bet command validity
        if len(parts) != 3:
            await ctx.send(f"Bet command from {ctx.author.name} was not executed due to syntax error.")
            valid = False

        # Check parts[1]: chosen player
        if valid and not (parts[1].isdigit() and 1 <= int(parts[1]) <= 2):
            await ctx.send(f"Bet command from {ctx.author.name} was not executed. Chosen player must be 1 or 2.")
            valid = False

        # Check parts[2]: amount of money
        if valid and not (parts[2].isdigit() and 0 < int(parts[2])):
            await ctx.send(f"Bet command from {ctx.author.name} was not executed. Amount of money must be an integer and bigger than 0.")
            valid = False

        if not valid:
            await ctx.send(f"Bet command syntax: ?bet <player> <amount>. Example: ?bet 1 100.")
            return

        chosen_player = int(parts[1])
        amount = int(parts[2])
        ### END OF COMMAND CHECK

        logger.debug("Bet command from player %s has valid syntax.", ctx.author.name)

        # Check if in wait list (no match fixing allowed)
        if ctx.author.id in self.next_game_queue:
            await ctx.send(f"Trying to match fixing? Shame on you, {ctx.author.name}.")
        else:
            status, message = self.bet_system.bet(ctx.author.id, ctx.author.name, amount, chosen_player)
            if status:
                logger.info("Executed bet command from user %s (%s) for player %d with amount of %d.", ctx.author.name, ctx.author.id, chosen_player, amount)
                new_balance = self.bet_db.get_balance_update_username(ctx.author.id, ctx.author.name)
                await ctx.send(f"User {ctx.author.name} placed a bet on player {chosen_player} for {amount}. New balance: {new_balance}.")
            else:
                logger.error("Bet command from user %s (%s) was not executed. Reason: %s", ctx.author.name, ctx.author.id, message)
                await ctx.send(f"Bet command from {ctx.author.name} was not executed. Reason: {message}")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command()
    async def register(self, ctx: commands.Context):
        """Register player"""
        self.bet_system.get_balance(ctx.author.id, ctx.author.name)
        result = self._register_player(ctx.message)

        if result:
            await ctx.send(
                f"Registered {ctx.author.name} to player queue for {self.next_game_queue[ctx.author.id].player_team}!"
            )
        else:
            await ctx.send(
                f"{ctx.author.name} is already in player_list or player_queue!"
            )

    @staticmethod
    def _get_action_key(message: Message, p1: bool) -> str or None:
        """Check if message contains a valid action key"""
        action_key = message.content.upper()

        # Filter
        if p1:
            action_keys_filtered = "".join([MAPPING_P1[i] for i in action_key if i in MAPPING_P1])
        else:
            action_keys_filtered = "".join([MAPPING_P2[i] for i in action_key if i in MAPPING_P2])
        # action_key = MAPPING.get(action_key, None)

        # print("mapped action key: ", action_key)

        return action_keys_filtered[:10]

    def _collect_command(self, action_key: [str], player: Player):
        """Send action key to API"""
        if player.player_team == "player_1":
            self.p1_commands.extend(action_key)

        elif player.player_team == "player_2":
            self.p2_commands.extend(action_key)

        # print("sent action key: ", action_key)

        # return status

    def _update_game_status(self, game_status: dict):
        """Update game status"""
        # print(game_status)
        if len(list(game_status.keys())) == 0:
            return

        self.game.game_state = game_status.get("game_state", "nothing")

        if game_status.get("p1_stats") is None:
            # Create dummy info
            self.game.p1_stats.hp = 400
            self.game.p1_stats.energy = 0
            self.game.p2_stats.hp = 400
            self.game.p2_stats.energy = 0
        else:
            self.game.p1_stats.hp = game_status["p1_stats"]["hp"]
            self.game.p1_stats.energy = game_status["p1_stats"]["energy"]
            self.game.p2_stats.hp = game_status["p2_stats"]["hp"]
            self.game.p2_stats.energy = game_status["p2_stats"]["energy"]

        # print("recieved game status: ", self.game.game_state)

    def _register_player(self, message: Message):
        if (message.author.id in self.player_list) or (
            message.author.id in self.next_game_queue
        ):
            return False

        self.next_game_queue[message.author.id] = Player(
            twitch_id=message.author.id,
            username=message.author.name,
            player_team="player_1" if len(self.next_game_queue) % 2 == 0 else "player_2",
        )

        return True

    def _procede_to_next_game(self, max_player=NUM_PLAYERS):
        """Procede to the next game"""
        if self.game.game_state == "finished":
            logger.info("Game ended")
            # self.player_list.clear()

            if self.game.p1_stats.hp == self.game.p2_stats.hp:
                # Draw
                winner = 0
                to_be_awarded = list(self.player_list.keys())
            else:
                # P1/P2 wins
                winner = 1 if self.game.p1_stats.hp > self.game.p2_stats.hp else 2
                to_be_awarded = list(
                    player_id for player_id, _player in self.player_list.items()
                    if _player.player_team == f"player_{winner}"
                )

            self.bet_system.round_finish(winner, to_be_awarded)

            self.player_list.clear()

            # add players in next_game_queue to player_list
            to_be_clear = []
            for id, player in enumerate(self.next_game_queue.values(), start=1):
                self.player_list[player.twitch_id] = player
                to_be_clear.append(player.twitch_id)
                if id == max_player:
                    break

            for id in to_be_clear:
                self.next_game_queue.pop(id)

            # self.next_game_queue.clear()

            logger.info("New game started, player list has been updated")

    def _send_command(self, interval=500):
        while True:
            # havest command from chat

            send_json = {
                "player_1": self.p1_commands[:],
                "player_2": self.p2_commands[:]
            }

            # print("sent command: ", send_json)

            self.p1_commands.clear()
            self.p2_commands.clear()

            response = send_to_api(COMMAND_HANDLER_ROUTE, send_json)

            # print("recieved game status: ", response.json())

            self._update_game_status(response.json())
            self._procede_to_next_game()
            self._update_status_to_gui()

            sleep(interval / 1000)

    def _update_status_to_gui(self):
        """Update status to GUI"""

        status = {
            "top_5_balance": self.bet_db.top_balance(5),
            "game_status": asdict(self.game),
            "player_list": [asdict(player) for player in self.player_list.values()],
            "next_game_queue": [asdict(player) for player in self.next_game_queue.values()]
        }

        with open(STATUS_JSON_ADDRESS, "w") as f:
            f.write(json.dumps(status))


def send_to_api(endpoint, json_content):
    """Send json content to API"""
    response = requests.post(endpoint, json=json_content)
    # logger.info("Response from API: %s", response)
    return response
