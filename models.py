#python module for interacting with our operating system.
import os

# all our models will go in this file
#need to import datetime for the DateTimeField
import datetime

#import everything from peewee... 
#SqliteDatabase and Model
from peewee import *

#UserMixin is what we need to make our User model
#This provides default implementations 
#for the methods that Flask-Login expects user objects to have.
from flask_login import UserMixin


# a Peewee extension for creating a database connection from a URL string.
from playhouse.db_url import connect


if 'ON_HEROKU' in os.environ:  
                              
  DATABASE = connect(os.environ.get('DATABASE_URL'))  
                                                     
else:
  DATABASE = SqliteDatabase('stories.sqlite')




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
  content = CharField()
  image = CharField()
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
