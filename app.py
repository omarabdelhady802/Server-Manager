from flask import Flask, render_template, redirect, session, request, jsonify, flash
from flask_moment import Moment
from datetime import datetime
from src import forms, resources
import os
from flask_sqlalchemy import SQLAlchemy
import requests

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# security key for forms
sqlite_db_file=f"{basedir}/database/server_manager.db"
app.config['SECRET_KEY'] = 'AB1997'

# ______________________ sql alchemy config ___________________________
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + sqlite_db_file
# track tables modification
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
moment = Moment(app)

from src import models

login_credentials = {"username": "Ai", "password": "Ai@2023"}

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

@app.template_global()
def logged_in() -> bool:
    return 'logged_in' in session


@app.route('/')
def index():  # put application's code here
    if logged_in():
        all_apps = db.session.query(models.Application).all()
        cpu_percentage = resources.get_cpu_usage()
        print(resources.get_network_activity())
        return render_template("home.html", cpu_percentage=cpu_percentage, memory_data=resources.get_memory_usage(),
                               services=all_apps, current_time=datetime.utcnow())
    else:
        return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        valid_credentials = (login_form.username.data == login_credentials['username'])
        valid_credentials &= (login_form.password.data == login_credentials['password'])
        if valid_credentials:
            session['logged_in'] = True
            flash('You have logged in successfully', category='success')
            return redirect(app.url_for('index'))
        else:
            flash("wrong username or password")

    return render_template('login.html', form=login_form)


@app.route('/app_register', methods=['GET','POST'])
def app_register():
    app_form = forms.Addjob()
    if request.method == 'POST' and len(request.form) != 0:
        try:
            app_name = request.form['app_name']
            port = int(request.form['port'])
            root_dir = request.form['root_dir']
            main_file_name = request.form['main_file_name']
            start_app_bat_pth = request.form['start_app_bat_pth']
            home_page_route = request.form['home_page_route']
            app_description = request.form['app_description']
            photo_path = request.form['photo_path']
            

            app_obj = models.Application(app_name=app_name, app_port=port, app_root_dir= root_dir,
                            main_file_name= main_file_name, start_app_bat_pth= start_app_bat_pth,
                            home_page_route= home_page_route, app_description=app_description,
                            photo_path=photo_path)
            
            db.session.add(app_obj)
            db.session.commit()
            flash(f'You app \'{app_name}\' has been added successfully', category='success')
            return redirect(app.url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred \\{e}\\', category='error')
        
    return render_template('app_register.html', form=app_form)


@app.errorhandler(404)
def page_not_found(e):
    error = str(e) if app.debug else ""
    return render_template('error_pages/404.html', error=error), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error_pages/500.html'), 500


@app.route('/logout')
def logout():
    session.clear()
    flash('You have logged out successfully', category='info')
    return redirect(app.url_for('login'))


# To Be added on the next batch
@app.route('/cpu_usage', methods=['GET'])
def cpu_usage_route():
    cpu_percentage = resources.get_cpu_usage()
    return jsonify(cpu_usage=cpu_percentage)

@app.route('/status/<id>', methods=['GET'])
def get_status(id):
    application = db.session.query(models.Application).filter(models.Application.id == id).first()
    if application :
        try:
            requestt = requests.get(f"http://127.0.0.1:{application.app_port}", timeout=2)
            if requestt.ok:
                return jsonify({"key":"active"})
            else :
                return jsonify({"key":"sleeping"})
        except:
            return jsonify({"key":"port is empty"})
            
    else :
        return jsonify({"key":"app not found"})
    
        
        


# To Be added on the next batch
@app.route('/memory_usage', methods=['GET'])
def memory_usage_route():
    memory_percentage = resources.get_memory_usage()
    return jsonify(memory_usage=memory_percentage)






if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True)
