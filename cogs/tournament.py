import discord
from discord.ext import commands
import json
import cogs.valoball as valoball

class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.teams = []
        self.remaining_players = bot.queue
    
    @commands.command()
    async def tournament(self, ctx):
        view = Tournament_Select_View(self.bot, self.remaining_players)
        print(self.remaining_players)
        self.bot.tournament_message = await ctx.channel.send("Menu!", view=view)

class Tournament_Select(discord.ui.Select):
    def __init__(self, bot, remaining_players):
        self.bot = bot
        self.remaining_players = remaining_players
        options = []
        for player in remaining_players:
            options.append(discord.SelectOption(label = player["name"], value = player["id"], emoji = "<:" + valoball.get_rank(self.bot.ranks, player) + ">"))
            #self.add_option(player["name"], player["id"], emoji = "<:" + valoball.get_rank(self.bot.ranks, player) + ">")
        super().__init__(placeholder="Select a team of 2-4 players",max_values=4,min_values=2, options=options)
    async def callback(self, interaction: discord.Interaction):
        print()
        print("TEAMS")
        print(self.bot.teams)
        team = []
        for player in self.values:
            team.append(get_player_by_id(int(player)))
            for option in self.options:
                if int(option.value) == int(player):
                    print("DOES THIS")
                    self.remaining_players.remove(get_player_by_id(int(player)))
        self.bot.teams.append(team)
        with open("teams.json", "r") as f:
            team_data = json.load(f)
        
        team_id = get_team_id(team)
        if team_data.get(team_id) == None: #If this team has never played a game together before
            team_data[team_id] = {"players": [p_id["id"] for p_id in team], "wins": 0, "losses": 0, "team_name": valoball.generate_team_name(team_id)} #Add them to the teams list and write it to the file
            with open('teams.json', 'w') as f:
                json.dump(team_data, f)
        
        teamsMessage = ""
        teamsMessage = teamsMessage + "**" + team_data[team_id]["team_name"] + ":** **Elo:** " + str(int(valoball.getTeamAverage(team))) + " | **Winrate:**" + str(round((team_data[team_id]["wins"] / max(1, (team_data[team_id]["wins"] + team_data[team_id]["losses"])) * 100), 2)) + "%\n"
        for player in team:
            teamsMessage = teamsMessage + "<:" + valoball.get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
        teamsMessage = teamsMessage + "\n"
        embed = discord.Embed(title=f"Team {len(self.bot.teams)}", description=teamsMessage,colour=0x00a2ed)
        self.bot.games_messages.append(await interaction.channel.send(embed=embed))
        await self.bot.tournament_message.delete()

        if len(self.remaining_players) < 4:
            team = []
            for player in self.remaining_players:
                team.append(player)
            self.bot.teams.append(team)
            with open("teams.json", "r") as f:
                team_data = json.load(f)
            
            team_id = get_team_id(team)
            if team_data.get(team_id) == None: #If this team has never played a game together before
                team_data[team_id] = {"players": [p_id["id"] for p_id in team], "wins": 0, "losses": 0, "team_name": valoball.generate_team_name(team_id)} #Add them to the teams list and write it to the file
                with open('teams.json', 'w') as f:
                    json.dump(team_data, f)
            
            teamsMessage = ""
            teamsMessage = teamsMessage + "**" + team_data[team_id]["team_name"] + ":** **Elo:** " + str(int(valoball.getTeamAverage(team))) + " | **Winrate:**" + str(round((team_data[team_id]["wins"] / max(1, (team_data[team_id]["wins"] + team_data[team_id]["losses"])) * 100), 2)) + "%\n"
            for player in team:
                teamsMessage = teamsMessage + "<:" + valoball.get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
            teamsMessage = teamsMessage + "\n"
            embed = discord.Embed(title=f"Team {len(self.bot.teams)}", description=teamsMessage,colour=0x00a2ed)
            self.bot.games_messages.append(await interaction.channel.send(embed=embed))
            await self.bot.tournament_message.delete()

        view = Tournament_Select_View(self.bot, self.remaining_players)
        self.bot.tournament_message = await interaction.channel.send("Menu!", view=view)
        await interaction.response.defer()

class Tournament_Select_View(discord.ui.View):
    def __init__(self, bot, remaining_players, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.add_item(Tournament_Select(bot, remaining_players))

def get_team_id(team):
    id_sum = 0
    for player in team:
        id_sum = id_sum + player["id"]
    return str(id_sum)

def get_player_by_id(id):
    print("GETS HERE")
    with open('leaderboard.json', 'r') as f:
        data = json.load(f)
    print(data)
    for player in data:
        if player["id"] == id:
            print("FOUND")
            return player 

async def setup(bot):
    await bot.add_cog(Tournament(bot))