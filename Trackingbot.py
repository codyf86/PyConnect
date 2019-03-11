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

class Trackingbot:
###############################################################################
    def __init__(self, bot):
        self.bot = bot
        self.count = 0
        self.fte = ''
        self.trackingbot_task = False
        self.version = '1.01'
        self.audio_file = self.get_cfg('[AUDIO_FILE]')
        self.channel = self.get_cfg('[CHANNEL]')
        self.count_limit = self.get_cfg('[COUNT_LIMIT]')
        self.embed = self.get_cfg('[EMBED]')
        self.parse = self.get_cfg('[PARSE]')
        self.role  = self.get_cfg('[ROLE]')
        self.safety  = self.get_cfg('[SAFETY]')
        self.target1  = self.get_cfg('[TARGET1]')
        self.target2  = self.get_cfg('[TARGET2]')
        self.target3  = self.get_cfg('[TARGET3]')
        self.target4  = self.get_cfg('[TARGET4]')
        self.target5  = self.get_cfg('[TARGET5]')
        self.voice = self.get_cfg('[VOICE]')

###############################################################################
    @commands.command(name='batphone', brief='Trigger voice batphone.',
            description='Trigger voice batphone.')
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def batphone(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Activating voice batphone!')
        print('Activating voice bat phone!')
        await ctx.send(embed=embed)
        mp3 = MP3(self.audio_file)
        voice = self.bot.get_channel(int(self.voice))
        player = await voice.connect()
        player.play(discord.FFmpegPCMAudio(self.audio_file))
        await asyncio.sleep(mp3.info.length + 1)
        await player.disconnect()

###############################################################################
    @commands.command(name='embed', brief='Embed the contents of a file.',
            description='Embed the contents of a file.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def embed(self, ctx):
        var = self.get_cfg('[EMBED]')
        with closing(open(var, 'r')) as file:
            buffer = file.read(None).splitlines()
            embed = discord.Embed(colour=discord.Colour(0x7ed321),
                    title='Embed:')
            embed.add_field(name=var, value=buffer, inline=False)
            await ctx.send(embed=embed)

###############################################################################
    def get_cfg(self, arg):
        with closing(open('PyConnect.ini', 'r')) as file:
            buffer = file.read(None).splitlines()
            value = buffer.pop(buffer.index(arg) + 1)
            return value

###############################################################################
    @commands.command(name='reload', brief='Reload config variables.',
            description='Reload config variables.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def reload(self, ctx):
        embed = discord.Embed(colour=discord.Colour(0x7ed321),
                title='Reloading config variables.')
        await ctx.send(embed=embed)
        self.audio_file = self.get_cfg('[AUDIO_FILE]')
        self.channel = self.get_cfg('[CHANNEL]')
        self.count_limit = self.get_cfg('[COUNT_LIMIT]')
        self.embed = self.get_cfg('[EMBED]')
        self.parse = self.get_cfg('[PARSE]')
        self.role  = self.get_cfg('[ROLE]')
        self.safety  = self.get_cfg('[SAFETY]')
        self.target1  = self.get_cfg('[TARGET1]')
        self.target2  = self.get_cfg('[TARGET2]')
        self.target3  = self.get_cfg('[TARGET3]')
        self.target4  = self.get_cfg('[TARGET4]')
        self.target5  = self.get_cfg('[TARGET5]')
        self.voice = self.get_cfg('[VOICE]')

###############################################################################
    @commands.command(name='set', brief='Set config variable.',
            description='Set config variable.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def set(self, ctx, arg1, arg2):
        embed = discord.Embed(colour=discord.Colour(0x7ed321), title='Set:')
        if arg1 == 'audio_file':
            self.channel = arg2
            embed.add_field(name='Audio File:', value=self.audio_file,
                    inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'channel':
            self.channel = arg2
            embed.add_field(name='Channel ID:', value=self.channel,
                    inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'count':
            self.count = arg2
            embed.add_field(name='Count:', value=self.count, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'count_limit':
            self.count_limit = arg2
            embed.add_field(name='Count Limit:', value=self.count_limit,
                    inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'embed':
            self.embed = arg2
            embed.add_field(name='Embed File:', value=self.embed, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'parse':
            self.parse = arg2
            embed.add_field(name='Log File:', value=self.parse, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'role':
            self.role = arg2
            embed.add_field(name='Role ID:', value=self.role, inline=False)
            await ctx.send(embed=embed)
        if arg1 == 'safety':
            if arg2 == 'true':
                self.safety = True
            elif arg2 == 'false':
                self.safety = False
            else:
                await ctx.send('Invalid value input.')
            embed.add_field(name='Safety:', value=self.safety, inline=False)
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
            self.voice = arg2
            embed.add_field(name='Voice ID:', value=self.voice, inline=False)
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
                title='(T)echnology for (P)repared (A)egis (R)aiding'
                        '\nVersion {}.'.format(self.version))
        embed.add_field(name='Safety Trigger:', value=self.safety, inline=False)
        embed.add_field(name='Count:', value=self.count, inline=False)
        embed.add_field(name='Count Limit:', value=self.count_limit,
                inline=False)
        embed.add_field(name='Embed File:', value=self.embed, inline=False)
        embed.add_field(name='Parsing File:', value=self.parse, inline=False)
        embed.add_field(name='Audio File:', value=self.audio_file, inline=False)
        embed.add_field(name='Channel ID:', value=self.channel, inline=False)
        embed.add_field(name='Role ID:', value=self.role, inline=False)
        embed.add_field(name='Voice ID', value=self.voice, inline=False)
        embed.add_field(name='Target 1:', value=self.target1, inline=False)
        embed.add_field(name='Target 2:', value=self.target2, inline=False)
        embed.add_field(name='Target 3:', value=self.target3, inline=False)
        embed.add_field(name='Target 4:', value=self.target4, inline=False)
        embed.add_field(name='Target 5:', value=self.target5, inline=False)
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
            channel = self.bot.get_channel(int(self.channel))
            for line in Pygtail(self.parse, paranoid=True, copytruncate=False):
                target_list = [self.target1 in line, self.target2 in line,
                        self.target3 in line, self.target4 in line,
                                self.target5 in line]
                if any(target_list):
                    self.count += 1
                    self.fte = line
                    print('Target found! Activating bat phone!')
                    if (self.count <= int(self.count_limit)
                            and self.safety is not True): 
                        await channel.send('<@&{}> -> {}'
                                .format(self.role, self.fte))
            await asyncio.sleep(5)

###############################################################################
def setup(bot):
    bot.add_cog(Trackingbot(bot))

