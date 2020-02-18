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
#get all the stories to put in the index route
#INDEX route 
@stories.route('/', methods=['GET'])
def stories_index():
	all_stories_query = models.Story.select()

	stories_dicts = []

	for story in all_stories_query:
		print(story)
		print(model_to_dict(story))

		#append(push) each story to the list
		stories_dicts.append(model_to_dict(story))
	return jsonify(
		data=stories_dicts,
		message=f"We can see all of the {len(stories_dicts)}stories!",
		status=200
	), 200


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





