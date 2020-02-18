import models

#import Blueprint
from flask import Blueprint, request, jsonify

#we need the current user that is logged in to see all the routes
from flask_login import current_user

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

	story = models.Story.create(user_id=current_user.id,title=payload['title'], 
		story_content=payload['story_content'], image=payload['image'])

	print(story.__dict__)

	story_dict = model_to_dict(story)

	#we don't need the password information here so we can pop it off the list
	story_dict['user_id'].pop('password')


	return jsonify(
		data=story_dict,
		message="New story was created!",
		status= 201,
	), 201





