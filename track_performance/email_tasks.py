import os
import logging
import traceback
import json
from flask import Flask, render_template, request, Response
from flask.views import View
from flask_mail import Mail, Message
from markupsafe import Markup

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



class EmailTasks:
    def __init__(self, project_name, receivers):
        file_path = os.path.join("project_inventory", "test_tasks.json")
        with open(file_path, "r") as f:
            data = json.load(f)
        
        self.members = data[project_name]["members"]
        self.receivers = receivers
        self.project_name = project_name

    def get_emails(self):
        emails = []
        for name in self.receivers:
            for member in self.members:
                if name in member:
                    email = self.members[member]["email"]
                    emails.append((name, email))
        
        return emails
    
    def set_priority(self, priority):
        if priority == "high":
            return "URGENT"
        if priority == "medium":
            return "Necessary"
        if priority == "low":
            return "Desired"
        
    def attach_task_info(self, task, priority, due):
        return render_template("tasks.html", task=task, priority=priority, due=due)
    
    def get_tasks(self, member):
        tsk_temp_complete = []
        tasks = self.members[member]
        for i, task in enumerate(tasks):
            if i > 2:
                priority = self.set_priority(tasks[str(task)]["priority"])
                due = tasks[str(task)]["due date"]
                html_task = Markup(self.attach_task_info(task, priority, due))
                tsk_temp_complete.append(html_task)
        
        logger.info("Tasks sent to template")
        return tsk_temp_complete
    
    @app.route("/templates")
    def send_mail(self):
        with app.app_context():
            emails  = self.get_emails()
            for email in emails:
                name = email[0]
                task_buttons = self.get_tasks(name)
                email = email[1]
                template = render_template("email_template.html", name=name, task_buttons = task_buttons, project_name=self.project_name)

                msg = Message(
                    subject=f"{self.project_name} Update!",
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
        task = request.form["task_value"]
        name = request.form["user_value"]
        due = request.form["due_value"]

        if task:
            print(f"Selection Recorded: {name} is working on {task} due on {due}")
            print("Saving Selection")
            file_path = os.path.join("project_inventory", "test_tasks.json")
            with open(file_path, "r") as f:
                member_data = json.load(f)
            member_data[project_name]["members"][name]["current task"] = task
            member_data[project_name]["members"][name]["CT due date"] = due
            with open(file_path, "w") as f:
                json.dump(member_data, f, indent=4)
            return "Thank you for your selection!"
        else:
            print("Selection Invalid")
            return "Selection Invalid"


        
if __name__ == '__main__':
    #Run: python -m flask run --host=0.0.0.0 --port=5000 
    app.run(debug=True, port=5000)