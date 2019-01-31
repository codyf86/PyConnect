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
from pygtail import Pygtail
import asyncio
import discord
import io

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

        Client.channel = Client.get_cfg(None,'[CHANNEL]')
        Client.parse   = Client.get_cfg(None, '[PARSE]')
        Client.role    = Client.get_cfg(None, '[ROLE]')
        Client.target1  = Client.get_cfg(None, '[TARGET1]')
        Client.target2  = Client.get_cfg(None, '[TARGET2]')
        Client.target3  = Client.get_cfg(None, '[TARGET3]')

###############################################################################
    def get_cfg(self, arg):
        with closing(open('PyConnect.ini', 'r')) as file:
            buffer = file.read(None).splitlines()
            value = buffer.pop(buffer.index(arg) + 1)
            return value

###############################################################################
    async def on_ready(self):
        print('The bot is ready!')
        await self.bot.change_presence(game=discord.Game(name='Project 1999'))

###############################################################################
    async def on_message(self, message):
        await self.bot.process_commands(message)

###############################################################################
    async def reload(self):
        Client.channel = Client.get_cfg(None,'[CHANNEL]')
        Client.parse   = Client.get_cfg(None, '[PARSE]')
        Client.role    = Client.get_cfg(None, '[ROLE]')
        Client.target1  = Client.get_cfg(None, '[TARGET1]')
        Client.target2  = Client.get_cfg(None, '[TARGET2]')
        Client.target3  = Client.get_cfg(None, '[TARGET3]')

###############################################################################
    async def set_var(self, arg1, arg2):
        if arg1 == 'channel':
            Client.channel = arg2
        if arg1 == 'parse':
            Client.parse = arg2
        if arg1 == 'role':
            Client.role = arg2
        if arg1 == 'target1':
            Client.target1 = arg2
        if arg1 == 'target2':
            Client.target2 = arg2
        if arg1 == 'target3':
            Client.target3 = arg2
    
###############################################################################
    async def track(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            for line in Pygtail(Client.parse):
                if Client.target1 in line or Client.target2 in line or Client.target3 in line:
                    print('Target found! Activating bat signal!')
                    await self.bot.send_message(
                        self.bot.get_channel(Client.channel), '!batsignal')
                    Client.fte = line
                    await Commands.set_var(None, 'fte', Client.fte)
            await asyncio.sleep(5)

###############################################################################
def main():
    with Client() as client:
        client.bot.loop.create_task(client.track())
        client.bot.run(client.get_cfg('[TOKEN]'))

if __name__ == "__main__":
    main()
