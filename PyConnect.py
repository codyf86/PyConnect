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
import argparse
import datetime
import discord
import io
import requests
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

###############################################################################
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process command-line.')
        parser.add_argument('-v', action="store_true", required=False,
                                help='Verbose to log file.')
        self.args = parser.parse_args()

###############################################################################
    def doLog(self, input):
        if self.args.v is True:
            with closing(open(self.LOG, 'a')) as file:
                for row in input.splitlines():
                    file.write(row + '\n')

###############################################################################
    def getCfg(self, cfgvar):
        with closing(open('PyConnect.ini', 'r')) as file:
            buffer = file.read(None).splitlines()
            value = buffer.pop(buffer.index(cfgvar) + 1)
            return value

###############################################################################
    def Get(self):
        r = requests.get(self.HOST)
        print(r.status_code)
        print(r.text)

###############################################################################
    @bot.event
    async def on_ready():
        print('The bot is ready!')
        await Client.bot.change_presence(game=discord.Game(name='Tracker bot'))

###############################################################################
    @bot.event
    async def on_message(message):
        if message.content == '!status':
            await Client.bot.send_message(message.channel, 'Currently tracking '
                    + Client.getCfg(message, '[TARGET]'))

###############################################################################
if __name__ == "__main__":
    with Client() as client:
        client.bot.run(client.getCfg('[TOKEN]'))

