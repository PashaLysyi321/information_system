from flask import Flask, redirect, url_for, request, session, render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists, extract, func, update

from setup import user_database, todolist
from forms.forms import SignUpForm, CreateTask, LOGIN, markasdone
from datetime import datetime

import plotly
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pasha'


def connect():

    oracle_connection_string = 'oracle+cx_oracle://{username}:{password}@{host}:{port}/{sid}'

    engine = create_engine( oracle_connection_string.format(

    username="SYSTEM",
    password="oracle",
    sid="XE",
    host="localhost",
    port="1521",
    database="PROJECT",
    ), echo=True)

    Session = sessionmaker(bind=engine)
    sessionn = Session()
    return sessionn

def pie(values1, values2):

    labels = ['Done today','Not done today'] 
    values = [values1, values2]

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3, marker_colors=['rgb(0,255,255)','rgb(64,224,208)'])])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def barplot(values1, values2):

    months = ['The day before yesterday', 'Yesterday', 'Today']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=[values1[0], values1[1], values1[2]],
        name='All',
        marker_color='rgb(0,0,205)'
    ))
    fig.add_trace(go.Bar(
        x=months,
        y=[values2[0], values2[1], values2[2]],
        name='Done',
        marker_color='rgb(65,105,225)'
    ))

    fig.update_layout(barmode='group')

    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route("/", methods = ['GET'])
def hello():
    return render_template('Page0.html')

@app.route("/logorreg", methods = ['GET'])
def hello1():
    return render_template('Page1.html')

@app.route('/registration', methods=["GET", "POST"])
def regis():
    form = SignUpForm()
    if form.is_submitted():
        try:
            sessionn = connect()
            result = request.form
            adddata = user_database(result['user_name'], result['user_mail'], result['user_age'], result['login'], result['user_pass'])
            sessionn.add(adddata)
            sessionn.commit()
            return render_template('confirmIsOkey.html', result = result)

        except:
            result = request.form
            if int(result['user_age']) < 16:
                errors = 1
            elif len(result['login']) <5:
                errors = 2
            elif len(result['user_pass']) <5:
                errors = 3
            else:
                errors = 4

            return render_template('confirmIsNotOkey.html', result = result, errors = errors)
        
    return render_template('registration.html', form = form)

@app.route('/login', methods=["GET", "POST"])
def thisislogin():
    form = LOGIN()
    if form.is_submitted():
        try:
            sessionn = connect()
            result = request.form
            check_log_pass_query = sessionn.query(user_database.id).filter_by(login=result['login'], user_pass=result['user_pass']).scalar()
            if check_log_pass_query:
                session['this_id'] = str(check_log_pass_query)
                return redirect(url_for('mainPanel'))
            else:
                return render_template('error_with_login.html', result = result)
        except:
            result = request.form
            return render_template('error_with_login.html', result = result)

    return render_template('login.html', form = form)

@app.route('/login/main', methods=["GET"])
def mainPanel():
    return render_template('main.html')

@app.route('/show', methods=["GET", "POST"])
def showplanfortodayy():

    sessionn = connect()

    current_datetime = datetime.now().date()
    this_year = current_datetime.year
    this_month = current_datetime.month
    this_day = current_datetime.day
    this_id = session.get('this_id', None)

    stmt = sessionn.query(todolist).filter(todolist.user_id == this_id, todolist.status == 0, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day).order_by(todolist.time_creating).all()
    results=[]
    for row in stmt:
       results.append([row.user_id, row.todolist_name, row.description_of_todo, row.time_creating, row.status])

    form = markasdone()
    if form.is_submitted():
        result = request.form
        adddata = result['my_number']
        if int(adddata) <= len(results) and int(adddata) >= 1:
            updating_task = results[int(adddata)-1]
            update_time = updating_task[3]

            sessionn.query(todolist).filter(todolist.user_id == this_id, todolist.time_creating == updating_task[3]).update({'status': 1})
            sessionn.commit()
            return render_template('refresh.html')
        else:
            return render_template('errors.html', error = 1)
    check = len(results)

    return render_template('showtaskfortoday.html', result = results, check = check)

@app.route('/todo', methods=["GET", "POST"])
def todotask():

    form = CreateTask()
    if form.is_submitted():
        try:
            sessionn = connect()
            result = request.form


            dt = datetime.now().date()
            this_year = dt.year
            this_month = dt.month
            this_day = dt.day
            dtt = datetime.now()
            this_sec = dtt.second
            this_min = dtt.minute
            this_hour = dtt.hour

            errors = -1
            if result['time_creating'][2] != '-' or result['time_creating'][5] !='-' or result['time_creating'][10] !=' ' or result['time_creating'][13] !=':' or result['time_creating'][16] !=':':
                errors = 0
                return render_template('createtaskisNOTOkey.html', result = result, errors = errors)
                

            if int(result['time_creating'][6:10]) < this_year:
                errors = 2
            elif int(result['time_creating'][6:10]) == this_year:
                if int(result['time_creating'][3:5]) < this_month:
                    errors = 2
                elif int(result['time_creating'][3:5]) == this_month:
                    if int(result['time_creating'][0:2]) < this_day:
                        errors = 2
                    elif int(result['time_creating'][0:2]) == this_day:
                        if int(result['time_creating'][11:13]) < this_hour:
                            errors = 2
                        elif int(result['time_creating'][11:13]) == this_hour:
                            if int(result['time_creating'][14:16]) < this_min:
                                errors = 2
                            elif int(result['time_creating'][14:16]) == this_min:
                                if int(result['time_creating'][17:19]) <= this_sec:
                                    errors = 2
            

            if errors != -1:
                return render_template('createtaskisNOTOkey.html', result = result, errors = errors)
            else:
                adddata = todolist(session.get('this_id', None), result['todolist_name'], result['description_of_todo'], result['time_creating'], 0)
                sessionn.add(adddata)
                sessionn.commit()
                return render_template('createtaskisOkey.html', result = result)
        
        except:
            result = request.form
            errors = 1
            return render_template('createtaskisNOTOkey.html', result = result, errors = errors)
        
    return render_template('todo.html', form = form)

@app.route('/settings', methods=["GET", "POST"])
def chart():

    sessionn = connect()

    current_datetime = datetime.now().date()
    this_year = current_datetime.year
    this_month = current_datetime.month
    this_day = current_datetime.day
    this_id = session.get('this_id', None)

    try:

        values_done = len(sessionn.query(todolist).filter(todolist.user_id == this_id, todolist.status == 1, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day).order_by(todolist.time_creating).all())
        values_notdone = len(sessionn.query(todolist).filter(todolist.user_id == this_id, todolist.status == 0, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day).order_by(todolist.time_creating).all())

        checker1 = 0
        checker2 = 0

        if values_done == 0 and values_notdone == 0:
            checker1 = 1
       
        pie_graph = pie(values_done, values_notdone)

        val1 = len(sessionn.query(todolist).filter(todolist.user_id == this_id, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day).all())
        val2 = len(sessionn.query(todolist).filter(todolist.user_id == this_id, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day-1).all())
        val3 = len(sessionn.query(todolist).filter(todolist.user_id == this_id, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day-2).all())
        val4 = len(sessionn.query(todolist).filter(todolist.user_id == this_id, todolist.status == 1, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day).all())
        val5 = len(sessionn.query(todolist).filter(todolist.user_id == this_id, todolist.status == 1, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day-1).all())
        val6 = len(sessionn.query(todolist).filter(todolist.user_id == this_id, todolist.status == 1, extract('YEAR', todolist.time_creating) == this_year, extract('month', todolist.time_creating) == this_month, extract('day', todolist.time_creating) == this_day-2).all())
        bar = barplot([val3, val2, val1], [val6, val5, val4])
        return render_template('usersettings.html', plot1=pie_graph, plot2=bar, checker1=checker1, checker2=checker2)

    except:
        return render_template('usersettings.html', checker1=1)

if __name__ == "__main__":
        app.run(debug = True)