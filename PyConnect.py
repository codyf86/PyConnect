#!/usr/local/bin/python3
###############################################################################
#!    This program is free software: you can redistribute it and/or modify
#!    it under the terms of the GNU General Public License as published by
#!    the Free Software Foundation, either version 3 of the License, or
#!    (at your option) any later version.

#!    This program is distributed in the hope that it will be useful,
#!    but WITHOUT ANY WARRANTY; without even the implied warranty of
#!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#!    GNU General Public License for more details.

#!    You should have received a copy of the GNU General Public License
#!    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#!    Copyright Cody Ferber, 2019.
###############################################################################
from Commands import *
from contextlib import closing
from discord.ext import commands
import asyncio
import discord

class Client:
###############################################################################
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
#       print(exception_type)
#       print(exception_value)
#       print(traceback)
        return True

    def __init__(self):
        self.bot = commands.Bot(command_prefix='!')
        self.on_ready = self.bot.event(self.on_ready)
        self.on_message = self.bot.event(self.on_message)
        self.bot.load_extension('Commands')

###############################################################################
    async def on_ready(self):
        print('The bot is ready!')
        await self.bot.change_presence(activity=discord.Game(name=
                'Project 1999'))

###############################################################################
    async def on_message(self, message):
        await self.bot.process_commands(message)

###############################################################################
def main():
    with Client() as client:
        client.bot.run(Commands.get_cfg(None, '[TOKEN]'))

if __name__ == "__main__":
    main()
