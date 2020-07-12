import discord
from discord.ext import commands

import os
import re

bot = commands.Bot(command_prefix='~')

plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')

for name in os.listdir(plugin_dir):
        path = os.path.join(plugin_dir, name)
        if os.path.isfile(path) and \
                (name.startswith('_') or not name.endswith('.py')):
            continue
        if os.path.isdir(path) and \
                (name.startswith('_') or not os.path.exists(
                    os.path.join(path, '__init__.py'))):
            continue

        m = re.match(r'([_A-Z0-9a-z]+)(.py)?', name)
        if not m:
            continue

        module_name = f'plugins.{m.group(1)}'
        try:
            bot.load_extension(module_name)
        except :
            pass

import os


bot.run(os.environ["discord_token"])
