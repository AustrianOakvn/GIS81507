import logging
import os

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
            initial_channels=[os.environ.get("CHANNEL")]
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
        logger.info("%s (%s): %s", message.author.name, message.author.id, message.content)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        if isinstance(message.content, str) and message.content.startswith("?"):
            logger.info("Received command")
            await self.handle_commands(message)
            return

        logger.info("Usual chat")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"Hello {ctx.author.name}!")
