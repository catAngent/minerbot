import os
from hikari import *
from constants import *
from typing import Union
from command_processor import listen_command
from player import get_player
from utils import respond, translate
import lang
from pathlib import Path

bot = None

@listen_command
async def relang_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    if p[ID] not in [586501508997054475, 545978973872717835, 703645555754270741, 493029410367340546]:
        await respond(
            e, notification=false,
            content=translate("relang.no_permissions", p[LANGUAGE]))
        return
    await respond(
        e, notification=false,
        content=translate("relang.started", p[LANGUAGE]))
    err = lang.load()
    if err is None:
        await respond(
            e, notification=false,
            content=translate("relang.success", p[LANGUAGE]))
        warns = lang.check_for_warns()
        await e.message.respond(f"There is {len(warns)} warnings.")

        buffer = ""
        for warn in warns:
            buffer += warn+"\r\n"
            if len(buffer) > 1600:
                await e.message.respond(buffer)
                buffer = ""
        if buffer != "":
            await e.message.respond(buffer)
    else:
        await respond(
            e, notification=false,
            content=translate("relang.error_in_lang", p[LANGUAGE]).format(err[0], err[1]))

@listen_command
async def uplang_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    if p[ID] not in [586501508997054475, 545978973872717835, 703645555754270741, 493029410367340546]:
        await respond(
            e, notification=false,
            content=translate("uplang.no_permissions", p[LANGUAGE]))
        return
    if not e.message.attachments:
        await respond(
            e, notification=false,
            content=translate("uplang.no_file", p[LANGUAGE]))
    a = e.message.attachments[0]
    bs = "\\"
    with open(f"./lang/{a.filename.replace('/', '').replace(bs, '').replace('~', '').replace('..', '')}", "wb") as fp:
        async with a.stream() as stream:
            async for chunk in stream:
                fp.write(chunk)
    await respond(
        e, notification=false,
        content=translate("uplang.success", p[LANGUAGE]))

@listen_command
async def downlang_command(e: Union[MessageCreateEvent, ComponentInteraction], command, flags, raw_command):
    p = get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else get_player(e.user.id.real)
    if p[ID] not in [586501508997054475, 545978973872717835, 703645555754270741, 493029410367340546]:
        await respond(
            e, notification=false,
            content=translate("downlang.no_permissions", p[LANGUAGE]))
        return
    fls = [f for f in os.listdir("./lang/") if os.path.isfile(os.path.join("./lang/", f))]
    if len(command) == 1:
        await respond(
            e, notification=false,
            content=translate("downlang.list_of_files", p[LANGUAGE]) + "\r\n" + "\r\n".join(fls))
        return
    if command[1] not in fls:
        await respond(
            e, notification=false,
            content=translate("downlang.no_such_file", p[LANGUAGE]))
        return
    f = open(f"./lang/{command[1]}", "rb")
    await respond(
        e, notification=false,
        content=translate("downlang.success", p[LANGUAGE]), attachment=Path(f"./lang/{command[1]}"))
    f.close()
