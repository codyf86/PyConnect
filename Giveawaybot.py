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

class Giveawaybot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.entries = []
        self.total_entries = 0

###############################################################################
    @commands.command(name='join', brief='Join Giveaway.',
            description='Join Giveaway.')
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def join(self, ctx):
        if ctx.message.author.id in self.entries:
            await ctx.send('You have already entered this drawing!')
        else:
            self.entries.append(ctx.message.author.id)
            self.total_entries = self.total_entries + 1
            await ctx.send('<@{}> has been added to the giveaway!'.format(ctx.message.author.id))

##############################################################################
    @commands.command(name='list', brief='list entries.',
            description='list entries.')
    @commands.cooldown(1, 15, commands.BucketType.channel)
    async def list(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Giveaway entries.')
        embed.add_field(name='User IDs:',value=self.entries, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Giveawaybot(bot))

