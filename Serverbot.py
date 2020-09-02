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
import telnetlib

class Serverbot(commands.Cog):
###############################################################################
    def __init__(self, bot):
        self.bot = bot
        self.version = '1.00'
        with open('PyConnect.json') as config_file:
            self.config = json.load(config_file)
            self.ip = self.config['server']['ip']
            self.port = self.config['server']['port']

        self.telnet = telnetlib.Telnet(self.ip, self.port)
        print(self.telnet.read_until(b'> ').decode('ascii'))

###############################################################################
    @commands.command(name='gmsay', brief='Send gmsay message to world.',
            description='Send gmsay message to world.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def gmsay(self, ctx, *args):
        x = 0
        for num in args:
            x += 1
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Sending gmsay message to world.')
        if x == 1:
            self.telnet.write(b'gmsay ' + args[0].encode('ascii') + b'\n')
            embed.add_field(name='Telnet:',value=self.telnet.read_until(b'> ')
                    .decode('ascii'), inline=False)
        else:
            embed.add_field(name='Telnet:',value='Invalid number of inputs!')
        await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='list',
            brief='Display Riot Test Server commands.',
                    description='Display Riot Test Server commands.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def list(self, ctx):
        self.telnet.write(b'help\n')
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Displaying Riot Test Server commands.')
        embed.add_field(name='Telnet:',value=self.telnet.read_until(b'> ')
                .decode('ascii'), inline=False)
        await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='lock', brief='Lock Riot Test Server.',
            description='Lock Riot Test Server.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def lock(self, ctx):
        self.telnet.write(b'lock\n')
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Locking Riot Test Server.')
        embed.add_field(name='Telnet:',value=self.telnet.read_until(b'> ')
                .decode('ascii'), inline=False)
        await ctx.send(embed=embed)

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
        embed = discord.Embed(colour=discord.Colour(0x7ed321), title='Setting:')
        if arg1 == 'ip':
            self.ip = arg2
            embed.add_field(name='IP:', value=self.ip, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'port':
            self.port = arg2
            embed.add_field(name='Port:', value=self.port, inline=False)
            await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='shutdown', brief='Shutdown Riot Test Server bot.',
            description='Shutdown Riot Test Server bot.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def shutdown(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Shutting down Riot Test Server bot!')
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
    @commands.command(name='tell', brief='Send player a tell.',
            description='Send player a tell.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def tell(self, ctx, *args):
        x = 0
        for num in args:
            x += 1
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Sending player a tell.')
        if x == 2:
            self.telnet.write(b'tell ' + args[0].encode('ascii') + b' '
                    + args[1].encode('ascii') + b'\n')
            embed.add_field(name='Telnet:',value=self.telnet.read_until(b'> ')
                    .decode('ascii'), inline=False)
        else:
            embed.add_field(name='Telnet:',value='Invalid number of inputs!')
        await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='unlock', brief='Unlock test server.',
            description='Unlock test server.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def unlock(self, ctx):
        self.telnet.write(b'unlock\n')
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Unlocking test server.')
        embed.add_field(name='Telnet:',value=self.telnet.read_until(b'> ')
                .decode('ascii'), inline=False)
        await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='who',
            brief='Display players online.',
                    description='Display players online.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def who(self, ctx):
        self.telnet.write(b'who\n')
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Displaying players online.')
        embed.add_field(name='Telnet:',value=self.telnet.read_until(b'> ')
                .decode('ascii'), inline=False)
        await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='zonestatus',
            brief='Display Riot Test Server zone status.',
                    description='Display Riot Test Server zone status.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def zonestatus(self, ctx):
        self.telnet.write(b'zonestatus\n')
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Displaying Riot Test Server zone status.')
        embed.add_field(name='Telnet:',value=self.telnet.read_until(b'> ')
                .decode('ascii'), inline=False)
        await ctx.send(embed=embed)

###############################################################################
def setup(bot):
    bot.add_cog(Serverbot(bot))

