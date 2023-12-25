from typing import Optional
from discord.ext import commands
import discord
from datetime import datetime, timedelta, timezone
import json
from random import random

class Valoball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.teams = None
        bot.regMessage = None
        bot.queueMessage = None
        bot.TeamsMessage = None
        bot.TeamsMessageId = None
        bot.leaderboardMessage = None
        bot.leaderboardMessageId = None
        bot.queue = [{"id": 1, "name": "Tommy", "wins": 0, "losses": 0, "elo": 1561}, 
                      {"id": 2, "name": "Cam", "wins": 0, "losses": 0, "elo": 973}, 
                      {"id": 3, "name": "Manny", "wins": 0, "losses": 0, "elo": 916}, 
                      {"id": 4, "name": "Massy", "wins": 0, "losses": 0, "elo": 812}, 
                      {"id": 5, "name": "Isabelle", "wins": 0, "losses": 0, "elo": 787}, 
                      {"id": 6, "name": "Eddy", "wins": 0, "losses": 0, "elo": 723}, 
                      {"id": 7, "name": "Sohan", "wins": 0, "losses": 0, "elo": 482}, 
                      {"id": 8, "name": "JR", "wins": 0, "losses": 0, "elo": 463}, 
                      {"id": 9, "name": "Kyaw", "wins": 0, "losses": 0, "elo": 431}, 
                      {"id": 10, "name": "Isaiah", "wins": 0, "losses": 0, "elo": 256}, 
                      {"id": 11, "name": "Kev", "wins": 0, "losses": 0, "elo": 226}, 
                      {"id": 12, "name": "Chin", "wins": 0, "losses": 0, "elo": 203}, 
                      {"id": 13, "name": "Sam", "wins": 0, "losses": 0, "elo": 166}] # Hardcoded start for queue for testing duo/trio queue
        # bot.queue = [] # Comment for testing
        bot.duoTrioQueue = []
        bot.ranks = {"Iron1:1185388187074433074": range(0, 29), "Iron2:1185388187946856448": range(30, 60), "Iron3:1185388189138042990": range(61, 99),
                     "Bronze1:1185387900532170815": range(100, 129), "Bronze2:1185387901312315462": range(130, 160), "Bronze3:1185387902063095848": range(161, 199),
                     "Silver1:1185387919666577529": range(200, 229), "Silver2:1185387982967025835": range(230, 260), "Silver3:1185387984586022932": range(261, 299),
                     "Gold1:1185387905036857465": range(300, 329), "Gold2:1185388088671879289": range(330, 360), "Gold3:1185388089649152060": range(361, 399),
                     "Plat1:1185387911735148564": range(400, 429), "Plat2:1185388022238281749": range(430, 460), "Plat3:1185387916093050971": range(461, 499),
                     "Diamond1:1185387903212331059": range(500, 529), "Diamond2:1185388086339846254": range(530, 560), "Diamond3:1185388087300325417": range(561, 599),
                     "Ascendant1:1185387897705205910": range(600, 629), "Ascendant2:1185387898493747230": range(630, 660), "Ascendant:31185387899659759656": range(661, 699),
                     "Immortal1:1185388051661336627": range(700, 729), "Immortal2:1185387909008867400": range(730, 760), "Immortal3:1185388052588265502": range(761, 799),
                     "Radiant:1185388311334895646": range(800, 10000)}
        
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
        # Logic for adding new players to json if they are not already in it
        foundFlag = 0
        leaderboard = json.load(open("leaderboard.json"))
        # print(leaderboard)
        # print(leaderboard[-1]["id"] + 1)
        for player in leaderboard:    # For loop accessing whole array of dictionaries (player = dict)
            if interaction.user.id == player["id"]: # Player is already in leaderboard
                foundFlag = 1
                break
        if foundFlag == 0:                              # Player is not in leaderboard
            newPlayer = {"id": interaction.user.id, "name": interaction.user.name, "wins": 0, "losses": 0, "elo": 350}
            leaderboard.append(newPlayer)
            # print(leaderboard)
            updatedJSON = json.dumps(leaderboard)
            f = open("leaderboard.json", "w")
            f.write(updatedJSON)
            f.close()
        
        alreadyInQueueFlag = 0
        for player in self.bot.queue:
            if interaction.user.id == player["id"]:
                alreadyInQueueFlag = 1
                break
        if (alreadyInQueueFlag == 0):
            # Place player in queue
            leaderboard = json.load(open("leaderboard.json"))
            for player in leaderboard:
                if interaction.user.id == player["id"]:
                    playerToQueue = player
            self.bot.queue.append(playerToQueue)
            await interaction.response.send_message(f"You ({interaction.user.name}) have entered the queue for volleyball!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You ({interaction.user.name}) are already in the queue for volleyball!", ephemeral=True)

        # if interaction.user.name not in self.bot.queue:
        #     self.bot.queue.append(interaction.user.name)
        #     await interaction.response.send_message(f"You ({interaction.user.name}) have entered the queue for volleyball!", ephemeral=True)
        # else:
        #     await interaction.response.send_message(f"You ({interaction.user.name}) are already in the queue for volleyball!", ephemeral=True)

    @discord.ui.button(label="Duo/Trio Queue", style=discord.ButtonStyle.blurple, custom_id="Duo/Trio Queue Button")
    async def duo_trio_queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Duo/Trio Queue Button Pressed")
          
        if findDictInList(self.bot.queue, "id", interaction.user.id) == None: # If player is not in queue yet
            await interaction.response.send_message(f"Please join the queue for volleyball first before doing this!", ephemeral=True)
        else:   # If player is in queue
            # Add selector menu for their duo/trio

            await interaction.response.send_message("Please select who you want to queue with!", view=SelectorView(bot=self.bot, interaction=interaction))

        # await interaction.response.defer()
        
        
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
        # leaderboard = json.load(open("leaderboard.json"))
        # print(leaderboard)
        for player in self.bot.queue:
            # print(player)
            queue_string = queue_string + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round(player["wins"] / max(1, (player["wins"] + player["losses"])), 2)) + "%\n"

        embed = discord.Embed(title="Valoball Queue", description=queue_string,colour=0x00f549)
        self.bot.queueMessage = await interaction.channel.send(embed=embed)
        await interaction.response.defer()
    
    @discord.ui.button(label="Generate Teams", style=discord.ButtonStyle.blurple, custom_id="Generate Teams Button")
    async def generate_teams_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        # print(self.bot.duoTrioQueue)

        numTeams = len(self.bot.queue) // 3  # Prioritize 3-player teams
        totalElo = 0
        eloRange = 50
        for player in self.bot.queue:
            totalElo += player["elo"]
        avgElo = totalElo / len(self.bot.queue) # Average Elo of all players in queue
        
        # While average team elos aren't in range, increase range every 5-10 iterartions
        iterCounter = 0
        maxRange = eloRange + 1
        while(maxRange > eloRange): # Loop for each team generation
            minTeamElo = avgElo
            maxTeamElo = avgElo
            teams = [ [] for x in range(numTeams)]
            remainingPlayers = self.bot.queue.copy()
            teamsOf4 = len(self.bot.queue) % 3
            for team in range(numTeams):    # Loop for each team
                playersPerTeam = 3
                if (teamsOf4 > 0):  # Checking if the team needs 4 players or 3
                    playersPerTeam = 4
                    teamsOf4 = teamsOf4 - 1
                player = 0
                while (player < playersPerTeam):    # Loop for each player in the team
                    # print(player)
                    playerNum = int(random() * len(remainingPlayers))   # Choosing random number for index of remaining players
                    ### New Functionality for Duo and Trio Queue
                    # if (remainingPlayers[playerNum] in self.bot.duoTrioQueue):
                    queuePlayerFlag = 0
                    for queues in self.bot.duoTrioQueue:
                        # print(str(len(remainingPlayers)) + " : " + str(playerNum))
                        if (len(remainingPlayers) > 0):
                            if (findDictInList(queues, "id", remainingPlayers[playerNum]["id"]) != None):
                                # print("Hit new if statement\n")
                                queuePlayerFlag = 1
                                # print(len(queues))
                                if (playersPerTeam - player >= len(queues)):
                                    for playerInQueue in queues:
                                        indexToPop = remainingPlayers.index(playerInQueue)
                                        teams[team].append(remainingPlayers[indexToPop])
                                        # print(remainingPlayers[indexToPop])
                                        remainingPlayers.pop(indexToPop)
                                        player += 1
                    if (queuePlayerFlag == 0 and len(remainingPlayers) > 0):
                        teams[team].append(remainingPlayers[playerNum])  # Add random player to team
                        remainingPlayers.pop(playerNum) # Remove player from available players list
                        player += 1
                    # print(len(remainingPlayers))
                # teams.append(team)  # Add team to list of teams
                teamElo = getTeamAverage(teams[team])  # Get the average elo for the team
                if (teamElo < minTeamElo):  # Check for min
                    minTeamElo = teamElo
                if (teamElo > maxTeamElo):  # Check for max
                    maxTeamElo = teamElo
            maxRange = maxTeamElo - minTeamElo  # Get max range for checking
            iterCounter += 1
            if (iterCounter % 10 == 0): # Every ten iterations
                eloRange += 50  # Increase range by 50
            # print(iterCounter)
            # print(maxRange, maxTeamElo, minTeamElo, "\n")
        # print(teams)

        self.bot.teams = teams
            
        teamsMessage = ""
        teamNum = 0
        for team in teams:
            teamNum += 1
            teamsMessage = teamsMessage + "Team " + str(teamNum) + ": " + str(int(getTeamAverage(team))) + " Elo\n"
            for player in team:
                teamsMessage = teamsMessage + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round(player["wins"] / max(1, (player["wins"] + player["losses"])), 2)) + "%\n"
            teamsMessage = teamsMessage + "\n"
        embed = discord.Embed(title="Valoball Teams", description=teamsMessage,colour=0x00a2ed)
        
        if self.bot.TeamsMessage == None:
            self.bot.TeamsMessage = await interaction.channel.send(embed=embed)
            self.bot.TeamsMessageId = self.bot.TeamsMessage.id
            # print(self.bot.TeamsMessage.id)
            # print(teamsMessage)
        else:
            message = await interaction.channel.fetch_message(self.bot.TeamsMessageId)
            await message.delete()
            self.bot.TeamsMessage = await interaction.channel.send(embed=embed)
            self.bot.TeamsMessageId = self.bot.TeamsMessage.id
        await interaction.response.defer()

    @discord.ui.button(label="Report Score", style=discord.ButtonStyle.blurple, custom_id="Report Score Button")
    async def score_report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Testing new button")
        

        await interaction.response.defer()
    
    @discord.ui.button(label="Leaderboard", style=discord.ButtonStyle.blurple, custom_id="Leaderboard Button")
    async def leaderboard_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Testing new button")
        leaderboardMessage = ""

        # Loading players from json file
        with open("leaderboard.json", 'r') as file:
            all_players = json.load(file)

        # Sorting player list
        all_players = sorted(all_players, key = lambda x: x['elo'], reverse = True) # Reverse = True to put it in descending order

        # Crafting message embed
        for player in all_players:
            leaderboardMessage = leaderboardMessage + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round(player["wins"] / max(1, (player["wins"] + player["losses"])), 2)) + "%\n"
        leaderboardMessage = leaderboardMessage + "\n"
        embed = discord.Embed(title="Valoball Leaderboard", description=leaderboardMessage,colour=0xffc0cb)

        # Sending message embed
        if self.bot.leaderboardMessage == None: # Checking if a message has already been sent in this session
            self.bot.leaderboardMessage = await interaction.channel.send(embed=embed)
            self.bot.leaderboardMessageId = self.bot.leaderboardMessage.id
        else:
            message = await interaction.channel.fetch_message(self.bot.leaderboardMessageId)    # Fetching last sent leaderboard message embed
            await message.delete()  # Deleting last sent leaderboard message embed
            self.bot.leaderboardMessage = await interaction.channel.send(embed=embed)
            self.bot.leaderboardMessageId = self.bot.leaderboardMessage.id

        await interaction.response.defer()

class Selector(discord.ui.Select):
    def __init__(self, interaction: discord.Interaction, bot):
        self.bot = bot
        selectorOptions = []
        for player in bot.queue:
            if (player["id"] == interaction.user.id) or (player in bot.duoTrioQueue):
                # Don't add if player is the person selecting queues
                break
            else:
                playerOption = discord.SelectOption(label = player["name"], value = player["id"], description = player["elo"]) # description= str(player["elo"]))
            selectorOptions.append(playerOption)
        super().__init__(placeholder="Please choose up to two players to queue with!", min_values=1, max_values=2, options=selectorOptions)

    async def callback(self, interaction: discord.Interaction):
        queue = []
        for player in self.values:
            queue.append(findDictInList(self.bot.queue, "id", int(player)))
        queue.append(findDictInList(self.bot.queue, "id", interaction.user.id))

        valoballInstance = self.bot.get_cog("Valoball")
        valoballInstance.bot.duoTrioQueue.append(queue)

        await interaction.response.defer()  

class SelectorView(discord.ui.View):
    def __init__(self, bot, interaction: discord.Interaction, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.add_item(Selector(bot=bot, interaction=interaction))

def findDictInList(lst, key, value):
    for item in lst:
        if key in item and item[key] == value:
            return item
    return None

def getTeamAverage(team):
    totalElo = 0
    for player in team:
        totalElo += player["elo"]
    return(totalElo / len(team))

def get_rank(ranks, player):
    # print(ranks)
    # print(player)
    ranges = list(ranks.values())
    ind = 0
    for range in ranges:
        if player["elo"] in range:
            return list(ranks.keys())[ind]
        ind = ind + 1

async def setup(bot):
    await bot.add_cog(Valoball(bot))