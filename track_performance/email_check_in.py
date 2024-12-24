import os
import logging
import traceback
import json
from flask import Flask, render_template, request, Response
from flask.views import View
from flask_mail import Mail, Message
from markupsafe import Markup
import time
from datetime import datetime,timedelta

logger = logging.getLogger(__name__)
try:
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'jsurvice@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ihva xisx fpzd iixb'

    mail = Mail(app)
except Exception as e:
    logger.error(traceback.format_exc())

class EmailCheckIn:
    def __init__(self, project_name, receivers):
        self.project_name = project_name
        self.receivers = receivers
        file_path = os.path.join("project_inventory", "test_tasks.json")
        with open(file_path, "r") as f:
            data = json.load(f)
        
        self.members = data[project_name]["members"]
        self.begin = data[project_name]["start date"]
        self.end = data[project_name]["end date"]

    def get_emails(self):
        try:
            emails = []
            for receiver in self.receivers:
                emails.append((receiver, self.members[receiver]["email"]))
            return emails
        except Exception as e:
            logger.error(traceback.format_exc())
            return False
    
    def get_interval(self):
        start_date = datetime.strptime(self.begin, "%m/%d/%Y")
        end_date = datetime.strptime(self.end, "%m/%d/%Y")
        logger.info(f"\nStart Date: {start_date} \nEnd Date: {end_date}")

        interval = (end_date - start_date).days
        logger.info(f"Interval: {interval} days")
        return interval
    
    def get_schedule(self):
        interval = self.get_interval()
        schedule = 0

        if interval <= 8:
            schedule = 1 
        if interval >= 8 and interval <= 64:
            schedule = 7 
        if interval >= 64 and interval <= 366:
            schedule = 28 
        
        logger.info(f"Mailing Schedule: {schedule} days")
        return schedule

    def send_mail(self):
        schedule = self.get_schedule()
        begin_date = datetime.strptime(self.begin, "%m/%d/%Y")
        logger.info(f"Begin Date: {begin_date}")
        next_date = begin_date.replace(day=begin_date.day + schedule)
        logger.info(f"First Follow-Up: {next_date}")
        try:
            while True:
                if next_date <= datetime.now():
                    logger.info("Date arrived: Sending emails")
                    self.email()
                    next_date = next_date.replace(day=next_date.day + schedule)

                    logger.info(f"Current Date: {datetime.now()}")
                    logger.info(f"Next Date: {next_date}")
                    time.sleep(schedule * (60 * 60 * 24))
        except Exception as e:
            logger.error(traceback.format_exc())
            
    @app.route("/templates")
    def email(self):
        emails = self.get_emails()
        for email in emails:
            with app.app_context():
                name = email[0]
                email = email[1]
                template = render_template("checkin_template.html", name=name, project_name=self.project_name)

                msg = Message(
                    subject="Follow-Up!",
                    sender="jsurvice@gmail.com",
                    recipients=[email],
                )
                msg.html = template
                try:
                    mail.send(msg)
                    logger.info(f"Email sent to {email}")
                except Exception as e:
                    logger.error(traceback.format_exc())
                    return False

        return True

    @app.route("/record-selection", methods=["POST"])
    def record_selection():
        project_name = request.form["project_value"]
        task = request.form["task_value"].lower() 
        name = request.form["user_value"]

        if task:
            file_path = os.path.join("project_inventory", "test_tasks.json")
            with open(file_path, "r") as f:
                member_data = json.load(f)
            
            due = member_data[project_name]["members"][name][task]["due date"]
            member_data[project_name]["members"][name]["current task"] = task
            member_data[project_name]["members"][name]["CT due date"] = due

            logger.info(f"Selection Recorded: {name} is working on {task} due on {due}")
            with open(file_path, "w") as f:
                json.dump(member_data, f, indent=4)
            return "Thank you for your update!"
        else:
            logger.info("Selection Invalid")
            return "Selection Invalid"

if __name__ == "__main__":
    app.run(debug=True, port = 5001)