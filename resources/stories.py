import models

#import Blueprint
from flask import Blueprint, request, jsonify

#we need the current user that is logged in to see all the routes
from flask_login import current_user, login_required

#get model as dict
from playhouse.shortcuts import model_to_dict

#story blueprint
stories = Blueprint('stories', 'stories')


#GET /
#get all the stories to put in the index route
#INDEX route 
@stories.route('/', methods=['GET'])
@login_required
def stories_index():
	#all_stories_query = models.Story.select()

	current_user_story_dicts = []

	for story in current_user.stories:
		print(story)
		print(model_to_dict(story))

		#append(push) each story to the list
		current_user_story_dicts.append(model_to_dict(story))
	return jsonify(
		data=current_user_story_dicts,
		message=f"We can see all of the {len(current_user_story_dicts)} stories for {current_user.email}!",
		status=200
	), 200


#CREATE route
#POST /
@stories.route('/', methods=['POST'])
@login_required
def create_stories():
	#we need to get the JSON from the req
	#request.get_json
	payload = request.get_json()
	print(payload)

	story = models.Story.create(
		user_id=current_user.id,
		title=payload['title'], 
		story_content=payload['story_content'], 
		image=payload['image'])

	print(story.__dict__)

	story_dict = model_to_dict(story)

	#we don't need the password information here so we can pop it off the list
	story_dict['user_id'].pop('password')


	return jsonify(
		data=story_dict,
		message="New story was created!",
		status= 201,
	), 201


#UPDATE route
#PUT /<id>
@stories.route('/<id>', methods=['PUT'])
@login_required
def update_story(id):

	#user is only allowed to update their stories
	payload = request.get_json()

	#user story 
	story = models.Story.get_by_id(id)
	print(story)

	#if the story id is the same as the user's story id
	#then they can update their own story
	if story.user_id.id == current_user.id:
		story.title = payload['title'] if 'title' in payload else None
		story.story_content = payload['story_content'] if 'story_content' in payload else None
		story.image = payload['image'] if 'image' in payload else None

		#save the updated story
		story.save()

		story_dict = model_to_dict(story)

		return jsonify(
			data=story_dict,
			message=f"We updated the story with id {id}",
			status=200
		), 200

	#if the story wasn't created by the user that is logged in,
	#then they shouldn't be able to update
	else: 

		return jsonify(
			data= {
			"error": "You cannot update this story"
			},
			message=f"The user story id{story.user_id.id} does not match the current user's id {current_user.id}. User can only update own story",
			status=403
		), 403







#DESTROY route
#DELETE /<id>
#need an id as a param to be able to delete that specific story
@stories.route('/<id>', methods=['Delete'])
def delete_story(id):
	#delete where the storyid = id that you want to delete
	delete_query = models.Story.delete().where(models.Story.id == id)
	#after this we need to execute this
	delete_query.execute()

	return jsonify(
		data={},
		message=f"We are able to delete Story with ID of {id}",
		status=200,
	), 200








