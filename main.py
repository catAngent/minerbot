from hikari import *

import command_processor
import lang
import sqltools
import utils

import commands
import admin_commands

bot = None

def main():
    global bot
    
    tokenfile = open("./token", "r")
    bot = GatewayBot(token=tokenfile.read().replace("\r", "").replace("\n", ""), banner=None, intents=Intents.ALL)
    tokenfile.close()

    commands.bot = bot
    admin_commands.bot = bot
    utils.bot = bot

    sqltools.add_columns("users", [
        ("inventory", "BLOB", []),
        ("lang", "TEXT", "en"),
        ("next_work", "REAL", 0),
        ("to_add", "BLOB", []),
        ("settings", "BLOB", []),
    ])  # INTEGER TEXT REAL BLOB

    @bot.listen()
    async def on_start(e: StartedEvent):
        print("started.")
        await bot.update_presence(activity=Activity(name="ping me!", type=ActivityType.WATCHING))
        # asyncio.create_task(loop1())

    @bot.listen()
    async def on_command(e: MessageCreateEvent) -> None:
        if e.message.content and e.message.content.startswith("+"):
            await command_processor.process_command(e, e.message.content[1:])

    @bot.listen()
    async def on_ping(e: MessageCreateEvent) -> None:
        if e.message.content and e.message.content == f"<@{bot.get_me().id}>":
            await command_processor.process_command(e, "menu")

    @bot.listen()
    async def on_button(e: InteractionCreateEvent) -> None:
        i = e.interaction
        if isinstance(i, ComponentInteraction):
            metacmd = i.custom_id.split(";")
            cmd = metacmd[1].split(" ")
            if metacmd[0] != str(i.user.id.real):
                return
            await i.create_initial_response(ResponseType.MESSAGE_UPDATE)
            await command_processor.process_command(i, metacmd[1])

    lang.load()
    bot.run()


if __name__ == "__main__":
    main()
