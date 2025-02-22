from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login_btn = SubmitField("Login")


class Addjob(FlaskForm):
    new_app_name = StringField("App Name", name='app_name', validators=[DataRequired()])
    
    new_app_port = IntegerField("App Port", name='port', validators=[DataRequired(), NumberRange(0,9999, "Port is out of range")])
    
    new_app_root_dir = StringField("App Root Dir", name='root_dir', validators=[DataRequired()])

    new_main_file_name = StringField("main_file_name", name='main_file_name', validators=[DataRequired()])

    new_start_app_bat_pth = StringField("start_app_bat", name='start_app_bat_pth', validators=[DataRequired()])

    new_home_page_route = StringField("home_page_route",name='home_page_route')

    new_app_description = TextAreaField("Description", name='app_description', render_kw={'col': 2}, validators=[DataRequired()])

    new_photo_path = StringField("Image Path", name='photo_path', validators=[DataRequired()])
    new_job_btn = SubmitField("Login")