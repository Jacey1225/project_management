import gspread
from google.oauth2.service_account import Credentials
import logging

logger = logging.getLogger(__name__)

class Record:
    def __init__(self, spreadsheet_key, worksheet_name, credentials_path: str = "project_inventory/pm-testing-444822-bfb818f1b21b.json"):
        self.spreadsheet_key = spreadsheet_key
        self.worksheet_name = worksheet_name
        self.credentials_path = credentials_path
        self.client = self._authenticate()

    def _authenticate(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(self.credentials_path, scopes=scope)
        return gspread.authorize(creds)

    def open_sheet(self):
        try:
            spreadsheet = self.client.open_by_key(self.spreadsheet_key)

            worksheet_list = [worksheet.title for worksheet in spreadsheet.worksheets()]
            logger.info(f"Available worksheets: {worksheet_list}")
            worksheet = spreadsheet.worksheet(self.worksheet_name)
            return worksheet
        except gspread.exceptions.SpreadsheetNotFound:
            logger.info(f"Spreadsheet with key {self.spreadsheet_key} not found.")
        except gspread.exceptions.WorksheetNotFound:
            logger.info(f"Worksheet {self.worksheet_name} not found in the spreadsheet.")
        return None

    def read_spreadsheet(self, filename: str):
        sheet = self.open_sheet()
        if sheet:
            try:
                expected_headers = ["project title"]
                data = sheet.get_all_records(expected_headers=expected_headers)
                logger.info(f"data read successfully: {data}")
                
                sheet.export(filename)
                logger.info(f"Spreadsheet exported to {filename}")
            except gspread.exceptions.APIError as e:
                logger.info(f"Error reading data from spreadsheet: {e}")