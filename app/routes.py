from app import app
from flask import render_template,flash,redirect,url_for,request
from flask_login import current_user, login_user,logout_user,login_required
from app.forms import LoginForm
from werkzeug.urls import url_parse
from app.models import User,Post


@app.route('/')
@app.route('/index')
@login_required
def index():
    #python = {"Trainer" : "Imran","Cooridnator" : "Parthiban"}
    Courses = ["Python", "AWS" , "Go Lang"]
    return render_template('index.html',title_page = "KXC",courses = Courses,messages = "Message is passed")
    #return render_template('index.html',python = python)

@app.route('/login',methods = ["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.verify_password(form.password.data):
			flash("Invalid username or Password")
			return redirect(url_for("login"))		
		login_user(user,remember = form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '' :
			flash("Welcome {} , your email {}".format(form.username.data,form.remember_me.data))
			next_page = url_for('index')
		return redirect(url_for(next_page))
	return render_template('login.html',title = "Sign In",form = form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))