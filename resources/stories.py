import models

#import Blueprint
from flask import Blueprint, request

#get model as dict
from playhouse.shortcuts import model_to_dict

#story blueprint
stories = Blueprint('stories', 'stories')


#GET /
#INDEX route 
@stories.route('/', methods=['GET'])
def stories_index():
	return "stories index"


#CREATE route
#POST /
@stories.route('/', methods=['POST'])
def create_stories():
	#we need to get the JSON from the req
	#request.get_json
	payload = request.get_json()
	print(payload)
	return "stories create route"