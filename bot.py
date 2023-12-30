import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import discord.ui

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='>>', intents=discord.Intents.all())
        self.initial_extensions = ["cogs.utils", "cogs.valoball"]
        self.spawn_message = None
    async def setup_hook(self):
        print(f"Logging in as: {self.user}")
        for ext in self.initial_extensions:
            await self.load_extension(ext)
        print(self.cogs)
        synced = await bot.tree.sync()
        print(f"Commands: \n {synced}")

bot = MyBot()

#Bot commands work like this. You declare them like this and the name of the command will be the name of the command with the prefix.
@bot.tree.command(name="test")
#This line is for parameters for a command
@app_commands.describe(to_say = "What should be said", number = "Some number")
async def test(interaction: discord.Interaction, to_say: str, number: int):
    await interaction.response.send_message(f"{to_say} + {number}")

load_dotenv()
# botKey = os.getenv("KEY")
# print(botKey)
# bot.run(botKey)
bot.run("MTE3MDg4MTI1MjgzNzA0ODUxMw.GjCHKu.BmDPuCcYqtgWhOD-RZbx37-bzjI6AI88k7jhXI")