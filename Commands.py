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
from random import *
import asyncio
import discord

class Commands:
###############################################################################
    def __init__(self, bot):
        self.bot = bot
        self.tracking_task = self.bot.loop.create_task(self.track())
        self.tracking_task.cancel()
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
    @commands.command(name="attack", description="Attack a monster.")
    @commands.cooldown(1, 2, commands.BucketType.channel)
    async def attack(self, ctx):
        "Attack a monster."
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
    @commands.command(name="batphone", description="Trigger voice batphone.")
    @commands.cooldown(1, 30, commands.BucketType.channel)
    async def batphone(self, ctx):
        "Trigger voice batphone."
        mp3 = MP3(self.audio_file)
        voice = self.bot.get_channel(int(self.voice))
        player = await voice.connect()
        player.play(discord.FFmpegPCMAudio(self.audio_file))
        await asyncio.sleep(mp3.info.length + 1)
        await player.disconnect()

###############################################################################
    @commands.command(name="charinfo", description="Display character info.")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def charinfo(self, ctx):
        "Display character info."
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
    def get_cfg(self, arg):
        with closing(open('PyConnect.ini', 'r')) as file:
            buffer = file.read(None).splitlines()
            value = buffer.pop(buffer.index(arg) + 1)
            return value

###############################################################################
    @commands.command(name="reload", description="Reload config variables.")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def reload(self, ctx):
        "Reload config variables."
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
    @commands.command(name="register",
            description="Register account for rpgbot.")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def register(self, ctx):
        "Register account for rpgbot."
        author_id = ctx.message.author.id
        self.level[author_id] = 1
        self.xp[author_id] = 0
        await ctx.send('User ID is now registered!')
        await ctx.send('Use !charinfo for character stats!')

###############################################################################
    @commands.command(name="roll", description="Roll magical dice.")
    @commands.cooldown(10, 30, commands.BucketType.channel)
    async def roll(self, ctx, *args):
        "Roll magical dice."
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
    @commands.command(name="set", description="Set config variable.")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def set(self, ctx, arg1, arg2):
        "Set config variable."
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
    @commands.command(name="shutdown", description="Shutdown bot.")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def shutdown(self, ctx):
        "Shutdown bot."
        await ctx.send('Shutting down!')
        await self.bot.close()

###############################################################################
    @commands.command(name="start", description="Start tracking loop.")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def start(self, ctx):
        "Start tracking loop."
        if self.tracking_task.done():
            self.tracking_task = self.bot.loop.create_task(self.track())
            await ctx.send("Tracking loop started!")
        else:
            await ctx.send("Tracking loop is already running!")

###############################################################################
    @commands.command(name="status", description="Display bot status.")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def status(self, ctx):
        "Display bot status."
        await ctx.send('(T)echnology for (P)repared (A)egis (R)aiding')
        await ctx.send('Parsing file: {}'.format(self.parse))
        await ctx.send('Playing audio file: {}'.format(self.audio_file))
        await ctx.send('Batphoning role_id:channel_id::voice_id: {}:{}:{}.'
                .format(self.role, self.channel, self.voice))
        await ctx.send('Tracking: {}, {}, {}, {}, and {}'
                .format(self.target1, self.target2, self.target3,
                        self.target4, self.target5))
        await ctx.send('OK!')

###############################################################################
    @commands.command(name="stop", description="Stop tracking loop.")
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def stop(self, ctx):
        "Stop tracking loop."
        if not self.tracking_task.done():
            self.tracking_task.cancel()
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
    bot.add_cog(Commands(bot))
