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
from mutagen.mp3 import MP3
from pygtail import Pygtail
import asyncio
import discord
import json
import string
import re

class Trackingbot(commands.Cog):
###############################################################################
    def __init__(self, bot):
        self.bot = bot
        self.line = ''
        self.trackingbot_task = False
        self.voice_connected = False
        self.version = '1.05'
        with open('PyConnect.json') as config_file:
            self.config = json.load(config_file)
            self.channel_id = self.config['id']['channel']
            self.parse = self.config['file']['parse']
            self.role_id  = self.config['id']['role']
            self.sound0 = self.config['sound']['0']
            self.sound1  = self.config['sound']['1']
            self.sound2  = self.config['sound']['2']
            self.sound3  = self.config['sound']['3']
            self.sound4  = self.config['sound']['4']
            self.sound5  = self.config['sound']['5']
            self.target1  = self.config['target']['1']
            self.target2  = self.config['target']['2']
            self.target3  = self.config['target']['3']
            self.target4  = self.config['target']['4']
            self.target5  = self.config['target']['5']
            self.voice_id = self.config['id']['voice']

###############################################################################
    @commands.command(name='batphone', brief='Trigger voice batphone.',
            description='Trigger voice batphone.')
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def batphone(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Activating voice batphone!')
        await ctx.send(embed=embed)
        print('Activating voice bat phone!')
        mp3 = MP3(self.sound0)
        voice = self.bot.get_channel(int(self.voice_id))
        if self.voice_connected is False:
            self.player = await voice.connect()
        self.player.play(discord.FFmpegPCMAudio(self.sound0))
        await asyncio.sleep(mp3.info.length + 1)

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
            self.audio = self.config['file']['audio']
            self.channel_id = self.config['id']['channel']
            self.parse = self.config['file']['parse']
            self.role_id  = self.config['id']['role']
            self.sound0 = self.config['sound']['0']
            self.sound1  = self.config['sound']['1']
            self.sound2  = self.config['sound']['2']
            self.sound3  = self.config['sound']['3']
            self.sound4  = self.config['sound']['4']
            self.sound5  = self.config['sound']['5']
            self.target1  = self.config['target']['1']
            self.target2  = self.config['target']['2']
            self.target3  = self.config['target']['3']
            self.target4  = self.config['target']['4']
            self.target5  = self.config['target']['5']
            self.voice_id = self.config['id']['voice']

###############################################################################
    @commands.command(name='set', brief='Set config variable.',
            description='Set config variable.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def set(self, ctx, arg1, arg2):
        embed = discord.Embed(colour=discord.Colour(0x7ed321), title='Set:')
        if arg1 == 'audio_file':
            self.audio = arg2
            embed.add_field(name='Audio File:', value=self.audio, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'channel':
            self.channel_id = arg2
            embed.add_field(name='Channel ID:', value=self.channel_id,
                    inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'parse':
            self.parse = arg2
            embed.add_field(name='Log File:', value=self.parse, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'role':
            self.role_id = arg2
            embed.add_field(name='Role ID:', value=self.role_id, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'target1':
            self.target1 = arg2
            embed.add_field(name='Target 1:', value=self.target1, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'target2':
            self.target2 = arg2
            embed.add_field(name='Target 2:', value=self.target2, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'target3':
            self.target3 = arg2
            embed.add_field(name='Target 3:', value=self.target3, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'target4':
            self.target4 = arg2
            embed.add_field(name='Target 4:', value=self.target4, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'target5':
            self.target5 = arg2
            embed.add_field(name='Target 5:', value=self.target5, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'voice':
            self.voice_id = arg2
            embed.add_field(name='Voice ID:', value=self.voice_id, inline=False)
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
    @commands.command(name='snooze', brief='Snooze voice batphone.',
            description='Snooze voice batphone.')
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def snooze(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Snoozing voice batphone!')
        await ctx.send(embed=embed)
        print('Snoozing voice bat phone!')
        for voice in self.bot.voice_clients:
            if(voice.guild == ctx.guild):
                await voice.disconnect()
                self.voice_connected = False

###############################################################################
    @commands.command(name='start', brief='Start Tracking loop.',
            description='Start Trackingbot loop.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def start(self, ctx):
        if self.trackingbot_task is False:
            self.trackingbot_task = self.bot.loop.create_task(self.track())
            embed = discord.Embed(colour=discord.Colour(0x7ed321),
                    title='Tracking loop started!')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour(0x7ed321),
                    title='Tracking loop is already running!')
            await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='status', brief='Display bot status.',
            description='Display bot status.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def status(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Riot Tracking Bot:\nVersion {}.'.format(self.version))
        embed.add_field(name='Audio File:', value=self.audio, inline=False)
        embed.add_field(name='Channel ID:', value=self.channel_id, inline=False)
        embed.add_field(name='Parse File:', value=self.parse, inline=False)
        embed.add_field(name='Role ID:', value=self.role_id, inline=False)
        embed.add_field(name='Sound 0:', value=self.sound0, inline=False)
        embed.add_field(name='Sound 1:', value=self.sound1, inline=False)
        embed.add_field(name='Sound 2:', value=self.sound2, inline=False)
        embed.add_field(name='Sound 3:', value=self.sound3, inline=False)
        embed.add_field(name='Sound 4:', value=self.sound4, inline=False)
        embed.add_field(name='Sound 5:', value=self.sound5, inline=False)
        embed.add_field(name='Target 1:', value=self.target1, inline=False)
        embed.add_field(name='Target 2:', value=self.target2, inline=False)
        embed.add_field(name='Target 3:', value=self.target3, inline=False)
        embed.add_field(name='Target 4:', value=self.target4, inline=False)
        embed.add_field(name='Target 5:', value=self.target5, inline=False)
        embed.add_field(name='Voice ID', value=self.voice_id, inline=False)
        await ctx.send(embed=embed)

###############################################################################
    @commands.command(name='stop', brief='Stop Tracking loop.',
            description='Stop Trackingbot loop.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def stop(self, ctx):
        if self.trackingbot_task is not False:
            self.trackingbot_task.cancel()
            self.trackingbot_task = False
            embed = discord.Embed(colour=discord.Colour(0x7ed321),
                    title='Tracking loop stopped!')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=discord.Colour(0x7ed321),
                    title='Tracking loop is not currently running!')
            await ctx.send(embed=embed)

###############################################################################
    async def track(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            channel = self.bot.get_channel(int(self.channel_id))
            voice = self.bot.get_channel(int(self.voice_id))
            if self.voice_connected is False:
                self.player = await voice.connect()
                self.voice_connected = True
            for line in Pygtail(self.parse, paranoid=True, copytruncate=False):
                if self.target1 in line:
                    self.line = re.sub(r'\[.*?\]', '', line)
                    await channel.send('{}'.format(self.line))
                    mp3 = MP3(self.sound1)
                    self.player.play(discord.FFmpegPCMAudio(self.sound1))
                    await asyncio.sleep(mp3.info.length + 1)
                if self.target2 in line:
                    self.line = re.sub(r'\[.*?\]', '', line)
                    await channel.send('{}'.format(self.line))
                    mp3 = MP3(self.sound2)
                    self.player.play(discord.FFmpegPCMAudio(self.sound2))
                    await asyncio.sleep(mp3.info.length + 1)
                if self.target3 in line:
                    self.line = re.sub(r'\[.*?\]', '', line)
                    await channel.send('{}'.format(self.line))
                    mp3 = MP3(self.sound3)
                    self.player.play(discord.FFmpegPCMAudio(self.sound3))
                    await asyncio.sleep(mp3.info.length + 1)
                if self.target4 in line:
                    self.line = re.sub(r'\[.*?\]', '', line)
                    await channel.send('{}'.format(self.line))
                    mp3 = MP3(self.sound4)
                    self.player.play(discord.FFmpegPCMAudio(self.sound4))
                    await asyncio.sleep(mp3.info.length + 1)
                if self.target5 in line:
                    self.line = re.sub(r'\[.*?\]', '', line)
                    await channel.send('{}'.format(self.line))
                    mp3 = MP3(self.sound5)
                    self.player.play(discord.FFmpegPCMAudio(self.sound5))
                    await asyncio.sleep(mp3.info.length + 1)
            await asyncio.sleep(2)

###############################################################################
def setup(bot):
    bot.add_cog(Trackingbot(bot))

