import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

credentials_path = "./credentials.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)

gc = gspread.authorize(credentials)

sheet_key = "sheet_key"
sht = gc.open_by_key()
worksheet = sht.worksheet("team")

# Select a range
cell_list = worksheet.range("A2:D5")

for cell in cell_list:
    print(cell.value)

# Update in batch
# worksheet.update_cells(cell_list)