from functools import wraps
from flask import Flask, flash, redirect
from flask import render_template, request, url_for, session
from extensions import mysql, mail
from config import Config

from db import DatabaseService
from mail import BirthdayAddReminderEmail

app = Flask(__name__)
app.config.from_object(Config)

mysql.init_app(app)
mail.init_app(app)

dataBaseApi = DatabaseService()

def login_required(func):   
    @wraps(func)
    def wrapper(*args, **kwargs):  
        if session.get('loggedin') is not True:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

@app.route("/remind_me", methods = ['GET', 'POST'])
@login_required
def remind_me():  
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        emailAddReminder = BirthdayAddReminderEmail(session['email'], app)
        emailAddReminder.send(name, date)
        flash('Email sent successfully')
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route("/index" , methods = ['GET', 'POST'])
@login_required
def index():  
    if session.get('loggedin') is not True:
        return redirect(url_for("login"))

    if request.method == 'POST':
        if(request.form['name'] == "" or request.form['date'] == ""):
            flash("Please enter all the fields")
            return render_template("index.html")
        dataBaseApi.insert_birthday(request.form['name'], request.form['date'], session['id'])
        flash('Birthday added successfully')
        return redirect(url_for('index'))

    birthdays = dataBaseApi.get_birthdays(session['id'])
    return render_template("index.html", birthdays = birthdays)


@app.route("/")
@app.route('/login', methods = ['GET', 'POST'])
def login():  
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        account = dataBaseApi.get_account(email, password)
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            birthdays = dataBaseApi.get_birthdays(session['id'])
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg, birthdays = birthdays)
        else:
            msg = 'Incorrect email / password !'
            return render_template("login.html", msg = msg)
    return render_template("login.html")

@app.route('/register', methods = ['GET', 'POST'])
def register():  
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        dataBaseApi.insert_account(email, password)
        flash('You are successfully Registered')
        return redirect(url_for("login"))
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug = True)
