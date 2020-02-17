# all our models will go in this file
#need to import datetime for the DateTimeField
import datetime

#import everything from peewee... 
#SqliteDatabase and Model
from peewee import *

#like MONGO_DB_URL = 'mongodb://localhost/stories', {...}
DATABASE = SqliteDatabase('stories.sqlite') 


#UserMixin is what we need to make our User model
#This provides default implementations 
#for the methods that Flask-Login expects user objects to have.
from flask_login import UserMixin


#User model for authentication 
# peewee doesn't have some methods and properties for the User  
# so we inherit from UserMixin (in addition to peewee's Model class)
# which will provide/implement them for us
class User(UserMixin, Model):
  name = CharField()
  username = CharField(unique=True) #need a unique username
  email = CharField(unique=True) #need a unique email
  password = CharField()
  created_at = DateTimeField(default=datetime.datetime.now)

  class Meta:
    database = DATABASE


class Story(Model): 
  title = CharField()
  #one to many relationship between users and stories
  user_id = ForeignKeyField(User, backref='stories')
  story_content = CharField()
  image = FileField()
  created_at = DateTimeField(default=datetime.datetime.now)

  #special constructor that gives our class instructions on how to
  #connect to a specific database 
  class Meta:
    database = DATABASE 


#method that gets called in app.py
def initialize():
  DATABASE.connect()
  
  #list of tables to create 
  #this means create tables for user and story only if they don't already exist
  DATABASE.create_tables([User, Story], safe=True)
  print("Connected to DB and created tables if they weren't already there")

  #close the DB connection
  DATABASE.close()
