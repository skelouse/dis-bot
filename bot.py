## bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')



class CustomClient(discord.Client):
    guild = None

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for i in self.guilds:
            if i.name == "DS 2020 Cohort":
                self.guild = i

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content == '99':
            response = 'ayye'
            await message.channel.send(response)

client = CustomClient()
client.run(TOKEN)

