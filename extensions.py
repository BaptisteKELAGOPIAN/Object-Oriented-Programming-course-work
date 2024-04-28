from flask import Flask
from flask_mail import Mail
from flask_mysqldb import MySQL

mysql = MySQL()
mail = Mail()

def init_app(app):
    mysql.init_app(app)
    mail.init_app(app)
