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
        self.trackingbot_task = self.bot.loop.create_task(self.track())
        self.trackingbot_task.cancel()
        self.audio_file = self.get_cfg('[AUDIO_FILE]')
        self.channel = self.get_cfg('[CHANNEL]')
        self.count_limit = self.get_cfg('[COUNT_LIMIT]')
        self.parse   = self.get_cfg('[PARSE]')
        self.role    = self.get_cfg('[ROLE]')
        self.target1  = self.get_cfg('[TARGET1]')
        self.target2  = self.get_cfg('[TARGET2]')
        self.target3  = self.get_cfg('[TARGET3]')
        self.target4  = self.get_cfg('[TARGET4]')
        self.target5  = self.get_cfg('[TARGET5]')
        self.voice = self.get_cfg('[VOICE]')
        self.count = 0
        self.fte = ''

###############################################################################
    @commands.command(name='batphone', brief='Trigger voice batphone.',
            description='Trigger voice batphone.')
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def batphone(self, ctx):
        mp3 = MP3(self.audio_file)
        voice = self.bot.get_channel(int(self.voice))
        player = await voice.connect()
        player.play(discord.FFmpegPCMAudio(self.audio_file))
        await asyncio.sleep(mp3.info.length + 1)
        await player.disconnect()

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
        await ctx.send('Reloading config variables...')
        self.audio_file = self.get_cfg('[AUDIO_FILE]')
        self.channel = self.get_cfg('[CHANNEL]')
        self.count_limit = self.get_cfg('[COUNT_LIMIT]')
        self.parse   = self.get_cfg('[PARSE]')
        self.role    = self.get_cfg('[ROLE]')
        self.target1  = self.get_cfg('[TARGET1]')
        self.target2  = self.get_cfg('[TARGET2]')
        self.target3  = self.get_cfg('[TARGET3]')
        self.target2  = self.get_cfg('[TARGET4]')
        self.target3  = self.get_cfg('[TARGET5]')
        await ctx.send('OK!')

###############################################################################
    @commands.command(name='set', brief='Set config variable.',
            description='Set config variable.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def set(self, ctx, arg1, arg2):
        if arg1 == 'audio_file':
            self.channel = arg2
            await ctx.send('Set audio file to: {}'.format(self.audio_file))
        if arg1 == 'channel':
            self.channel = arg2
            await ctx.send('Set channel to: {}'.format(self.channel))
        if arg1 == 'count':
            self.count = arg2
            await ctx.send('Batphone count set to: {}'.format(self.count))
        if arg1 == 'parse':
            self.parse = arg2
            await ctx.send('Set parse file to: {}'.format(self.parse))
        if arg1 == 'role':
            self.role = arg2
            await ctx.send('Set batphone role to: {}'.format(self.role))
        if arg1 == 'target1':
            self.target1 = arg2
            await ctx.send('Set target1 to: {}'.format(self.target1))
        if arg1 == 'target2':
            self.target2 = arg2
            await ctx.send('Set target2 to: {}'.format(self.target2))
        if arg1 == 'target3':
            self.target3 = arg2
            await ctx.send('Set target3 to: {}'.format(self.target3))
        if arg1 == 'target4':
            self.target4 = arg2
            await ctx.send('Set target4 to: {}'.format(self.target4))
        if arg1 == 'target5':
            self.target5 = arg2
            await ctx.send('Set target5 to: {}'.format(self.target5))
        await ctx.send('OK!')

###############################################################################
    @commands.command(name='shutdown', brief='Shutdown bot.',
            description='Shutdown bot.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def shutdown(self, ctx):
        await ctx.send('Shutting down!')
        await self.bot.close()

###############################################################################
    @commands.command(name='start', brief='Start Tracking loop.',
            description='Start Trackingbot loop.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def start(self, ctx):
        if self.trackingbot_task.done():
            self.trackingbot_task = self.bot.loop.create_task(self.track())
            await ctx.send("Tracking loop started!")
        else:
            await ctx.send("Tracking loop is already running!")

###############################################################################
    @commands.command(name='status', brief='Display bot status.',
            description='Display bot status.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def status(self, ctx):
        await ctx.send('(T)echnology for (P)repared (A)egis (R)aiding')
        await ctx.send('Parsing file: {}'.format(self.parse))
        await ctx.send('Playing audio file: {}'.format(self.audio_file))
        await ctx.send('Batphoning role_id:channel_id::voice_id: {}:{}:{}.'
                .format(self.role, self.channel, self.voice))
        await ctx.send('Trackingbot: {}, {}, {}, {}, and {}'
                .format(self.target1, self.target2, self.target3,
                        self.target4, self.target5))
        await ctx.send('OK!')

###############################################################################
    @commands.command(name='stop', brief='Stop Tracking loop.',
            description='Stop Trackingbot loop.')
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def stop(self, ctx):
        if not self.trackingbot_task.done():
            self.trackingbot_task.cancel()
            await ctx.send('Tracking loop stopped!')
        else:
            await ctx.send('Tracking loop is not currently running!')

###############################################################################
    async def track(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            channel = self.bot.get_channel(int(self.channel))
            voice = self.bot.get_channel(int(self.voice))
            for line in Pygtail(self.parse):
                target_list = [self.target1 in line, self.target2 in line,
                        self.target3 in line, self.target4 in line,
                                self.target5 in line]
                if any(target_list):
                    self.count = self.count + 1
                    self.fte = line
                    if (self.count <= int(self.count_limit)): 
                        print('Target found! Activating bat signal!')
                        await channel.send('<@&{}> -> {}'
                                .format(self.role, self.fte))
                        mp3 = MP3(self.audio_file)
                        player = await voice.connect()
                        player.play(discord.FFmpegPCMAudio(self.audio_file))
                        await asyncio.sleep(mp3.info.length + 1)
                        await player.disconnect()
            await asyncio.sleep(5)

###############################################################################
def setup(bot):
    bot.add_cog(Trackingbot(bot))
