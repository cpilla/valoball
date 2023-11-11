from discord.ext import commands
import discord
from datetime import datetime, timedelta, timezone
import json

class Valoball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.regMessage = None
        bot.queueMessage = None
        bot.queue = []
        bot.ranks = {"Iron1": range(0, 29), "Iron2": range(30, 60), "Iron3": range(61, 99),
                     "Bronze1": range(100, 129), "Bronze2": range(130, 160), "Bronze3": range(161, 199),
                     "Silver1": range(200, 229), "Silver2": range(230, 260), "Silver3": range(261, 299),
                     "Gold1": range(300, 329), "Gold2": range(330, 360), "Gold3": range(361, 399),
                     "Plat1": range(400, 429), "Plat2": range(430, 460), "Plat3": range(461, 499),
                     "Diamond1": range(500, 529), "Diamond2": range(530, 560), "Diamond3": range(561, 599),
                     "Ascendant1": range(600, 629), "Ascendant2": range(630, 660), "Ascendant3": range(661, 699),
                     "Immortal1": range(700, 729), "Immortal2": range(730, 760), "Immortal3": range(761, 799),
                     "Radiant": range(800, 10000)}
        
    @commands.command()
    async def spawn(self, ctx):
        embed = discord.Embed(title = "Valoball Test Embed", color = 0xdaaa00)
        view = RegistrationMenu(self.bot)
        if self.bot.regMessage == None:
            messages = [message async for message in ctx.message.channel.history(limit=100) if datetime.today().replace(tzinfo=None) - message.created_at.replace(tzinfo=None) < timedelta(days=14)]
            try:
                await ctx.message.channel.delete_messages(messages)
            except:
                pass
            self.bot.regMessage = await ctx.send(embed=embed, view=view)

class RegistrationMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.bot = bot

    @discord.ui.button(label="Enter Queue", style=discord.ButtonStyle.green, custom_id="Enter Queue Button")
    async def enter_queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.name not in self.bot.queue:
            self.bot.queue.append(interaction.user.name)
            await interaction.response.send_message(f"You ({interaction.user.name}) have entered the queue for volleyball!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You ({interaction.user.name}) are already in the queue for volleyball!", ephemeral=True)
        
    @discord.ui.button(label="Exit Queue", style=discord.ButtonStyle.red, custom_id="Exit Queue Button")
    async def exit_queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.name not in self.bot.queue:
            await interaction.response.send_message(f"You ({interaction.user.name}) are not in the queue for volleyball!", ephemeral=True)
        else:
            self.bot.queue.remove(interaction.user.name)
            await interaction.response.send_message(f"You ({interaction.user.name}) have exited the queue for volleyball!", ephemeral=True)
    
    @discord.ui.button(label="View Queue", style=discord.ButtonStyle.blurple, custom_id="View Queue Button")
    async def view_queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        queue_string = ""
        leaderboard = json.load(open("leaderboard.json"))
        print(leaderboard)
        for player_name in self.bot.queue:
            print(player_name)
            for player in leaderboard:
                if player["name"] == player_name:
                    queue_string = queue_string + ":" + get_rank(self.bot.ranks, player) + ":" + "**" + player_name + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round(player["wins"] / max(1, (player["wins"] + player["losses"])), 2)) + "%\n"

        embed = discord.Embed(title="Valoball Queue", description=queue_string,colour=0x00f549)
        self.bot.queueMessage = await interaction.channel.send(embed=embed)
    
    @discord.ui.button(label="Generate Teams", style=discord.ButtonStyle.blurple, custom_id="Generate Teams Button")
    async def generate_teams_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.name not in self.bot.queue:
            self.bot.queue.append(interaction.user.name)
            await interaction.response.send_message(f"You ({interaction.user.name}) have entered the queue for volleyball!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You ({interaction.user.name}) are already in the queue for volleyball!", ephemeral=True)

def get_rank(ranks, player):
    print(ranks)
    print(player)
    ranges = list(ranks.values())
    ind = 0
    for range in ranges:
        if player["elo"] in range:
            return list(ranks.keys())[ind]
        ind = ind + 1

async def setup(bot):
    await bot.add_cog(Valoball(bot))