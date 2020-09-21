from app import app
from flask import render_template,flash,redirect,url_for,request
from flask_login import current_user, login_user,logout_user,login_required
from app.forms import LoginForm,RegistrationForm,EditProfile
from werkzeug.urls import url_parse
from app.models import User,Post
from app import db
from datetime import datetime


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
		return redirect(next_page)
	return render_template('login.html',title = "Sign In",form = form)

@app.route('/register',methods = ["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	form = RegistrationForm()
	try:
		if form.validate_on_submit():
			user = User(username = form.username.data,email = form.email.data)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			flash("Congratulations , You are added now")
			return redirect(url_for("login"))
	except:
		flash("USername or email already exists")
		redirect(url_for("register"))
	flash("Give your details")
	return render_template("register.html",title = "Register Page",form = form)

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username = username).first_or_404()
	posts = [
		{'user_id' : user , "content" : "test post 1"},
		{'user_id' : user , "content" : "test post 2"}
	]
	return render_template('user.html' , user = user, posts = posts)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/edit_profile',methods = ["GET","POST"])
@login_required
def edit_profile():
	form = EditProfile()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash("Your changes have been saved.")
		return redirect(url_for('edit_profile'))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html',title="Edit Profile Page", form = form)

