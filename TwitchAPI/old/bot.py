from typing import Callable, Union

from twitchio.channel import Channel
from twitchio.ext import commands
from twitchio.user import User


class Bot(commands.Bot):
    def __init__(
        self,
        access_token: str,
        prefix: Union[str, Callable],
        initial_channels: Union[list, Callable],
    ):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(
            token=access_token, prefix=prefix, initial_channels=initial_channels
        )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"Hello {ctx.author.name}!")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message)
        print(message.author)
        print(message.author.name)
        print(message.timestamp)
        print(message.tags)
        print(message.channel)
        print(message.content)

        """{
            '@badge-info': 'predictions/NRG,founder/7', 
            'badges': 'predictions/blue-1,founder/0', 
            'client-nonce': '327d7fb472a789cbfeee1287765e15d8', 
            'color': '#DAA520', 
            'display-name': 'kamefortres', 
            'emotes': '', 
            'first-msg': '0', 
            'flags': '', 
            'id': 'e088040b-d729-4062-b3c4-c89be4da965b', 
            'mod': '0', 
            'returning-chatter': '0', 
            'room-id': '104833324', 
            'subscriber': '1', 
            'tmi-sent-ts': '1698478538062', 
            'turbo': '0', 
            'user-id': '149381353', 
            'user-type': ''
        }"""

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def event_join(self, channel: Channel, user: User):
        print(f"{user.name} has joined {channel.name}")
        return await super().event_join(channel, user)


if __name__ == "__main__":
    import os

    # load secrets from .env file
    from dotenv import load_dotenv

    load_dotenv()

    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    PREFIX = os.getenv("PREFIX")
    INITIAL_CHANNELS = os.getenv("INITIAL_CHANNELS").split(",")

    # This is our main entry point into our program...
    # We create an instance of our Bot class and run it...
    bot = Bot(
        access_token=ACCESS_TOKEN,
        prefix=PREFIX,  # This can be a callable which returns a list of strings or a string...
        initial_channels=INITIAL_CHANNELS,  # This can also be a callable which returns a list of strings...
    )
    bot.run()
