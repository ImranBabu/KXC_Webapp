from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField , SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember_me = BooleanField("Remember Me")
	submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
	username = StringField("Username",validators=[DataRequired()])
	email = StringField("Email",validators = [DataRequired(),Email()])
	password = PasswordField("Password",validators = [DataRequired()])
	password2 = PasswordField("Confirm Password",validators = [DataRequired() , EqualTo('password')])
	submit = SubmitField("Register")



	def validate_username(self,username):
		user = User.query.filter_by(username = username.data).first()
		if user is not None:
			raise ValidationError("Username Already Exists use Different Username")
	
	def validate_email(self,email):
		user = User.query.filter_by(email = email.data).first()
		if user is not None:
			raise ValidationError("Email Already Exists use Different Email")

class EditProfile(FlaskForm):
	username = StringField('Username',validators=[DataRequired()])
	about_me = TextAreaField("About Me", validators = [Length(min = 0, max = 250)])
	submit = SubmitField("Submit")