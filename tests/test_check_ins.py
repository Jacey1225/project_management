import pytest
import os
import subprocess
from track_performance.email_check_in import EmailCheckIn
from track_performance.email_check_in import app
from flask import Flask
import logging

logger = logging.getLogger(__name__)

class TestCheckIn:
    @pytest.fixture
    def check(self):
        project_name = "Test Project"
        receivers = ["jacey"]
        return EmailCheckIn(project_name, receivers)
    
    
    def test_time_interval(self, check):
        interval = check.get_interval()

        assert interval
    
    @pytest.fixture
    def run_flask(self):
        server = subprocess.Popen(["python", "-m", "flask", "run", "--host=127.0.0.1", "--port=5001"])
        yield 
        server.terminate()

    @pytest.mark.selected
    @pytest.mark.usefixtures("run_flask")
    def test_mail_schedule(self, check):
        client = app.test_client()
        check.send_mail()
        logger.info("Schedule started")

    