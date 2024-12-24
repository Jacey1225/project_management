import pytest
from management.organize import Organize
import logging


class TestOrganize:
    @pytest.fixture
    def og(self):
        return Organize()

    
    def test_organize_team(self, og):
        member = ["jacey", "jaceysimps@gmail.com", "task 1", "high", "01/01/25", "5", "task 5", "low", "01/03/25", "3"]
        team = og.write_member(member)
        assert team is not False
    @pytest.mark.selected
    def test_write_json(self, og):
        project_data = og.write_json()
        assert project_data
