import gspread
from oauth2client.service_account import ServiceAccountCredentials

DEFAULT_SCOPE = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]


class TeamSpread():

    def __init__(self, credentials_path, spread_key, sheet_name):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, DEFAULT_SCOPE)
        self.gc = gspread.authorize(self.credentials)
        self.spread_sheet = self.gc.open_by_key(spread_key)
        self.sheet_name = sheet_name

    def update_team(self, team_data):
        # element in team_data : [number, created_at, team_name, runner1, runner2, runner3, runner4]
        worksheet = self.spread_sheet.worksheet(self.sheet_name)
        print("Update team data: %d rows" % (len(team_data)))

        cell_list = worksheet.range("A2:G%d" % (len(team_data) + 1))
        for idx, cell in enumerate(cell_list):
            i = int(idx / 7)
            j = idx % 7
            element = team_data[i][j]
            cell.value = element
            
        # Update in batch
        worksheet.update_cells(cell_list)