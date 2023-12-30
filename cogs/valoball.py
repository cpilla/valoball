from typing import Optional
from discord.ext import commands
import discord
from datetime import datetime, timedelta, timezone
import json
from random import random
import asyncio
from discord import ui
from discord.interactions import Interaction

class Valoball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.spawn_message = None
        bot.teams = None
        bot.queueMessage = None
        bot.TeamsMessage = None
        bot.TeamsMessageId = None
        bot.leaderboardMessage = None
        bot.leaderboardMessageId = None
        bot.games_messages = []
        bot.games_embeds = []
        bot.matchups = []
        '''
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
        '''
        with open("leaderboard.json", "r") as f:
            bot.queue = json.load(f)
        # bot.queue = [] # Comment for testing
        bot.duoTrioQueue = []
        bot.ranks = {"Iron1:1185388187074433074": range(0, 29), "Iron2:1185388187946856448": range(30, 60), "Iron3:1185388189138042990": range(61, 99),
                     "Bronze1:1185387900532170815": range(100, 129), "Bronze2:1185387901312315462": range(130, 160), "Bronze3:1185387902063095848": range(161, 199),
                     "Silver1:1185387919666577529": range(200, 229), "Silver2:1185387982967025835": range(230, 260), "Silver3:1185387984586022932": range(261, 299),
                     "Gold1:1185387905036857465": range(300, 329), "Gold2:1185388088671879289": range(330, 360), "Gold3:1185388089649152060": range(361, 399),
                     "Plat1:1185387911735148564": range(400, 429), "Plat2:1185388022238281749": range(430, 460), "Plat3:1185387916093050971": range(461, 499),
                     "Diamond1:1185387903212331059": range(500, 529), "Diamond2:1185388086339846254": range(530, 560), "Diamond3:1185388087300325417": range(561, 599),
                     "Ascendant1:1185387897705205910": range(600, 629), "Ascendant2:1185387898493747230": range(630, 660), "Ascendant3:1185387899659759656": range(661, 699),
                     "Immortal1:1185388051661336627": range(700, 729), "Immortal2:1185387909008867400": range(730, 760), "Immortal3:1185388052588265502": range(761, 799),
                     "Radiant:1185388311334895646": range(800, 10000)}
        bot.game_scores = []
        
    async def after_ready(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(993243011326673010)
        embed = discord.Embed(title = "Valoball Test Embed", color = 0xdaaa00)
        view = RegistrationMenu(self.bot)
        if self.bot.spawn_message == None:
            messages = [message async for message in channel.history(limit=100) if datetime.today().replace(tzinfo=None) - message.created_at.replace(tzinfo=None) < timedelta(days=14)]
            try:
                await channel.delete_messages(messages)
            except:
                pass
            self.bot.spawn_message = await channel.send(embed=embed, view=view)

    async def cog_load(self):
        asyncio.create_task(self.after_ready())


    @commands.command()
    async def spawn(self, ctx):
        embed = discord.Embed(title = "Valoball Test Embed", color = 0xdaaa00)
        view = RegistrationMenu(self.bot)
        if self.bot.spawn_message == None:
            messages = [message async for message in ctx.message.channel.history(limit=100) if datetime.today().replace(tzinfo=None) - message.created_at.replace(tzinfo=None) < timedelta(days=14)]
            try:
                await ctx.message.channel.delete_messages(messages)
            except:
                pass
            self.bot.spawn_message = await ctx.send(embed=embed, view=view)

class RegistrationMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout = None)
        self.bot = bot

    @discord.ui.button(label="Enter Queue", style=discord.ButtonStyle.green, custom_id="Enter Queue Button")
    async def enter_queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Logic for adding new players to json if they are not already in it
        foundFlag = 0
        with open("leaderboard.json", "r") as f:
            leaderboard = json.load(f)
        # print(leaderboard)
        # print(leaderboard[-1]["id"] + 1)
        for player in leaderboard:    # For loop accessing whole array of dictionaries (player = dict)
            if interaction.user.id == player["id"]: # Player is already in leaderboard
                foundFlag = 1
                break
        if foundFlag == 0:                              # Player is not in leaderboard
            newPlayer = {"id": interaction.user.id, "name": interaction.user.name, "wins": 0, "losses": 0, "elo": 350}
            leaderboard.append(newPlayer)
            with open("leaderboard.json", "w") as f:
                json.dump(leaderboard, f)
            # print(leaderboard)
            #updatedJSON = json.dumps(leaderboard)
            #f = open("leaderboard.json", "w")
            #f.write(updatedJSON)
            #f.close()
        
        alreadyInQueueFlag = 0
        for player in self.bot.queue:
            if interaction.user.id == player["id"]:
                alreadyInQueueFlag = 1
                break
        if (alreadyInQueueFlag == 0):
            # Place player in queue
            with open("leaderboard.json", "r") as f:
                leaderboard = json.load(f)
            #leaderboard = json.load(open("leaderboard.json"))
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
        
        numTeams = len(self.bot.queue) // 3
        numQueues = len(self.bot.duoTrioQueue)

        if findDictInList(self.bot.queue, "id", interaction.user.id) == None: # If player is not in queue yet
            await interaction.response.send_message(f"Please join the queue for volleyball first before doing this!", ephemeral=True)
        else:   # If player is in queue
            if (numTeams <= numQueues):
                await interaction.response.send_message(f"No more special queues available!", ephemeral=True)
            # Add selector menu for their duo/trio
            else:
                foundFlag = 0
                for queues in self.bot.duoTrioQueue:
                    if (findDictInList(queues, "id", interaction.user.id) != None):
                        foundFlag = 1
                        break
                if (foundFlag == 0):
                    await interaction.response.send_message("Please select who you want to queue with!", view=SelectorView(bot=self.bot, interaction=interaction))
                else:
                    await interaction.response.send_message(f"You are already queued with people!", ephemeral=True)

        # await interaction.response.defer()
        
        
    @discord.ui.button(label="Exit Queue", style=discord.ButtonStyle.red, custom_id="Exit Queue Button")
    async def exit_queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if findDictInList(self.bot.queue, "id", interaction.user.id) == None:
            await interaction.response.send_message(f"You ({interaction.user.name}) are not in the queue for volleyball!", ephemeral=True)
        else:
            self.bot.queue.remove(findDictInList(self.bot.queue, "id", interaction.user.id))
            for queues in self.bot.duoTrioQueue:
                retVal = findDictInList(queues, "id", interaction.user.id)
                if (retVal != None):
                    if (len(queues) == 2):
                        self.bot.duoTrioQueue.remove(queues)
                    else:
                        queues.remove(retVal)
            await interaction.response.send_message(f"You ({interaction.user.name}) have exited the queue for volleyball!", ephemeral=True)
            print(self.bot.duoTrioQueue)
    
    @discord.ui.button(label="View Queue", style=discord.ButtonStyle.blurple, custom_id="View Queue Button")
    async def view_queue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        queue_string = ""
        leaderboard = json.load(open("leaderboard.json"))
        # print(leaderboard)
        for player in self.bot.queue:
            # print(player)
            player = findDictInList(leaderboard, "id", player["id"])
            #print(get_rank(self.bot.ranks, player))
            #emoji = "<:" + get_rank(self.bot.ranks, player) + ">"
            queue_string = queue_string + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"

        embed = discord.Embed(title="Valoball Queue", description=queue_string,colour=0x00f549)
        if self.bot.queueMessage != None:
            await self.bot.queueMessage.delete()
        self.bot.queueMessage = await interaction.channel.send(embed=embed)
        await interaction.response.defer()
    
    @discord.ui.button(label="Generate Teams", style=discord.ButtonStyle.blurple, custom_id="Generate Teams Button")
    async def generate_teams_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        # print(self.bot.duoTrioQueue)
        with open("teams.json", 'r') as f:
            team_data = json.load(f)
        #f = open('teams.json')
        #team_data = json.load(f)

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
        for team in self.bot.teams:
            team_id = get_team_id(team)
            if team_data.get(team_id) == None: #If this team has never played a game together before
                team_data[team_id] = {"players": team, "wins": 0, "losses": 0, "team_name": generate_team_name(team_id)} #Add them to the teams list and write it to the file
                with open('teams.json', 'w') as f:
                    json.dump(team_data, f)

        for message in self.bot.games_messages: #Clear all the old games messages
            await message.delete()
        self.bot.games_messages.clear()

        num_games = len(self.bot.teams) // 2
        self.bot.game_scores = []
        self.bot.games_embeds = []
        self.bot.matchups = []
        teamsMessage = ""
        for game in range(0, num_games):
            self.bot.game_scores.append([0,0])
        for game in range(0, num_games): #Create the game messages
            teamsMessage = ""
            teams = []
            for team_num in range(2 * game, 2 * game + 2): #For each set of 2 teams
                team = self.bot.teams[team_num]
                team_id = get_team_id(team)
                teams.append(team_data[team_id])
                #teamsMessage = teamsMessage + "**" + team_data[team_id]["team_name"] + ":** **Elo:** " + str(int(getTeamAverage(team))) + " | **Winrate:**" + str(round(((team_data[team_id]["wins"] / max(1, (team_data[team_id]["wins"] + team_data[team_id]["losses"]))) * 100), 2)) + "%\n"
                teamsMessage = teamsMessage + "**" + team_data[team_id]["team_name"] + ":** **Elo:** " + str(int(getTeamAverage(team))) + " | **Winrate:**" + str(round((team_data[team_id]["wins"] / max(1, (team_data[team_id]["wins"] + team_data[team_id]["losses"])) * 100), 2)) + "%\n"
                for player in team:
                    teamsMessage = teamsMessage + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
                teamsMessage = teamsMessage + "\n"
            self.bot.matchups.append([2 * game, 2 * game + 1])
            embed = discord.Embed(title=f"Game {game + 1}", description=teamsMessage,colour=0x00a2ed)
            view = Score_Report_Button(teams, self.bot, game)
            self.bot.games_messages.append(await interaction.channel.send(embed=embed, view=view))
            self.bot.games_embeds.append(embed)
        teamsMessage = ""
        if num_games % 2 != 0: #If there is an odd number of teams, print the one that is on deck
            teamsMessage = ""
            team = self.bot.teams[len(self.bot.teams) - 1]
            team_id = get_team_id(team)
            teamsMessage = teamsMessage + "**" + team_data[team_id]["team_name"] + ":** **Elo:** " + str(int(getTeamAverage(team))) + " | **Winrate:**" + str(round((team_data[team_id]["wins"] / max(1, (team_data[team_id]["wins"] + team_data[team_id]["losses"])) * 100), 2)) + "%\n"
            for player in team:
                teamsMessage = teamsMessage + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
            teamsMessage = teamsMessage + "\n"
            embed = discord.Embed(title="On Deck", description=teamsMessage,colour=0x00a2ed)
            self.bot.games_messages.append(await interaction.channel.send(embed=embed))
            self.bot.games_embeds.append(embed)
        await interaction.response.defer()

        '''    
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
        '''
    @discord.ui.button(label="Finalize Scores", style=discord.ButtonStyle.blurple, custom_id="Finalize Scores Button")
    async def score_report_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        #print(self.bot.game_scores)
        #print(self.bot.matchups)
        pregame_stats = self.bot.teams
        match_results = []
        for i in range(len(self.bot.matchups)):
            #Calculate Elo Changes For Each Player
            #Update player stats and team stats
            team1 = self.bot.teams[self.bot.matchups[i][0]]
            score1 = self.bot.game_scores[i][0]
            team2 = self.bot.teams[self.bot.matchups[i][1]]
            score2 = self.bot.game_scores[i][1]
            if score1 > score2:
                match_results.append([self.bot.matchups[i][0], self.bot.matchups[i][1]])
            else:
                match_results.append([self.bot.matchups[i][1], self.bot.matchups[i][0]])
            update_stats([team1,team2], [score1,score2], self.bot)
            self.bot.teams = refresh_teams(self.bot)
            team1 = self.bot.teams[self.bot.matchups[i][0]]
            team2 = self.bot.teams[self.bot.matchups[i][1]]
            #Update Embeds To Display Elo Changes and Winners/Losers
            await update_embed([team1,team2], self.bot, i, [pregame_stats[self.bot.matchups[i][0]],pregame_stats[self.bot.matchups[i][1]]])
        #Determine New Matchups
        #print(match_results)
        if len(self.bot.teams) % 2 == 0:
            for i in range(len(match_results) - 1):
                loss = match_results[i][1]
                match_results[i][1] = match_results[i + 1][0]
                match_results[i + 1][0] = loss
        if len(self.bot.teams) % 2 == 1:
            team_indexes = list(range(0, len(self.bot.teams)))
            temp = []
            for ind in range(len(team_indexes)):
                for match in match_results:
                    if ind in match:
                        temp.append(ind)
            for item in temp:
                team_indexes.remove(item)
            for i in range(len(match_results)):
                if i == len(match_results) - 1:
                    match_results[i][1] = team_indexes[0]
                else:
                    loss = match_results[i][1]
                    match_results[i][1] = match_results[i + 1][0]
                    match_results[i + 1][0] = loss
        #print(match_results)
        #Wait 30 Seconds
        await interaction.response.defer()
        await asyncio.sleep(5)
        #Update Embeds and data structures to reflect new matchups.
        self.bot.matchups = match_results
        with open("teams.json", 'r') as f:
            team_data = json.load(f)

        #print("GETS HERE")
        for game in match_results:
            teamsMessage = ""
            teams = []
            for team_num in game:
                #print(team_num)
                team = self.bot.teams[team_num]
                #print(team)
                team_id = get_team_id(team)
                teams.append(team_data[team_id])
                teamsMessage = teamsMessage + "**" + team_data[team_id]["team_name"] + ":** **Elo:** " + str(int(getTeamAverage(team))) + " | **Winrate:**" + str(round((team_data[team_id]["wins"] / max(1, (team_data[team_id]["wins"] + team_data[team_id]["losses"])) * 100), 2)) + "%\n"
                for player in team:
                    teamsMessage = teamsMessage + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
                teamsMessage = teamsMessage + "\n"
            new_view = Score_Report_Button(teams, self.bot, match_results.index(game))
            new_embed = discord.Embed(title=f"Game {match_results.index(game) + 1}", description=teamsMessage,colour=0x00a2ed)
            original_message = self.bot.games_messages[match_results.index(game)]
            original_message = await original_message.edit(embed = new_embed, view=new_view)
        teamsMessage = ""
        if len(self.bot.teams) % 2  == 1:
            team_indexes = list(range(0, len(self.bot.teams)))
            temp = []
            for ind in range(len(team_indexes)):
                for match in match_results:
                    if ind in match:
                        temp.append(ind)
            for item in temp:
                team_indexes.remove(item)
            teamsMessage = ""
            team = self.bot.teams[team_indexes[0]]
            team_id = get_team_id(team)
            teamsMessage = teamsMessage + "**" + team_data[team_id]["team_name"] + ":** **Elo:** " + str(int(getTeamAverage(team))) + " | **Winrate:**" + str(round((team_data[team_id]["wins"] / max(1, (team_data[team_id]["wins"] + team_data[team_id]["losses"])) * 100), 2)) + "%\n"
            for player in team:
                teamsMessage = teamsMessage + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
            teamsMessage = teamsMessage + "\n"
            new_embed = discord.Embed(title=f"On Deck", description=teamsMessage,colour=0x00a2ed)
            original_message = self.bot.games_messages[-1]
            original_message = await original_message.edit(embed = new_embed, view = None)
        teamsMessage = ""



        
    
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
            leaderboardMessage = leaderboardMessage + "<:" + get_rank(self.bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
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

class Score_Report_Button(discord.ui.View):
    def __init__(self, teams, bot, game):
        super().__init__(timeout = None)
        self.bot = bot
        self.teams = teams
        self.game = game

    @discord.ui.button(label="Report Score", style=discord.ButtonStyle.blurple, custom_id="Report Score Button")
    async def report_score_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = Score_Report(self.teams, self.bot, self.game)
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.bot.game_scores[self.game] = [modal.children[0].value, modal.children[1].value]



class Score_Report(ui.Modal):
    def __init__(self, teams, bot, game):
        super().__init__(title='Score Report')
        self.bot = bot
        team_1_name = teams[0]["team_name"]
        team_2_name = teams[1]["team_name"]
        self.team_1_score = ui.TextInput(label=f'{team_1_name} Score', required=True, max_length=2, min_length=1)
        self.team_2_score = ui.TextInput(label=f'{team_2_name} Score', required=True, max_length=2, min_length=1)
        self.add_item(self.team_1_score)
        self.add_item(self.team_2_score)
    
    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()

class Selector(discord.ui.Select):
    def __init__(self, interaction: discord.Interaction, bot):
        self.bot = bot
        selectorOptions = []
        for player in bot.queue:
            if (player["id"] == interaction.user.id):
                # Don't add if player is the person selecting queues
                break
            else:
                foundFlag = 0
                for queues in bot.duoTrioQueue:
                    if (findDictInList(queues, "id", player["id"]) != None):
                        foundFlag = 1
                        break
                if (foundFlag == 0):
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

def generate_team_name(id):
    animals = ["Apes","Badgers","Bats","Bears","Buffalo","Cats","Cheetahs","Deer","Dolphins","Donkeys","Echidnas","Elephants","Elk","Ferrets","Foxes","Giraffes","Gorillas","Hares","Hedgehogs","Hippopotamuses","Horses","Hyenas","Jaguars","Kangaroos","Kittens","Lemur","Leopards","Lions","Martens","Mice","Moles","Monkeys","Otters","Platypus","Porcupines","Porpoises","Prairie","Dogs","Rabbits","Rhinoceroses","Roes","Rooks","Seals","Sheep","Squirrels","Tigers","Whales","Wolves","Wombats","Zebras"]
    adjectives = ["aback","abaft","abandoned","abashed","aberrant","abhorrent","abiding","abject","ablaze","able","abnormal","aboard","aboriginal","abortive","abounding","abrasive","abrupt","absent","absorbed","absorbing","abstracted","absurd","abundant","abusive","acceptable","accessible","accidental","accurate","acid","acidic","acoustic","acrid","actually","ad","hoc","adamant","adaptable","addicted","adhesive","adjoining","adorable","adventurous","afraid","aggressive","agonizing","agreeable","ahead","ajar","alcoholic","alert","alike","alive","alleged","alluring","aloof","amazing","ambiguous","ambitious","amuck","amused","amusing","ancient","angry","animated","annoyed","annoying","anxious","apathetic","aquatic","aromatic","arrogant","ashamed","aspiring","assorted","astonishing","attractive","auspicious","automatic","available","average","awake","aware","awesome","awful","axiomatic","bad","barbarous","bashful","bawdy","beautiful","befitting","belligerent","beneficial","bent","berserk","best","better","bewildered","big","billowy","bite-sized","bitter","bizarre","black","black-and-white","bloody","blue","blue-eyed","blushing","boiling","boorish","bored","boring","bouncy","boundless","brainy","brash","brave","brawny","breakable","breezy","brief","bright","bright","broad","broken","brown","bumpy","burly","bustling","busy","cagey","calculating","callous","calm","capable","capricious","careful","careless","caring","cautious","ceaseless","certain","changeable","charming","cheap","cheerful","chemical","chief","childlike","chilly","chivalrous","chubby","chunky","clammy","classy","clean","clear","clever","cloistered","cloudy","closed","clumsy","cluttered","coherent","cold","colorful","colossal","combative","comfortable","common","complete","complex","concerned","condemned","confused","conscious","cooing","cool","cooperative","coordinated","courageous","cowardly","crabby","craven","crazy","creepy","crooked","crowded","cruel","cuddly","cultured","cumbersome","curious","curly","curved","curvy","cut","cute","cute","cynical","daffy","daily","damaged","damaging","damp","dangerous","dapper","dark","dashing","dazzling","dead","deadpan","deafening","dear","debonair","decisive","decorous","deep","deeply","defeated","defective","defiant","delicate","delicious","delightful","demonic","delirious","dependent","depressed","deranged","descriptive","deserted","detailed","determined","devilish","didactic","different","difficult","diligent","direful","dirty","disagreeable","disastrous","discreet","disgusted","disgusting","disillusioned","dispensable","distinct","disturbed","divergent","dizzy","domineering","doubtful","drab","draconian","dramatic","dreary","drunk","dry","dull","dusty","dynamic","dysfunctional","eager","early","earsplitting","earthy","easy","eatable","economic","educated","efficacious","efficient","eight","elastic","elated","elderly","electric","elegant","elfin","elite","embarrassed","eminent","empty","enchanted","enchanting","encouraging","endurable","energetic","enormous","entertaining","enthusiastic","envious","equable","equal","erect","erratic","ethereal","evanescent","evasive","even excellent excited","exciting exclusive","exotic","expensive","extra-large extra-small exuberant","exultant","fabulous","faded","faint fair","faithful","fallacious","false familiar famous","fanatical","fancy","fantastic","far"," far-flung"," fascinated","fast","fat faulty","fearful fearless","feeble feigned","female fertile","festive","few fierce","filthy","fine","finicky","first"," five"," fixed"," flagrant","flaky","flashy","flat","flawless","flimsy"," flippant","flowery","fluffy","fluttering"," foamy","foolish","foregoing","forgetful","fortunate","four frail","fragile","frantic","free"," freezing"," frequent"," fresh"," fretful","friendly","frightened frightening full fumbling functional","funny","furry furtive","future futuristic","fuzzy ","gabby","gainful","gamy","gaping","garrulous","gaudy","general gentle","giant","giddy","gifted","gigantic","glamorous","gleaming","glib","glistening glorious","glossy","godly","good","goofy","gorgeous","graceful","grandiose","grateful gratis","gray greasy great","greedy","green grey grieving","groovy","grotesque","grouchy","grubby gruesome","grumpy","guarded","guiltless","gullible gusty","guttural H habitual","half","hallowed","halting","handsome","handsomely","handy","hanging","hapless","happy","hard","hard-to-find","harmonious","harsh","hateful","heady","healthy","heartbreaking","heavenly heavy hellish","helpful","helpless","hesitant","hideous high","highfalutin","high-pitched","hilarious","hissing","historical","holistic","hollow","homeless","homely","honorable","horrible","hospitable","hot huge","hulking","humdrum","humorous","hungry","hurried","hurt","hushed","husky","hypnotic","hysterical","icky","icy","idiotic","ignorant","ill","illegal","ill-fated","ill-informed","illustrious","imaginary","immense","imminent","impartial","imperfect","impolite","important","imported","impossible","incandescent","incompetent","inconclusive","industrious","incredible","inexpensive","infamous","innate","innocent","inquisitive","insidious","instinctive","intelligent","interesting","internal","invincible","irate","irritating","itchy","jaded","jagged","jazzy","jealous","jittery","jobless","jolly","joyous","judicious","juicy","jumbled","jumpy","juvenile","kaput","keen","kind","kindhearted","kindly","knotty","knowing","knowledgeable","known","labored","lackadaisical","lacking","lame","lamentable","languid","large","last","late","laughable","lavish","lazy","lean","learned","left","legal","lethal","level","lewd","light","like","likeable","limping","literate","little","lively","lively","living","lonely","long","longing","long-term","loose","lopsided","loud","loutish","lovely","loving","low","lowly","lucky","ludicrous","lumpy","lush","luxuriant","lying","lyrical","macabre","macho","maddening","madly","magenta","magical","magnificent","majestic","makeshift","male","malicious","mammoth","maniacal","many","marked","massive","married","marvelous","material","materialistic","mature","mean","measly","meaty","medical","meek","mellow","melodic","melted","merciful","mere","messy","mighty","military","milky","mindless","miniature","minor","miscreant","misty","mixed","moaning","modern","moldy","momentous","motionless","mountainous","muddled","mundane","murky","mushy","mute","mysterious","naive","nappy","narrow","nasty","natural","naughty","nauseating","near","neat","nebulous","necessary","needless","needy","neighborly","nervous","new","next","nice","nifty","nimble","nine","nippy","noiseless","noisy","nonchalant","nondescript","nonstop","normal","nostalgic","nosy","noxious","null","numberless","numerous","nutritious","nutty","oafish","obedient","obeisant","obese","obnoxious","obscene","obsequious","observant","obsolete","obtainable","oceanic","odd","offbeat","old","old-fashioned","omniscient","one","onerous","open","opposite","optimal","orange","ordinary","organic","ossified","outgoing","outrageous","outstanding","oval","overconfident","overjoyed","overrated","overt","overwrought","painful","painstaking","pale","paltry","panicky","panoramic","parallel","parched","parsimonious","past","pastoral","pathetic","peaceful","penitent","perfect","periodic","permissible","perpetual","petite","petite","phobic","physical","picayune","pink","piquant","placid","plain","plant","plastic","plausible","pleasant","plucky","pointless","poised","polite","political","poor","possessive","possible","powerful","precious","premium","present","pretty","previous","pricey","prickly","private","probable","productive","profuse","protective","proud","psychedelic","psychotic","public","puffy","pumped","puny","purple","purring","pushy","puzzled","puzzling","quack","quaint","quarrelsome","questionable","quick","quickest","quiet","quirky","quixotic","quizzical","rabid","racial","ragged","rainy","rambunctious","rampant","rapid","rare","raspy","ratty","ready","real","rebel","receptive","recondite","red","redundant","reflective","regular","relieved","remarkable","reminiscent","repulsive","resolute","resonant","responsible","rhetorical","rich","right","righteous","rightful","rigid","ripe","ritzy","roasted","robust","romantic","roomy","rotten","rough","round","royal","ruddy","rude","rural","rustic","ruthless","sable","sad","safe","salty","same","sassy","satisfying","savory","scandalous","scarce","scared","scary","scattered","scientific","scintillating","scrawny","screeching","second","second-hand","secret","secretive","sedate","seemly","selective","selfish","separate","serious","shaggy","shaky","shallow","sharp","shiny","shivering","shocking","short","shrill","shut","shy","sick","silent","silent","silky","silly","simple","simplistic","sincere","six","skillful","skinny","sleepy","slim","slimy","slippery","sloppy","slow","small","smart","smelly","smiling","smoggy","smooth","sneaky","snobbish","snotty","soft","soggy","solid","somber","sophisticated","sordid","sore","sore","sour","sparkling","special","spectacular","spicy","spiffy","spiky","spiritual","spiteful","splendid","spooky","spotless","spotted","spotty","spurious","squalid","square","squealing","squeamish","staking","stale","standing","statuesque","steadfast","steady","steep","stereotyped","sticky","stiff","stimulating","stingy","stormy","straight","strange","striped","strong","stupendous","stupid","sturdy","subdued","subsequent","substantial","successful","succinct","sudden","sulky","super","superb","superficial","supreme","swanky","sweet","sweltering","swift","symptomatic","synonymous","taboo","tacit","tacky","talented","tall","tame","tan","tangible","tangy","tart","tasteful","tasteless","tasty","tawdry","tearful","tedious","teeny","teeny-tiny","telling","temporary","ten","tender tense","tense","tenuous","terrible","terrific","tested","testy","thankful","therapeutic","thick","thin","thinkable","third","thirsty","thoughtful","thoughtless","threatening","three","thundering","tidy","tight","tightfisted","tiny","tired","tiresome","toothsome","torpid","tough","towering","tranquil","trashy","tremendous","tricky","trite","troubled","truculent","true","truthful","two","typical","ubiquitous","ugliest","ugly","ultra","unable","unaccountable","unadvised","unarmed","unbecoming","unbiased","uncovered","understood","undesirable","unequal","unequaled","uneven","unhealthy","uninterested","unique","unkempt","unknown","unnatural","unruly","unsightly","unsuitable","untidy","unused","unusual","unwieldy","unwritten","upbeat","uppity","upset","uptight","used","useful","useless","utopian","utter","uttermost","vacuous","vagabond","vague","valuable","various","vast","vengeful","venomous","verdant","versed","victorious","vigorous","violent","violet","vivacious","voiceless","volatile","voracious","vulgar","wacky","waggish","waiting","","wakeful","wandering","wanting","warlike","warm","wary","wasteful","watery","weak","wealthy","weary","well-groomed","well-made","well-off","well-to-do","wet","whimsical","whispering","white","whole","wholesale","wicked","wide","wide-eyed","wiggly","wild","willing","windy","wiry","wise","wistful","witty","woebegone","womanly","wonderful","wooden","woozy","workable","worried","worthless","wrathful","wretched","wrong","wry","xenophobic","yellow","yielding","young","youthful","yummy","zany","zealous","zesty","zippy","zonked"]
    adjectives = [adjective.capitalize() for adjective in adjectives]
    last4 = id[len(id)- 4:]
    last4 = int(((1098/9999) * (int(last4) - 9999) + 1098)) #Normalize to the range of the array
    next2 = id[len(id) - 5: len(id) - 3]
    next2 = int(((49/99) * (int(next2) - 99) + 49)) #Normalize to the range of the array
    return "The " + adjectives[int(last4)] + " " + animals[int(next2)] 

def get_team_id(team):
    id_sum = 0
    for player in team:
        id_sum = id_sum + player["id"]
    return str(id_sum)

def update_stats(teams, score, bot):
    k_factor = 420 #The max elo a team should be able to gain/lose in a game
    if score[0] > score[1]:
        win = 0
    else:
        win = 1
    
    exp1 = get_expected(teams, 0)
    exp2 = get_expected(teams, 1)

    if win == 0:
        elo1 = k_factor*(1 - exp1)
        elo2 = k_factor*(0 - exp2)
        update_players_stats(teams[0], elo1, 1, bot)
        update_players_stats(teams[1], elo2, -1, bot)
    else:
        elo1 = k_factor*(0 - exp1)
        elo2 = k_factor*(1 - exp2)
        update_players_stats(teams[0], elo1, -1, bot)
        update_players_stats(teams[1], elo2, 1, bot)

    

def get_expected(teams, index):
    elo_diff_factor = 400 #The elo difference where the better team should have a ~90% chance of winning

    avg1 = getTeamAverage(teams[0])
    avg2 = getTeamAverage(teams[1])

    if index == 0:
        return 1/(1 + 10**((avg2 - avg1)/elo_diff_factor))
    else:
        return 1/(1 + 10**((avg1 - avg2)/elo_diff_factor))

def update_players_stats(team, elo, result, bot):
    with open('teams.json', 'r') as f:
        team_data = json.load(f)
    with open('leaderboard.json', 'r') as f:
        data = json.load(f)
    team_elo = get_total_team_elo(team)
    team_id = get_team_id(team)
    win_players = []
    for player in team:
        for entry in data:
            if entry["id"] == player["id"]:
                if result == 1:
                    #print(1 - (entry["elo"] / team_elo))
                    win_players.append({"id": entry["id"], "factor": 1 - (entry["elo"] / team_elo)})
                    #entry["elo"] = int(entry["elo"] + ((1 - (entry["elo"] / team_elo)) * elo))
                    entry["wins"] = entry["wins"] + 1
                else:
                    #print(entry)
                    #print(((entry["elo"] / team_elo) * elo))
                    entry["elo"] = int(entry["elo"] + ((entry["elo"] / team_elo) * elo))
                    entry["losses"] = entry["losses"] + 1
                with open('leaderboard.json', 'w') as f:
                    json.dump(data, f)
                break

    sum_inverse_elos = 0
    for player in win_players:
        sum_inverse_elos = sum_inverse_elos + player["factor"]

    with open('leaderboard.json', 'r') as f:
        data = json.load(f)

    for entry in data:
        if result == 1:
            for player in win_players:
                if player["id"] == entry["id"]:
                    entry["elo"] = int(entry["elo"] + (player["factor"] / sum_inverse_elos) * elo)
    with open('leaderboard.json', 'w') as f:
        json.dump(data, f)
    
    for entry in team_data[team_id]["players"]:
        if result == 1:
            for player in win_players:
                if player["id"] == entry["id"]:
                    entry["elo"] = int(entry["elo"] + (player["factor"] / sum_inverse_elos) * elo)
            #entry["elo"] = int(entry["elo"] + result * (1 - (entry["elo"] / team_elo) * elo))
            entry["wins"] = entry["wins"] + 1
        else:
            entry["elo"] = int(entry["elo"] + ((entry["elo"] / team_elo) * elo))
            entry["losses"] = entry["losses"] + 1
        with open('teams.json', 'w') as f:
            json.dump(team_data, f)
    if result == 1:
        team_data[team_id]["wins"] = team_data[team_id]["wins"] + 1
    else:
        team_data[team_id]["losses"] = team_data[team_id]["losses"] + 1
    with open('teams.json', 'w') as f:
        json.dump(team_data, f)
    bot.team_data = team_data
    bot.data = data

def get_total_team_elo(team):
    total = 0
    for player in team:
        total = total + player["elo"]
    return total
   
async def update_embed(teams, bot, num, pregame_stats):
    print("PREGAME")
    print(pregame_stats)
    print("TEAMS")
    print(teams)
    print("ALL TEAMS")
    print(bot.teams)
    print("INDEXES")
    print(len(teams))
    with open('teams.json', 'r') as f:
        team_data = json.load(f)
    original_message = bot.games_messages[num]
    teamsMessage = ""
    for team in teams:
        team_id = get_team_id(team)
        teamsMessage = teamsMessage + "**" + team_data[team_id]["team_name"] + ":** **Elo:** " + str(int(getTeamAverage(team))) + " | **Winrate:**" + str(round((team_data[team_id]["wins"] / max(1, (team_data[team_id]["wins"] + team_data[team_id]["losses"])) * 100), 2)) + "%\n"
        for player in team:
            print(f"team index: {bot.teams.index(team)}")
            print(f"PLAYER: {player}")
            print(f"player index on team:{team.index(player)}")
            for pre_team in pregame_stats:
                for entry in pre_team:
                    if entry["id"] == player["id"]:
                        target = entry
            if player["elo"] > target["elo"]:
                teamsMessage = teamsMessage + "<:" + get_rank(bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "(+" + str(int(player["elo"]) - int(target["elo"])) + ")  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
            else:
                teamsMessage = teamsMessage + "<:" + get_rank(bot.ranks, player) + "> " + "**" + player["name"] + "**  **ELO:** " + str(player["elo"]) + "(-" + str(abs(int(player["elo"]) - int(target["elo"]))) + ")  **Winrate:**  " + str(round((player["wins"] / max(1, (player["wins"] + player["losses"])) * 100), 2)) + "%\n"
        teamsMessage = teamsMessage + "\n"
    new_embed = discord.Embed(title=f"Game {num + 1}", description=teamsMessage,colour=0x00a2ed)
    original_message = await original_message.edit(embed = new_embed, view=None)

def refresh_teams(bot):
    with open('teams.json', 'r') as f:
        team_data = json.load(f)
    temp = []
    for team in bot.teams:
        team_id = get_team_id(team)
        temp.append(team_data[team_id]["players"])
    return temp

async def setup(bot):
    await bot.add_cog(Valoball(bot))
