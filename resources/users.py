#import models
import models

#import Blueprint
from flask import Blueprint, request

#user blueprint
users = Blueprint('users', 'users')


#GET /

@users.route('/', methods=['GET'])
def test_user_resource():
  return "testing the user resource here"


#POST /register
@users.route('/register', methods=['POST'])
def register():
  print(request.get_json())
  return "check terminal for request.get_son()"