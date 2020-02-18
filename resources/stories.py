import models

#import Blueprint
from flask import Blueprint

#get model as dict
from playhouse.shortcuts import model_to_dict

#story blueprint
stories = Blueprint('stories', 'stories')


#GET /
#index route 
@stories.route('/', methods=['GET'])
def stories_index():
	return "stories index"