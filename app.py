from flask import Flask 

import models 


DEBUG = True
PORT = 8000

# instantiating the Flask class
app = Flask(__name__) 

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