import pytest
import logging

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

    @pytest.mark.selected
    def test_request_form(self, rc):
        data = rc.read_spreadsheet()
        logger.info(f"Read {len(data)} rows from the spreadsheet.")

        assert len(data) > 0
        assert data is not None
    