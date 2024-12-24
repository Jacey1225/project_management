from management.record import Record
from management.organize import Organize
from track_performance.email_tasks import EmailTasks
import pytest
import os
import logging

logger = logging.getLogger(__name__)

class TestMain:
    @pytest.fixture
    def rc(self, monkeypatch):
        def mock_input(prompt):
            if prompt == "Enter the spreadsheet key: ":
                return "1Vh-_KJyMxXj19KAYlUwoWkOSaNPeXnJlu0Shr3KaNVI"
            elif prompt == "Enter the worksheet name: ":
                return "reference tasks"

        monkeypatch.setattr("builtins.input", mock_input)
        
        spreadsheet_key = input("Enter the spreadsheet key: ")
        worksheet_name = input("Enter the worksheet name: ")
        rc = Record(spreadsheet_key, worksheet_name)
        return rc   
    
    @pytest.mark.selected
    def test_main(self, rc):
        file_path = os.path.join("project_inventory", "test_spreadsheet.csv")
        rc.read_spreadsheet(file_path)

        og = Organize()
        og.write_json()

        email = EmailTasks("Test Project", ["jacey"])
        email.send_mail()

        #Run: python -m flask run --host=0.0.0.0 --port=5000 