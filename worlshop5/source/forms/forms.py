from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateTimeField

class SignUpForm(FlaskForm):
    
    user_name = StringField("user_name: ")
    user_mail = StringField("user_mail: ")  
    user_age = StringField("user_age: ")
    login = StringField("login: ")
    user_pass = PasswordField("password: ")
    submit = SubmitField("OK")

class CreateTask(FlaskForm):
    
    user_id = IntegerField("user_id of your user: ")
    todolist_name = StringField("todolist_name: ")
    description_of_todo = TextAreaField("description: ")
    time_creating = DateTimeField("time: ")
    submit = SubmitField("OK")

class LOGIN(FlaskForm):
    
    login = StringField("login: ")
    user_pass = PasswordField("password: ")
    submit = SubmitField("OK")

class markasdone(FlaskForm):
    
    my_number = StringField("№: ")
    submit = SubmitField("OK")