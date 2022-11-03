from hikari import *

from constants import *
import config
from typing import Union

registered_commands = {}

def listen_command(func):
    registered_commands[func.__name__.replace("_command", "")] = func
    return func

async def process_command(e: Union[MessageCreateEvent, ComponentInteraction], raw_cmd):
    command = raw_cmd.split(" ")
    flags = []
    for i in command[::-1]:
        if i.startswith("--"):
            command.remove(i)
            flags.append(i[2:])
    cmd = registered_commands.get(command[0])
    if cmd is not None:
        await cmd(e, command, flags, raw_cmd)
