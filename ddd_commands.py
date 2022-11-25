from naff import (
    Client,
    Button,
    Embed,
    ButtonStyles,
    ComponentContext,
    Extension, InteractionContext,
    component_callback, slash_command,
)
from collections import defaultdict
from db_driver import get_events, log_event
import os


class DDDExtension(Extension):
    bot: Client

    @slash_command(name="nut", description="Reports that you have nutted.")
    async def nut(self, ctx: InteractionContext):
        # adds a component to the message
        confirm_button = Button(
            style=ButtonStyles.GREEN,
            label="Confirm ✅",
            custom_id="nut_confirmation_button"
        )
        cancel_button = Button(
            style=ButtonStyles.RED,
            label="Cancel ❌",
            custom_id="nut_cancel_button"
        )

        msg = "Press the green button to confirm that you have nutted." \
              " Otherwise, press the red button to cancel." \
              " Remember to be honest."

        # respond to the interaction
        await ctx.send(msg, components=[confirm_button, cancel_button], ephemeral=True)


    @component_callback("nut_confirmation_button")
    async def nut_confirm_callback(self, ctx: ComponentContext):
        log_event(ctx.author.id)

        announce_button = Button(
            style=ButtonStyles.GREEN,
            label="Yes, announce it!",
            custom_id="nut_announce_button")

        no_announce_button = Button(
            style=ButtonStyles.RED,
            label="No, don't announce it.",
            custom_id="nut_no_announce_button")
        
        await ctx.edit_origin(content="Congratulations, you have nutted. Would you like to announce this to the server?",
                              components=[announce_button, no_announce_button])

    @component_callback("nut_cancel_button")
    async def nut_cancel_callback(self, ctx: ComponentContext):
        await ctx.edit_origin(content="Nut cancelled.", components=[])

    @component_callback("nut_announce_button")
    async def nut_announce_callback(self, ctx: ComponentContext):
        await ctx.edit_origin(content="Announcing...", components=[])

        announce_channel = self.bot.get_channel(int(os.getenv("CHANNEL")))

        msg = "Congratulations, <@{}> has nutted!".format(ctx.author.id)

        await announce_channel.send(msg)

    @component_callback("nut_no_announce_button")
    async def nut_no_announce_callback(self, ctx: ComponentContext):
        await ctx.edit_origin(content="Announcement cancelled.", components=[])

    @slash_command(name="leaderboard", description="Shows the leaderboard.")
    async def leaderboard(self, ctx: InteractionContext):
        events = get_events()

        leaderboard = defaultdict(int)
        for event in events:
            user_id = event[1]
            leaderboard[user_id] += 1

        leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)

        embed = Embed(title="Leaderboard")

        msg = ""
        for user_id, count in leaderboard:
            msg += f"<@{user_id}>: {count}\n"

        embed.description = msg

        await ctx.send(embed=embed)


def setup(bot: Client):
    """Let naff load the extension"""

    DDDExtension(bot)