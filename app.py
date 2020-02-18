from flask import Flask 



#uses flash to display messages when a user is required to log in
from flask_login import LoginManager

# import blueprints from ./resources/users
from resources.users import users 

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


#using blueprints-- similar to "controllers"
app.register_blueprint(users, url_prefix='/api/v1/users')




#ROUTES 

#GET / 
#index route
@app.route('/')  
def index():
  return 'Homepage'



#listener
if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT) 