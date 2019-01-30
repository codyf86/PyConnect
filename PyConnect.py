#!/usr/local/bin/python3 -u
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
from discord.ext import commands
from discord.ext.commands import Bot
from pygtail import Pygtail
from random import *
import asyncio
import datetime
import discord
import io

###############################################################################
class Client():
###############################################################################
    bot = commands.Bot(command_prefix='!')

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
#       print(exception_type)
#       print(exception_value)
#       print(traceback)
        return True

    def __init__(self):
        Client.channel = Client.get_cfg(None, '[CHANNEL]')
        Client.parse   = Client.get_cfg(None, '[PARSE]')
        Client.role    = Client.get_cfg(None, '[ROLE]')
        Client.target1  = Client.get_cfg(None, '[TARGET1]')
        Client.target2  = Client.get_cfg(None, '[TARGET2]')
        Client.target3  = Client.get_cfg(None, '[TARGET3]')
        return None

###############################################################################
    @bot.command(pass_context=True)
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def batphone(ctx):
        role = discord.utils.get(ctx.message.server.roles, name=Client.role)
        await Client.bot.say('{} -> {}'.format(role.mention, Client.fte))

###############################################################################
    def get_cfg(self, arg):
        with closing(open('PyConnect.ini', 'r')) as file:
            buffer = file.read(None).splitlines()
            value = buffer.pop(buffer.index(arg) + 1)
            return value

###############################################################################
    @bot.event
    async def on_ready():
        print('The bot is ready!')
        await Client.bot.change_presence(game=discord.Game(name='Project 1999'))

###############################################################################
    @bot.event
    async def on_message(message):
        await Client.bot.process_commands(message)

###############################################################################
    @bot.command(pass_context=True)
    @commands.cooldown(10, 30, commands.BucketType.channel)
    async def roll(ctx, *args):
        x = 0
        await Client.bot.say('A random die is rolled by {}.'.format(
                ctx.message.author.name))
        for num in args:
            if num:
                x = x + 1
        if x == 1:
            await Client.bot.say('It could have been any number between 0'
                    ' and {}, but this time it turned up a {}.'.format(
                            args[0], str(randint(0, int(args[0])))))
        elif x == 2:
            await Client.bot.say('It could have been any number between {} '
                    'and {}, but this time it turned up a {}.'.format(
                            args[0], args[1], str(randint(int(args[0]),
                                    int(args[1])))))
        else:
            await Client.bot.say('Invalid number of inputs!')

###############################################################################
    @bot.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def set(ctx, arg1, arg2):
        if arg1 == 'channel':
            Client.channel = arg2
            await Client.bot.say('Channel set to: {}'.format(Client.channel))
        if arg1 == 'parse':
            Client.parse = arg2
            await Client.bot.say('Parse file set to: {}'.format(Client.parse))
        if arg1 == 'role':
            Client.role = arg2
            await Client.bot.say('Batphone role set to: {}'.format(Client.role))
        if arg1 == 'target1':
            Client.target1 = arg2
            await Client.bot.say('Target1 set to: {}'.format(Client.target1))
        if arg1 == 'target2':
            Client.target2 = arg2
            await Client.bot.say('Target2 set to: {}'.format(Client.target2))
        if arg1 == 'target3':
            Client.target3 = arg2
            await Client.bot.say('Target3 set to: {}'.format(Client.target3))

###############################################################################
    @bot.command(pass_context=True)
    async def shutdown(ctx):
        await Client.bot.say('Shutting down!')
        await Client.bot.logout()

###############################################################################
    @bot.command(pass_context=True)
    async def status(ctx):
        await Client.bot.say('(T)echnology for (P)repared (A)egis (R)aiding')
        await Client.bot.say('Talking in channel: {}'.format(Client.channel))
        await Client.bot.say('Parsing file: {}'.format(Client.parse))
        await Client.bot.say('Batphoning role: {}'.format(Client.role))
        await Client.bot.say('Tracking: {}, {}, and {}'.format(
                Client.target1, Client.target2, Client.target3))

###############################################################################
    async def track():
        await Client.bot.wait_until_ready()
        while not Client.bot.is_closed:
            for line in Pygtail(Client.parse):
                if Client.target1 or Client.target2 or Client.target3 in line:
                    print('Target found! Activating bat signal!')
                    await Client.bot.send_message(
                        Client.bot.get_channel(Client.channel), '!batsignal')
                    Client.fte = line
            await asyncio.sleep(5)

###############################################################################
def main():
    with Client() as client:
        client.bot.loop.create_task(Client.track())
        client.bot.run(client.get_cfg('[TOKEN]'))

if __name__ == "__main__":
    main()

