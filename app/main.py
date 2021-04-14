from discord import Intents, Message
from discord.ext import commands
from discord_slash import SlashCommand
from cogwatch import Watcher
from loguru import logger

from app.config import DEVELOPMENT, bot_settings, logging_settings

logging_settings.setup_loguru()


class AuthBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            command_prefix=bot_settings.command_prefix,
            intents=Intents.all(),
        )

    async def on_ready(self):
        # Setup cogwatch
        logging_settings.intercept_logging("cogwatch")

        watcher = Watcher(
            self, path="app/cogs", debug=DEVELOPMENT, default_logger=False
        )
        await watcher.start()

        # Done
        logger.info("Discord bot ready!")

    async def on_message(self, message: Message):
        if message.author.bot:
            return

        # TODO: Remove this once it's a bit more developed (before production)
        if DEVELOPMENT:
            logger.info(
                f"[{message.guild.name} - {message.channel.name}] {message.author.name}"
                + f"#{message.author.discriminator}: {message.clean_content}"
            )

        await super().on_message(message)


bot = AuthBot()
slash = SlashCommand(
    bot, sync_commands=True, override_type=True  # , sync_on_cog_reload=True
)

bot.load_extension("app.cogs.goon_auth")
bot.run(bot_settings.discord_token)
