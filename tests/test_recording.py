import pytest
import logging
import os

from management.record import Record


logger = logging.getLogger(__name__)

class TestRecording:
    def test_sample(self):
        logger.info("1 + 2 = 3")

        assert 1 + 2 == 3

    @pytest.fixture
    def rc(self):
        sheet_key = "1Vh-_KJyMxXj19KAYlUwoWkOSaNPeXnJlu0Shr3KaNVI"
        sheet_name = "reference tasks"
        return Record(sheet_key, sheet_name)

    def test_request_form(self, rc):
        filename = "test_spreadsheet.csv"
        data = rc.read_spreadsheet(filename)
        assert data is not False

    
    def test_organize_data(self, rc):
        team_tasks = rc.organize_data()
        logger.info(f"Team tasks: {team_tasks}")

        assert team_tasks
    
    @pytest.mark.selected
    def test_to_json(self, rc):
        json_data = rc.export_to_json()

        file_path = os.path.join("project_inventory", "test_tasks.json")
        with open(file_path, "r") as file:
            data = file.read()
            assert data is not None