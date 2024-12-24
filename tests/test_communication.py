import pytest
from track_performance.email_tasks import EmailTasks
from track_performance.email_tasks import app
from flask import Flask


class TestCommunicate:
    @pytest.fixture
    def com(self):
        project_name = "Test Project"
        receivers = ["jacey"]
        return EmailTasks(project_name, receivers)
    @pytest.mark.selected
    def test_mail(self, com):
        client = app.test_client()
        mail = com.send_mail()

        assert mail is True