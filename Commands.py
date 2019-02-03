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
from pygtail import Pygtail
import asyncio
import discord

class Commands:
###############################################################################
    def __init__(self, bot):
        self.bot = bot
        self.background_task = self.bot.loop.create_task(self.track())

        self.channel = self.get_cfg('[CHANNEL]')
        self.parse   = self.get_cfg('[PARSE]')
        self.role    = self.get_cfg('[ROLE]')
        self.target1  = self.get_cfg('[TARGET1]')
        self.target2  = self.get_cfg('[TARGET2]')
        self.target3  = self.get_cfg('[TARGET3]')

###############################################################################
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def batphone(self, ctx):
        role = discord.utils.get(ctx.message.server.roles, name=self.role)
        await ctx.message.channel.send('{} -> {}'.format(role.mention,
                self.fte))

###############################################################################
    def get_cfg(self, arg):
        with closing(open('PyConnect.ini', 'r')) as file:
            buffer = file.read(None).splitlines()
            value = buffer.pop(buffer.index(arg) + 1)
            return value

###############################################################################
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def reload(self, ctx):
        await ctx.message.channel.send('Reloading config variables...')
        self.channel = self.get_cfg('[CHANNEL]')
        self.parse   = self.get_cfg('[PARSE]')
        self.role    = self.get_cfg('[ROLE]')
        self.target1  = self.get_cfg('[TARGET1]')
        self.target2  = self.get_cfg('[TARGET2]')
        self.target3  = self.get_cfg('[TARGET3]')
        await ctx.message.channel.send('OK!')

###############################################################################
    @commands.command()
    @commands.cooldown(10, 30, commands.BucketType.channel)
    async def roll(self, ctx, *args):
        x = 0
        await ctx.message.channel.send('A random die is rolled by {}.'.format(
                ctx.message.author.name))
        for num in args:
            if num:
                x = x + 1
        if x == 1:
            await ctx.message.channel.send('It could have been any number'
                    'between 0 and {}, but this time it turned up a {}.'
                            .format(args[0], str(randint(0, int(args[0])))))
        elif x == 2:
            await ctx.message.channel.send('It could have been any number'
                    'between {} and {}, but this time it turned up a {}.'
                            .format(args[0], args[1], str(randint(int(args[0]),
                                    int(args[1])))))
        else:
            await ctx.message.channel.send('Invalid number of inputs!')

###############################################################################
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def set(self, ctx, arg1, arg2):
        if arg1 == 'channel':
            await ctx.message.channel.send('Set channel to: {}'
                    .format(self.channel))
            self.channel = arg2
        if arg1 == 'parse':
            await ctx.message.channel.send('Set parse file to: {}'
                    .format(self.parse))
            self.parse = arg2
        if arg1 == 'role':
            await ctx.message.channel.send('Set batphone role to: {}'
                    .format(self.role))
            self.role = arg2
        if arg1 == 'target1':
            await ctx.message.channel.send('Set target1 to: {}'
                    .format(self.target1))
            self.target1 = arg2
        if arg1 == 'target2':
            await ctx.message.channel.send('Set target2 to: {}'
                    .format(self.target2))
            self.target2 = arg2
        if arg1 == 'target3':
            await ctx.message.channel.send('Set target3 to: {}'
                    .format(self.target3))
            self.target3 = arg2
        await ctx.message.channel.send('OK!')

###############################################################################
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def shutdown(self, ctx):
        await ctx.message.channel.send('Shutting down!')
        await self.bot.close()

###############################################################################
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def start(self, ctx):
        if self.background_task.done():
            self.background_task = self.bot.loop.create_task(self.track())
            await ctx.message.channel.send("Tracking loop started!")
        else:
            await ctx.message.channel.send("Tracking loop is already running!")

###############################################################################
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def status(self, ctx):
        await ctx.message.channel.send('(T)echnology for (P)repared (A)egis'
                ' (R)aiding')
        await ctx.message.channel.send('Parsing file: {}'.format(self.parse))
        await ctx.message.channel.send('Batphoning role:channel_id: {}:{}'
                .format(self.role, self.channel))
        await ctx.message.channel.send('Tracking: {}, {}, and {}'
                .format(self.target1, self.target2, self.target3))
        await ctx.message.channel.send('OK!')

###############################################################################
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def stop(self, ctx):
        if not self.background_task.done():
            self.background_task.cancel()
            await ctx.message.channel.send('Tracking loop stopped!')
        else:
            await ctx.message.channel.send('Tracking loop is not currently'
                    ' running!')

###############################################################################
    async def track(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            channel = self.bot.get_channel(int(self.channel))
            for line in Pygtail(self.parse):
                target_list = [self.target1 in line, self.target2 in line,
                        self.target3 in line]
                if any(target_list):
                    print('Target found! Activating bat signal!')
                    await channel.send('!batsignal')
                    self.fte = line
            await asyncio.sleep(5)

###############################################################################
def setup(bot):
    bot.add_cog(Commands(bot))
