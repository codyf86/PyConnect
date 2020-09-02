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

#!    Copyright Cody Ferber, 2020.
###############################################################################
from contextlib import closing
from discord.ext import commands
import discord
import json

class Serverbot(commands.Cog):
###############################################################################
    def __init__(self, bot):
        self.bot = bot
        self.version = '1.00'
        with open('PyConnect.json') as config_file:
            self.config = json.load(config_file)
            self.ip = self.config['server']['ip']
            self.port = self.config['server']['port']

###############################################################################
    @commands.command(name='reload', brief='Reload config variables.',
            description='Reload config variables.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def reload(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Reloading config variables.')
        await ctx.send(embed=embed)
        with open('PyConnect.json') as config_file:
            self.config = json.load(config_file)
            self.ip = self.config['server']['ip']
            self.port = self.config['server']['port']

###############################################################################
    @commands.command(name='set', brief='Set config variable.',
            description='Set config variable.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def set(self, ctx, arg1, arg2):
        embed = discord.Embed(colour=discord.Colour(0x7ed321), title='Set:')
        if arg1 == 'ip':
            self.ip = arg2
            embed.add_field(name='IP:', value=self.ip, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'port':
            self.port = arg2
            embed.add_field(name='Port:', value=self.port, inline=False)
            await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='shutdown', brief='Shutdown bot.',
            description='Shutdown bot.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def shutdown(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Shutting Down!')
        await ctx.send(embed=embed)
        await self.bot.close()

###############################################################################
    @commands.command(name='status', brief='Display bot status.',
            description='Display bot status.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def status(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Riot Test Server Bot:\nVersion {}.'.format(self.version))
        embed.add_field(name='IP:', value=self.ip, inline=False)
        embed.add_field(name='Port:', value=self.port, inline=False)
        await ctx.send(embed=embed)

###############################################################################
def setup(bot):
    bot.add_cog(Serverbot(bot))

