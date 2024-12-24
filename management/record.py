import gspread
from google.oauth2.service_account import Credentials
from management.organize import Organize
import logging
import traceback
import csv
import os
import json

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

    def open_sheet(self): # opens the spreadsheet
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

# Reads data from the spreadsheet and exports it to a CSV file

    def read_spreadsheet(self, file_path) -> bool: # reads the data from the spreadsheet
        sheet = self.open_sheet()
        if os.path.exists(file_path):
            logger.info("File already exists. Skipping export.")
            return True
        if sheet:
            try:
                data = sheet.get_all_values()
                with open(file_path, "a+") as file: # writes the data to a CSV file
                    writer = csv.writer(file)
                    for row in data:
                        logger.info(f"Writing row: {row}")
                        list_item = list(row)
                        writer.writerow(list_item)
                logger.info(f"Spreadsheet exported to {file_path}")
                return True
            except gspread.exceptions.APIError as e:
                error = traceback.format_exc()
                logger.info(f"Error reading data from spreadsheet: {error}")
                return False