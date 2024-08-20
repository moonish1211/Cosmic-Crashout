import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import pandasql as psql

# credentials_json = "Credentials.json"
credentials_json = "EEG_Game/Credentials.json"

# Set up credentials and authorize the client
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(credentials_json, scopes=scopes)
client = gspread.authorize(creds)

# Open the workbook and the worksheet
sheet_id = "1k00xJp-kqFWDGojwYm6aqRY-TVzrV72LpdIvIRa5u60"
workbook = client.open_by_key(sheet_id)
sheet = workbook.get_worksheet(0)



def findNextRow(mode):
    sheet = getWorksheet(mode)
    values = sheet.col_values(1)
    next_empty_row = len(values) + 1
    return next_empty_row

def inputScore(name, score, mode):
    sheet = getWorksheet(mode)
    row = findNextRow(mode)
    sheet.update_cell(row, 1, name)
    sheet.update_cell(row, 2, score)
def getTopPlayers(limit, mode):  # limit is how many people get shown
    sheet = getWorksheet(mode)
    df = pd.DataFrame(sheet.get_all_records())
    query = f"SELECT * FROM df ORDER BY score DESC LIMIT {limit};"
    result = psql.sqldf(query, locals())
    return result
def getWorksheet(mode):
    if (mode == "easy"):
        sheet = workbook.get_worksheet(0)
    elif (mode == "medium"):
        sheet = workbook.get_worksheet(1)
    elif (mode == "hard"):
        sheet = workbook.get_worksheet(2)
    return sheet

#print(getTopPlayers(10))
#inputScore("test", 4)