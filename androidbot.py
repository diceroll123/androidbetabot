import asyncio
import datetime

import aiohttp
import discord
from discord.ext.commands import Bot

import config


class AndroidPreviewBot(Bot):

    def __init__(self):
        super().__init__(command_prefix='!', status=discord.Status.dnd,
                         activity=discord.Activity(type=discord.ActivityType.watching, name='android.com/beta'))
        self.current_url = None

    async def on_ready(self):
        print('Logged in as', self.user.name)
        print('------')
        await self.check_beta_page()

    async def on_message(self, message):
        if message.channel.id != config.ANDROID_CHANNEL_ID:
            return
        if message.author.id != config.MY_USER_ID:
            return
        await message.channel.send('Shutting down! See you next year. \N{WINKING FACE}')
        await self.close()

    async def check_beta_page(self):
        await self.wait_until_ready()
        android_channel = self.get_channel(config.ANDROID_CHANNEL_ID)
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.head('https://developer.android.com/preview/devices', allow_redirects=False) as resp:
                    location = resp.headers.get('Location')
                    if not self.current_url:
                        self.current_url = location

                    if location != self.current_url:
                        await self.change_presence(
                            activity=discord.Activity(type=discord.ActivityType.playing,
                                                      name=f'with Android beta!'),
                            status=discord.Status.online)
                        print(datetime.datetime.now(), '- YES!')
                        break
                    else:
                        print(datetime.datetime.now(), '- nope')
            await asyncio.sleep(15)

        while True:
            await android_channel.send(f'<@{config.MY_USER_ID}> - {location}')
            await asyncio.sleep(1)


AndroidPreviewBot().run(config.TOKEN)
