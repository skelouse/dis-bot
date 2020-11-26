import os
import ast
import sys
import discord
from discord.utils import get
from dotenv import load_dotenv
from traceback import format_exc
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

        elif message.content == '/log':
            with open("./log.txt") as f:
                res = f.read()
            await message.channel.send(res)

        elif message.content.startswith("```") and message.content.endswith("```"):
            botuser = False
            for i in message.author.roles:
                if i.name == "Bot User":
                    botuser = True
            if botuser:
                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()
                with open('./log.txt', 'a') as f:
                    f.write(str(message.author)+' - ')
                    content = message.content[3:-3]
                    if content.startswith('python'):
                        content = content[6:].strip()
                    f.write(content)
                    f.write('\n')
                try:
                    exec(content)

                except Exception:
                    await message.channel.send(format_exc())
                    return

                sys.stdout = old_stdout

                response = redirected_output.getvalue()
                if not response:
                    response = 'None'
                await message.channel.send(response)
            else:
                await message.channel.send("You are not allowed to use this bot, please request permission")

client = CustomClient()
client.run(TOKEN)

