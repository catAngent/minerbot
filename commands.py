import math
import time

import command_processor
import player
from constants import *
from hikari import *
from typing import Union

import config
from command_processor import listen_command
from player import get_player
from utils import respond, translate, buttonfield
import lang

bot = None

@listen_command
async def inventory_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)

    search = command[1] if len(command) >= 2 else None
    search = search if search != "_" else None
    page = int(command[2]) if len(command) >= 3 else 1

    embed = Embed(
        color=0xb3ff7e,
        title=translate("inventory.name", p[LANGUAGE]),
        description=f'{search+" 🔍" if search else ""}\r\n{translate("inventory.page", p[LANGUAGE])} {page}',
    )
    items = [(id, count) for id, count in enumerate(p[INVENTORY]) if count != 0 if (search is None or search.lower() in translate(f"material.{id}", p[LANGUAGE]).lower() or search.lower() in translate(f"material.{id}", config.default_language).lower())]
    last_page = math.ceil(len(items)/config.inventory_page_size)
    if not 1 <= page <= last_page:
        await respond(
            e, notification=true,
            content=translate("inventory.no_page", p[LANGUAGE]),
        )
    items.sort(key=lambda x: x[1], reverse=True)
    items = items[config.inventory_page_size*(page-1):]
    items = items if len(items) <= config.inventory_page_size else items[:config.inventory_page_size]
    [embed.add_field(name=translate(f"material.{id}", p[LANGUAGE]).capitalize(), value=f"{count}{config.inventory_icons[id]}", inline=true) for id, count in items]
    await respond(
        e, notification=false,
        embed=embed,
        components=buttonfield(p[ID], [
            (f"item {c} --page-{page} --search-{search}", "", None, config.inventory_icons[c]) for c, i in items
        ]) + buttonfield(p[ID], [
            (f"inventory {search if search else '_'} {page-1 if page > 1 else last_page} --placeholder", translate("inventory.prev_page", p[LANGUAGE])),
            (f"inventory {search if search else '_'} {page+1 if page < last_page else 1}", translate("inventory.next_page", p[LANGUAGE])),
            ("invsearch", translate("inventory.search", p[LANGUAGE]), None, "🔍"),
            ("inventory" if search else "menu", translate("menu.button.back", p[LANGUAGE])),
        ])
    )
    player.set_player(p)

@listen_command
async def invsearch_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    await respond(
        e, notification=true,
        content=translate("inventory.search.question", p[LANGUAGE]),
    )
    ie = await bot.wait_for(GuildMessageCreateEvent, timeout=120, predicate=lambda x: x.author_id == p[ID] and x.message.channel_id == e.message.channel_id)
    await ie.message.delete()
    await command_processor.process_command(e, f"inventory {ie.message.content}")

@listen_command
async def item_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    item = 0
    try:
        item = int(command[1])
        if item < 0:
            raise Exception
        if item >= config.inventory_size:
            raise Exception
    except Exception as ex:
        await respond(
            e, notification=true,
            content=translate("item.command.no_item", p[LANGUAGE]))
        return
    await respond(
        e, notification=false,
        embed=Embed(color=0xb3ff7e, title=f"{p[INVENTORY][item]} {config.inventory_icons[item]}"),
        components=buttonfield(p[ID], [
            (f"craft from {item}", translate("item.craft.from", p[LANGUAGE])),
            (f"craft to {item}", translate("item.craft.to", p[LANGUAGE])),
        ]+[("inventory", translate("menu.button.back", p[LANGUAGE]))])
    )
    player.set_player(p)

@listen_command
async def craft_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    if len(command) != 3:
        await respond(
            e, notification=true,
            content=translate("craft.command.wrong_argument_number", p[LANGUAGE]))
        return
    source = "ingredients" if command[1] == "from" else ("results" if command[1] == "to" else None)
    if source is None:
        await respond(
            e, notification=true,
            content=translate("craft.command.wrong_argument", p[LANGUAGE]))
        return
    item = 0
    try:
        item = int(command[2])
        if item < 0:
            raise Exception
        if item >= config.inventory_size:
            raise Exception
    except Exception as ex:
        await respond(
            e, notification=true,
            content=translate("craft.command.no_item", p[LANGUAGE]))
        return

    embed = Embed(color=Color(0xb3ff7e))
    [embed.add_field(f"{translate(i['name'], p[LANGUAGE])}", f"{i['time']}⏳; {', '.join([f'{j[1]}{config.inventory_icons[j[0]]}' for j in i['ingredients']])} => {', '.join([f'{j[1]}{config.inventory_icons[j[0]]}' for j in i['results']])}") for i in config.crafting_recipes if item in [j[0] for j in i[source]]]
    await respond(
        e, notification=false,
        embed=embed,
        content="",
        components=buttonfield(p[ID], [
            (f"docraft {c}", f"{translate(i['name'], p[LANGUAGE])} {i['time']}⏳") for c, i in
            enumerate(config.crafting_recipes) if item in [j[0] for j in i[source]]
        ]+[(f"item {item}", translate("menu.button.back", p[LANGUAGE]))]),
    )
    player.set_player(p)

@listen_command
async def docraft_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    recipe = config.crafting_recipes[int(command[1])]
    if time.time() >= p[NEXT_WORK]:
        for i in recipe["ingredients"]:
            if p[INVENTORY][i[0]] < i[1]:
                await respond(
                    e, notification=true,
                    content=f"<@{p[ID]}> " + translate('crafting.no_resources', p[LANGUAGE]).format(
                        config.inventory_icons[i[0]]))
                return
        p[NEXT_WORK] = time.time() + recipe["time"]
        await respond(
            e, notification=true,
            content=f"<@{p[ID]}> " + translate('crafting.started', p[LANGUAGE]).format(f"<t:{int(time.time()+recipe['time'])}:R>"))
        for i in recipe["ingredients"]:
            p[INVENTORY][i[0]] -= i[1]
        p[TO_ADD] += [(time.time() + recipe["time"], recipe["results"])]
    else:
        await respond(
            e, notification=true,
            content=f"<@{p[ID]}> " + translate('crafting.cooldown', p[LANGUAGE]).format(
                int(p[NEXT_WORK] - time.time())))
    player.set_player(p)

@listen_command
async def lang_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    await respond(
        e, notification=false,
        embed=Embed(color=Color(0xb3ff7e), title=translate("lang.select", p[LANGUAGE])),
        content="",
        components=buttonfield(p[ID],
                                [(f"setlang {i}", translate("lang.name", f"{i}")) for i in lang.languages.keys()] +
                                [("menu", translate("menu.button.back", p[LANGUAGE]))]
        )
    )

@listen_command
async def setlang_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    p[LANGUAGE] = command[1]
    await respond(
        e, notification=true,
        content=f"<@{p[ID]}> " + translate("lang.changed", p[LANGUAGE]))
    player.set_player(p)

@listen_command
async def menu_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    await respond(
        e, notification=false,
        content="",
        embed=Embed(
            color=Color(0xb3ff7e),
            title=translate("menu.id", p[LANGUAGE]).format(p[ID])+"\r\n"+(translate("menu.time_until_work", p[LANGUAGE]).format(int(p[NEXT_WORK] - time.time())) if int(p[NEXT_WORK] - time.time()) > 0 else translate("menu.can_work", p[LANGUAGE]))
        ),

        components=buttonfield(p[ID], [
            ("inventory", translate("inventory.name", p[LANGUAGE])),
            ("settings", translate("settings.name", p[LANGUAGE])),
            ("lang", translate("lang.lang", p[LANGUAGE])),
        ])
    )

@listen_command
async def settings_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    if len(command) >= 3:
        setting = int(command[1])
        mode = bool(int(command[2]))
        p[SETTINGS][setting] = mode
        player.set_player(p)
        await respond(
            e, notification=True,
            content=translate("settings.changed", p[LANGUAGE]).format(translate(f"settings.{setting}", p[LANGUAGE]), translate("settings.true" if mode else "settings.false", p[LANGUAGE]))
        )
    embed = Embed(color=Color(0xb3ff7e), title=translate("settings.name", p[LANGUAGE]))
    await respond(
        e, notification=False, remove_old_notification=p[SETTINGS][SEPARATE_NOTIFICATIONS],
        embed=embed,
        components=buttonfield(p[ID], [
            (f"settings {setting} {0 if p[SETTINGS][setting] else 1}", translate(f"settings.{setting}", p[LANGUAGE]), p[SETTINGS][setting]) for setting in range(config.settings_size)
        ]+[("menu", translate("menu.button.back", p[LANGUAGE]), None)])
    )
