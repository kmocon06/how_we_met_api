#import models
import models

#import Blueprint
from flask import Blueprint

#user blueprint
users = Blueprint('users', 'users')


#GET /

@users.route('/', methods=['GET'])
def test_user_resource():
  return "testing the user resource here"