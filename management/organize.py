import logging
import os
import traceback
import csv
import json

logger = logging.getLogger(__name__)

class Organize:
    def __init__(self):
        file_path = os.path.join("project_inventory", "test_spreadsheet.csv")
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            data = list(reader)
        self.data = data


    def get_project(self): # returns the project name, start date, and end date
        project_name = self.data[0][0]
        start = self.data[1][0]
        end = self.data[2][0]
        return project_name, start, end

    def organize_team(self): # organizes the data from the spreadsheet
        team = []
        try:
            #finds the team
            for i, row in enumerate(self.data):
                if i > 3:
                    email = row[2]
                    name = row[1]
                    member = (name, email)
                    if member not in team:
                        team.append(member)
            
            #finds the tasks for each team member
            for i, person in enumerate(team):
                for j, row in enumerate(self.data):
                    if row[1] in person:
                        task = (row[0], row[3], row[5], row[4])
                        team[i] = team[i] + (task)

            return team
        except Exception as e:  
            error = traceback.format_exc()
            logger.info(f"Error reading data from spreadsheet: {error}")

    def set_json(self): # sets up the json with the project name, start date, and end date
        project_name, start, end = self.get_project()

        project = {
            project_name: {
                "start date": start,
                "end date": end,
                "members": {}
            }
        }
        return project
    
    def get_tasks(self, member, project_name, project_data): # gets the tasks for each team member
        count = 2
        while count < len(member):
            task = member[count]
            priority = member[count+1]
            due = member[count+2]
            etc = member[count+3]
            project_data[project_name]["members"][member[0]][task] = {
                "priority": priority,
                "due date": due,
                "estimated completion": etc,
                "actual_completion": None
            }
            count += 4
        return project_data
    
    def write_member(self, project_data, member, project_name): # writes the tasks for each team member
        project_data[project_name]["members"][member[0]] = {
            "email": member[1],
            "current task": None,
            "CT due date": None,
        }
        project_data = self.get_tasks(member, project_name, project_data)
        return project_data

    def write_json(self): # puts it all together; writes the final json output
        project_name, start, end = self.get_project() # gets the project name, start, and end date
        members = self.organize_team() # gets the team
        
        project_data = self.set_json() # sets up the json
        for member in members: # writes the tasks for each team member
            #member = ["name", "email", "task", "priority", "due date", "ETC"]
            project_data = self.write_member(project_data, member, project_name)
        
        file_path = os.path.join("project_inventory", "test_tasks.json")
        with open(file_path, "w") as f:
            json.dump(project_data, f, indent=4)

        logger.info(f"Project data written to {file_path}")
        logger.info(f"Project data: {project_data}")
        return project_data