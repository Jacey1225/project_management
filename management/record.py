import gspread
from google.oauth2.service_account import Credentials
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

# Reads data from the spreadsheet and exports it to a CSV file

    def read_spreadsheet(self, filename: str) -> bool:
        sheet = self.open_sheet()
        file_path = os.path.join("project_inventory", filename)
        if os.path.exists(file_path):
            logger.info("File already exists. Skipping export.")
            return True
        if sheet:
            try:
                data = sheet.get_all_values()
                
                with open(file_path, "w") as file:
                    writer = csv.writer(file)
                    for row in data:
                        logger.info(f"Writing row: {row}")
                        writer.writerow(row)
                logger.info(f"Spreadsheet exported to {filename}")
                return True
            except gspread.exceptions.APIError as e:
                error = traceback.format_exc()
                logger.info(f"Error reading data from spreadsheet: {error}")
                return False
    def organize_data(self):
        sheet = os.path.join("project_inventory", "test_spreadsheet.csv")
        if os.path.exists(sheet):
            with open(sheet, "r") as f:
                reader = csv.reader(f)
                data = list(reader)
        
        team = []
        try:
            for i, row in enumerate(data):
                if i > 0:
                    email = row[2]
                    name = row[1]
                    member = (name, email)
                    if member not in team:
                        team.append(member)
            
            for i, person in enumerate(team):
                for j, row in enumerate(data):
                    if row[1] in person:
                        task = (row[0], row[3], row[5])
                        team[i] = team[i] + (task)

            logger.info(f"Team: {team}")
            return team
        except Exception as e:
            error = traceback.format_exc()
            logger.info(f"Error reading data from spreadsheet: {error}")

    def member_to_json(self, member):
        name = member[0]
        email = member[1]

        to_json = {name: {
            "email": email,
            "current task": None,
            "tasks": []
        }}
        count = 2
        while count < len(member):
            task = member[count]
            priority = member[count+1]
            due_date = member[count+2]
            task = {
                "task": task,
                "priority": priority,
                "due date": due_date
            }
            to_json[f"{name}"]["tasks"].append(task)
            count += 3
        
        logger.info(f"Converted member to JSON: {to_json}")
        return to_json

    def export_to_json(self) -> bool:
        data = self.organize_data()
        file_path = os.path.join("project_inventory", "test_tasks.json")
        if os.path.exists(file_path):
            logger.info("File already exists. Skipping export.")
            return True
        
        try:
            all_people = {}
            for member in data:
                person = self.member_to_json(member)
                all_people.update(person)

            with open(file_path, "w") as file:
                json.dump(all_people, file, indent = 4)
                
            logger.info(f"Spreadsheet exported to {file_path}")
            return True
        except Exception as e:
            error = traceback.format_exc()
            logger.info(f"Error reading data from spreadsheet: {error}")
            return False
        
