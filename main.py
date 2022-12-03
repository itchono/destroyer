import os

from dotenv import load_dotenv
from naff import Intents
from naff import Client
from db_driver import initialize_db


if __name__ == "__main__":
    # load the environmental vars from the .env file
    load_dotenv()

    # initialize the database
    initialize_db()

    intents_num = Intents.DEFAULT | Intents.GUILDS | Intents.GUILD_MEMBERS

    # create our bot instance
    bot = Client(
        intents=intents_num,
        auto_defer=True,  # automatically deferring interactions
        activity="Destroying your D",  # the status message of the bot
        fetch_members=True
    )

    bot.load_extension("ddd_commands")  # load the extension we made earlier

    # start the bot
    bot.start(os.getenv("TOKEN"))