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
from contextlib import closing
from discord.ext import commands
from random import *
from PyConnect import *
import asyncio
import discord

class Commands:
###############################################################################
    def __init__(self, bot):
        self.bot = bot

        Commands.channel = Client.get_cfg(None,'[CHANNEL]')
        Commands.parse   = Client.get_cfg(None, '[PARSE]')
        Commands.role    = Client.get_cfg(None, '[ROLE]')
        Commands.target1  = Client.get_cfg(None, '[TARGET1]')
        Commands.target2  = Client.get_cfg(None, '[TARGET2]')
        Commands.target3  = Client.get_cfg(None, '[TARGET3]')

###############################################################################
    @commands.command(pass_context=True)
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def batphone(self, ctx):
        role = discord.utils.get(ctx.message.server.roles, name=Commands.role)
        await self.bot.say('{} -> {}'.format(role.mention, Commands.fte))

###############################################################################
    @commands.command(pass_context=True)
    async def reload(self, ctx):
        await self.bot.say('Reloading config variables...')
        Commands.channel = Client.get_cfg(None,'[CHANNEL]')
        Commands.parse   = Client.get_cfg(None, '[PARSE]')
        Commands.role    = Client.get_cfg(None, '[ROLE]')
        Commands.target1  = Client.get_cfg(None, '[TARGET1]')
        Commands.target2  = Client.get_cfg(None, '[TARGET2]')
        Commands.target3  = Client.get_cfg(None, '[TARGET3]')
        await Client.reload(None)
        await self.bot.say('OK!')

###############################################################################
    @commands.command(pass_context=True)
    @commands.cooldown(10, 30, commands.BucketType.channel)
    async def roll(self, ctx, *args):
        x = 0
        await self.bot.say('A random die is rolled by {}.'.format(
                ctx.message.author.name))
        for num in args:
            if num:
                x = x + 1
        if x == 1:
            await self.bot.say('It could have been any number between 0'
                    ' and {}, but this time it turned up a {}.'.format(
                            args[0], str(randint(0, int(args[0])))))
        elif x == 2:
            await self.bot.say('It could have been any number between {} '
                    'and {}, but this time it turned up a {}.'.format(
                            args[0], args[1], str(randint(int(args[0]),
                                    int(args[1])))))
        else:
            await self.bot.say('Invalid number of inputs!')

###############################################################################
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def set(self, ctx, arg1, arg2):
        if arg1 == 'channel':
            await self.bot.say('Set channel to: {}'.format(Commands.channel))
            Commands.channel = arg2
        if arg1 == 'parse':
            await self.bot.say('Set parse file to: {}'.format(Commands.parse))
            Commands.parse = arg2
        if arg1 == 'role':
            await self.bot.say('Set batphone role to: {}'.format(Commands.role))
            Commands.role = arg2
        if arg1 == 'target1':
            await self.bot.say('Set target1 to: {}'.format(Commands.target1))
            Commands.target1 = arg2
        if arg1 == 'target2':
            await self.bot.say('Set target2 to: {}'.format(Commands.target2))
            Commands.target2 = arg2
        if arg1 == 'target3':
            await self.bot.say('Set target3 to: {}'.format(Commands.target3))
            Commands.target3 = arg2
        await Client.set_var(None, arg1, arg2)
        await self.bot.say('OK!')

###############################################################################
    async def set_var(self, arg1, arg2):
        if arg1 == 'fte':
            Commands.fte = arg2

###############################################################################
    @commands.command(pass_context=True)
    async def status(self, ctx):
        await self.bot.say('(T)echnology for (P)repared (A)egis (R)aiding')
        await self.bot.say('Talking in channel: {}'.format(Commands.channel))
        await self.bot.say('Parsing file: {}'.format(Commands.parse))
        await self.bot.say('Batphoning role: {}'.format(Commands.role))
        await self.bot.say('Tracking: {}, {}, and {}'.format(
                Commands.target1, Commands.target2, Commands.target3))


###############################################################################
def setup(bot):
    bot.add_cog(Commands(bot))
