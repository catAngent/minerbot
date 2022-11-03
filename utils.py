import lang
import config
from hikari import *
from typing import Union
import player
from constants import *

bot = None

def translate(token, language):
    if lang.languages.get(language) and lang.languages.get(language).get(token):
        return lang.languages[language][token]
    if lang.languages.get(config.default_language) and lang.languages.get(config.default_language).get(token):
        return lang.languages[config.default_language][token]
    return token


async def respond(e: Union[MessageCreateEvent, ComponentInteraction], notification=False, remove_old_notification=True, **kwargs):
    p = player.get_player(e.author_id.real) if isinstance(e, MessageCreateEvent) else player.get_player(e.user.id.real)
    if isinstance(e, ComponentInteraction):
        if notification and p[SETTINGS][SEPARATE_NOTIFICATIONS]:
            await e.execute(**kwargs, flags=MessageFlag.EPHEMERAL)
        else:
            if "content" not in kwargs.keys() and remove_old_notification:
                await e.message.edit("", **kwargs)
            else:
                await e.message.edit(**kwargs)
    else:
        await e.message.respond(**kwargs)


def buttonfield(id: int, ls):
    a = []
    i = 0
    for _ in range(5):
        r = bot.rest.build_action_row()
        for __ in range(5):
            b = r.add_button(
                (1 + i % 2) if (len(ls[i]) <= 2 or ls[i][2] is None) else (3 if ls[i][2] else 4),
                f"{id};{ls[i][0].replace(';', '')}"
            )
            b.set_label(ls[i][1])
            if len(ls[i]) >= 4 and ls[i][3] is not None:
                b.set_emoji(Emoji.parse(ls[i][3]))
            b.add_to_container()
            i += 1
            if i >= len(ls):
                break
        a.append(r)
        if i >= len(ls):
            break
    return a


