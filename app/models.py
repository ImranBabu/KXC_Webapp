from app import db
from app import login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash


class User(UserMixin,db.Model):
	id = db.Column(db.Integer ,primary_key = True)
	username = db.Column(db.String(80),index= True , unique = True)
	email = db.Column(db.String(150),index = True , unique = True)
	password_hash = db.Column(db.String(100))
	posts = db.relationship('Post',backref = 'author',lazy = 'dynamic')

	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return '<User {} Email {}>'.format(self.username,self.email)

class Post(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	content = db.Column(db.String(200))
	timestamp = db.Column(db.DateTime,index = True,default = datetime.utcnow)
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Posted {} by {}'.format(self.content,self.user_id)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))