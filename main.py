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

    # create our bot instance
    bot = Client(
        intents=Intents.DEFAULT,  # intents are what events we want to receive from discord, `DEFAULT` is usually fine
        auto_defer=True,  # automatically deferring interactions
        activity="Destroying your D",  # the status message of the bot
    )

    bot.load_extension("ddd_commands")  # load the extension we made earlier

    # start the bot
    bot.start(os.getenv("TOKEN"))