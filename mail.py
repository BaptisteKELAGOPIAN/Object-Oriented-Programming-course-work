from datetime import datetime, timedelta
from flask_mail import Message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from apscheduler.executors.pool import ThreadPoolExecutor
from extensions import mail

class BirthdayReminderEmail:
    def __init__(self, recipient, app):
        self.app = app
        self.sender = "Birthday Reminder"
        self.recipient = recipient
        self.__executors = {'default': ThreadPoolExecutor(20)}
        self.scheduler = BackgroundScheduler(executors=self.__executors)
        self.scheduler.start()

    def send(self, name):
        with self.app.app_context():
            msg = Message('Birthday Reminder', sender=self.sender, recipients=[self.recipient])
            msg.html = f"<html><body>Hello,<br><br>Today is the birthday of <span style='color: red;'>{name}</span><br>Wish him/her a happy birthday!<br><br>Have a nice day!</body></html>"
            mail.send(msg)

class BirthdayAddReminderEmail(BirthdayReminderEmail):
    def send(self, name, date):
        with self.app.app_context():
            msg = Message(f'Birthday Reminder, you added {name}', sender=self.sender, recipients=[self.recipient])
            msg.html = f"<html><body>Hello,<br><br>You just added to your reminder the birthday of <span style='color: red;'>{name}</span> on <span style='color: blue;'>{date}</span><br>We will send you a reminder on the day of the event.<br><br>Have a nice day!</body></html>"
            mail.send(msg)
            self.scheduler.add_job(self.send_reminder, 'date', run_date=date, args=[self.recipient, name])

    def send_reminder(self, email, name):
        super().send(name)