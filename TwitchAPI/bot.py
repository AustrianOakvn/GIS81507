import random
from typing import List
import logging
import os
import threading
from time import sleep

import requests
from twitchio.ext import commands
from twitchio.message import Message


from config import ATTACK_KEYS, COMMAND_HANDLER_ROUTE, CONTROL_KEYS, MAPPING, MOVEMENT_KEYS, NUM_PLAYERS, PING_ROUTE
from datamodel import GameStatus, Player
from components.databases.bet_db import BetDatabase
from components.bet.bet_system import BetSystem


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

        # if new game is started, then clear player_list and next_game_queue

        # Bet database & system
        self.bet_db = BetDatabase()
        self.bet_system = BetSystem(self.bet_db)

        # player_list is a dictionary of twitch_id: Player
        # self.player_list = {'964201114': Player(twitch_id='964201114', username='damtien440', player_team='player_1')}
        self.player_list = {}
        self.next_game_queue = {}

        self.game = GameStatus(
           game_state=None, p1_stats=None, p2_stats=None
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

        # Print the contents of our message to console...
        # logger.info(
        #     "%s (%s): %s", message.author.name, message.author.id, message.content
        # )

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...

        if isinstance(message.content, str) and message.content.startswith(
            self.command_prefix
        ):
            logger.info("Received command")
            await self.handle_commands(message)
            return

        logger.info("Usual chat")

        if message.author.id not in self.player_list:
            return

        action_key = self._get_action_key(message)
        if action_key is None:
            return

        logger.info("There is an action key")

        self._collect_command(
            action_key, self.player_list[message.author.id]
        )

        logger.info("Sent action key to game backend")

        # self._update_game_status(response.json())

        # TODO: If the game ended, then output the result to chat,
        # and remove the players from the player_list, procede to the next game
        # self._procede_to_next_game()

    @commands.command()
    async def balance(self, ctx: commands.Context):
        """Check balance function. Invoked when users say "?balance"

        Args:
            ctx (commands.Context): Chat context
        """
        logger.debug("Player %s sent check balance command.", ctx.author.name)
        current_balance = self.bet_system.get_balance(ctx.author.id)
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
        status, message = self.bet_system.bet(ctx.author.id, amount, chosen_player)
        if status:
            logger.info("Executed bet command from user %s (%s) for player %d with amount of %d.", ctx.author.name, ctx.author.id, chosen_player, amount)
            new_balance = self.bet_db.get_balance(ctx.author.id)
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
    def _get_action_key(message: Message) -> str or None:
        """Check if message contains a valid action key"""
        action_key = message.content[0].upper()

        if action_key in CONTROL_KEYS:
            return action_key
        
        action_key = MAPPING[action_key]
        
        print("mapped action key: ", action_key)

        return action_key

    def _collect_command(self, action_key: str, player: Player):
        """Send action key to API"""
        if player.player_team == "player_1":
            self.p1_commands.append(action_key)
            
        elif player.player_team == "player_2":
            self.p2_commands.append(action_key)
            
        # print("sent action key: ", action_key)
        
        # return status

    def _update_game_status(self, game_status):
        """Update game status"""
        self.game.game_state = game_status["game_state"]
        self.game.p1_stats.hp = game_status["p1_stats"]["hp"]
        self.game.p1_stats.energy = game_status["p1_stats"]["energy"]
        self.game.p2_stats.hp = game_status["p2_stats"]["hp"]
        self.game.p2_stats.energy = game_status["character_2"]["energy"]
        
        # print("recieved game status: ", self.game.game_state)

    def _register_player(self, message: Message):
        if (message.author.id in self.player_list) or (
            message.author.id in self.next_game_queue
        ):
            return False

        self.next_game_queue[message.author.id] = Player(
            twitch_id=message.author.id,
            username=message.author.name,
            player_team="player_1" if len(self.player_list) % 2 == 0 else "player_2",
        )

        return True

    def _procede_to_next_game(self):
        """Procede to the next game"""
        if self.game.game_state == "finished":
            logger.info("Game ended")
            self.player_list.clear()

            for id, player in enumerate(self.next_game_queue, start=1):
                self.player_list[player.twitch_id] = player
                if id > NUM_PLAYERS:
                    break
            self.next_game_queue.clear()
            logger.info("New game started, player list has been updated")

    def _send_command(self, interval=1000):
        while True:
            
            # havest command from chat
            send_json = {
                "player_1": self.p1_commands,
                "player_2": self.p2_commands
            }
            
            # send_json = {
            #     "player_1": random.sample(MOVEMENT_KEYS + ATTACK_KEYS, 5),
            #     "player_2": random.sample(MOVEMENT_KEYS + ATTACK_KEYS, 5)
            # }
            
            print("sent command: ", send_json)
            
            self.p1_commands.clear()
            self.p2_commands.clear()
            
            response = send_to_api(COMMAND_HANDLER_ROUTE, send_json)
            
            print("recieved game status: ", response.json())
            
            # TODO: Detect game end, update player list
            
            self._update_game_status(response.json())
            self._procede_to_next_game()

            sleep(interval / 1000)


def send_to_api(endpoint, json_content):
    """Send json content to API"""
    response = requests.post(endpoint, json=json_content)
    logger.info("Response from API: %s", response)
    return response
