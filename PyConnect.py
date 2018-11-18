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

#!    Copyright Cody Ferber, 2016.
###############################################################################
from contextlib import closing
import aiohttp
import asyncio
import datetime
import discord
import io
import sys

###############################################################################
class Client():
###############################################################################
    bot = discord.Client()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
#       print(exception_type)
#       print(exception_value)
#       print(traceback)
        return True

    def __init__(self):
        return None

###############################################################################
    def get_cfg(self, cfgvar):
        with closing(open('PyConnect.ini', 'r')) as file:
            buffer = file.read(None).splitlines()
            value = buffer.pop(buffer.index(cfgvar) + 1)
            return value

###############################################################################
    async def get_request(self, getvar):
        async with aiohttp.get(getvar) as r:
            return r.status, r.url

###############################################################################
    @bot.event
    async def on_ready():
        print('The bot is ready!')
        await Client.bot.change_presence(game=discord.Game(name='Project 1999'))

###############################################################################
    @bot.event
    async def on_message(message):
        if message.content == '!shutdown':
            print('Shutting down!')
            await Client.bot.send_message(message.channel, 'Shutting down!')
            await Client.bot.close()
        if message.content == '!status':
            await Client.bot.send_message(message.channel,
                    await Client.get_request(None, 'http://www.discord.com'))
            await Client.bot.send_message(message.channel, 'Currently tracking '
                    + Client.get_cfg(None, '[TARGET]'))

###############################################################################
    async def track():
        await Client.bot.wait_until_ready()
        while not Client.bot.is_closed:
            with closing(open(Client.get_cfg(None, '[PARSE]'), 'r')) as file:
                buffer = file.read(None)
                value = buffer.find(Client.get_cfg(None, '[TARGET]'))
                if value is not -1:
                    await Client.bot.send_message(
                            Client.bot.get_channel('513486044772171784'),
                                    'Target found!')
                    await asyncio.sleep(30)
                else:
                    await asyncio.sleep(30)

###############################################################################
def main():
    with Client() as client:
        client.bot.loop.create_task(Client.track())
        client.bot.run(client.get_cfg('[TOKEN]'))

if __name__ == "__main__":
    main()


