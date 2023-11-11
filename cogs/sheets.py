from discord.ext import commands
from googleapiclient.discovery import build
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Sheets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Initializing Google Authentication...")
        scope = ["https://spreadsheets.google.com/feeds",
                'https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"]  
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)
        bot.client = client
        sheet = client.open("Valoball")  # Open the spreadhseet
        print(sheet)
        bot.sheet = sheet

def get_sheet(bot, sheetName):
    return bot.sheet.worksheet(sheetName)

def get_data_from_nf(worksheet, nf):
    return worksheet.get_values(nf, value_render_option='UNFORMATTED_VALUE')

async def setup(bot):
    await bot.add_cog(Sheets(bot))