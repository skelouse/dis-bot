import os
import ast
import sys
import discord
from discord.utils import get
from dotenv import load_dotenv
from io import StringIO

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

        if message.content == '/help':
            await message.channel.send("'''(code here)'''  <-  Replace the ' with `")

        if message.content.startswith("```") and message.content.endswith("```"):
            botuser = False
            for i in message.author.roles:
                if i.name == "Bot User":
                    botuser = True
            if botuser:
                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()
                exec(message.content[3:-3])
                sys.stdout = old_stdout

                response = redirected_output.getvalue()
                if not response:
                    response = 'None'
                await message.channel.send(response)
            else:
                await message.channel.send("You are not allowed to use this bot, please request permission")

client = CustomClient()
client.run(TOKEN)

