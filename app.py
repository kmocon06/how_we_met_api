import os

from flask import Flask, jsonify, g

#to access react we need CORS
from flask_cors import CORS

#uses flash to display messages when a user is required to log in
from flask_login import LoginManager

# import blueprints from ./resources/users
from resources.users import users 
# import blueprints from ./resources/stories
from resources.stories import stories


#import models
import models 


DEBUG = True
PORT = 8000

# instantiating the Flask class
app = Flask(__name__) 


# need to set up a secret key
app.secret_key = "Alpacas. Donkeys. Koalas. Zebras."

#instantiate LoginManager to get a login_manager
login_manager = LoginManager()

#connect the app with the login manager
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist: 

		return None

#for people that are unauthorized (not logged in)
@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
		data={
		'error': 'user not logged in'
		},
		message="You are unable to access this. Please login",
		status=401
	), 401


#CORS- Cross Origin Resource Sharing 
#we need this to access our react app
CORS(users, origins=['http://localhost:3000', 'https://how-we-met-app.herokuapp.com'], supports_credentials=True)
CORS(stories, origins=['http://localhost:3000', 'https://how-we-met-app.herokuapp.com'], supports_credentials=True)


#using blueprints-- similar to "controllers"
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(stories, url_prefix='/api/v1/stories')


# we don't want to hog up the SQL connection pool
#connect to the DB before every request
#then close the db connection after every request

@app.before_request 
def before_request():
  # store db as global variable in "g"
	g.db = models.DATABASE
	g.db.connect()


@app.after_request
def after_request(response):

  	g.db.close()
  	return response


#ROUTES 

#GET / 
#index route
@app.route('/')  
def index():
  return 'Homepage'



#for Heroku
if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

#listener
if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT) 