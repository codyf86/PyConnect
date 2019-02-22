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
import asyncio
import discord

class Rpgbot:
    def __init__(self, bot):
        self.bot = bot
        self.level = {}
        self.xp = {}
        self.get_next_level = {}
        self.get_next_xp = {}
        self.get_xp_remain = {}
        self.next_level = [[2,  5],
                           [3, 10],
                           [4, 15],
                           [5, 20],
                           [6, 25],
                           [7, 30],
                           [8, 35],
                           [9, 40],
                           [10, 45],
                           [11, 50],
                           [12, 55],
                           [13, 60],
                           [15, 65],
                           [16, 70],
                           [17, 75],
                           [18, 80],
                           [19, 85],
                           [20, 90],
                           [21, 95],
                           [22, 100],
                           [23, 105],
                           [24, 110],
                           [25, 115]]

###############################################################################
    @commands.command(name='attack', brief='Attack a monster.',
            description='Attack a monster.')
    @commands.cooldown(1, 2, commands.BucketType.channel)
    async def attack(self, ctx):
        author_id = ctx.message.author.id
        get_next_level = self.next_level[self.level[author_id] -1 ][0]
        get_next_xp = self.next_level[get_next_level - 2][1]
        get_xp_remain = get_next_xp - self.xp[author_id]
        number = randint(0, 100)
        if (number >= 40):
            await ctx.send('You have defeated the monster!')
            if (get_xp_remain >= 1):
                get_xp_remain = get_xp_remain - 1
                self.xp[author_id] = self.xp[author_id] + 1
                await ctx.send('You gain 1 XP!')
                if (get_xp_remain == 0):
                    self.level[author_id] = self.level[author_id] + 1
                    await ctx.send('You have gained a level!')
                    await ctx.send('Welcome to level {}!'
                            .format(self.level[author_id]))
        elif (number >= 20) and (number <= 39):
            await ctx.send('You poop your pants and flee!')
        else:
            await ctx.send('You die bravely in battle!')
            if (get_xp_remain < 5):
                await ctx.send('You lose 1 XP!')
                self.xp[author_id] = self.xp[author_id] - 1
            else:
                await ctx.send('You lose 0 XP!')

###############################################################################
    @commands.command(name='charinfo', brief='Display character info.',
            description='Display character info.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def charinfo(self, ctx):
        author_id = ctx.message.author.id
        get_next_level = self.next_level[self.level[author_id] -1 ][0]
        get_next_xp = self.next_level[get_next_level - 2][1]
        get_xp_remain = get_next_xp - self.xp[author_id]
        self.get_next_level[author_id] = get_next_level
        self.get_next_xp[author_id] = get_next_xp
        self.get_xp_remain[author_id] = get_xp_remain
        await ctx.send('Level {}.'.format(self.level[author_id]))
        await ctx.send('{} XP.'.format(self.xp[author_id]))
        await ctx.send('You will gain a level in {} XP.'.format(get_xp_remain))

###############################################################################
    @commands.command(name='register', brief='Register account with rpgbot.',
            description='Register account with rpgbot.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def register(self, ctx):
        author_id = ctx.message.author.id
        self.level[author_id] = 1
        self.xp[author_id] = 0
        await ctx.send('User ID is now registered!')
        await ctx.send('Use !charinfo for character stats!')

###############################################################################
    @commands.command(name='roll', brief='Roll magical dice.',
            description='Roll magical dice.')
    @commands.cooldown(10, 30, commands.BucketType.channel)
    async def roll(self, ctx, *args):
        x = 0
        await ctx.send('A random die is rolled by {}.'.format(
                ctx.message.author.name))
        for num in args:
            if num:
                x = x + 1
        if x == 1:
            await ctx.send('It could have been any number'
                    'between 0 and {}, but this time it turned up a {}.'
                            .format(args[0], str(randint(0, int(args[0])))))
        elif x == 2:
            await ctx.send('It could have been any number'
                    'between {} and {}, but this time it turned up a {}.'
                            .format(args[0], args[1], str(randint(int(args[0]),
                                    int(args[1])))))
        else:
            await ctx.send('Invalid number of inputs!')

###############################################################################
def setup(bot):
    bot.add_cog(Rpgbot(bot))

