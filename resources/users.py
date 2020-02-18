#import models
import models

#import Blueprint
from flask import Blueprint, request, jsonify

#import generate_password_hash
from flask_bcrypt import generate_password_hash, check_password_hash

from flask_login import login_user

#get model as dict
from playhouse.shortcuts import model_to_dict

#user blueprint
users = Blueprint('users', 'users')


#GET /

@users.route('/', methods=['GET'])
def test_user_resource():
  return "testing the user resource here"


#POST /register
@users.route('/register', methods=['POST'])
def register():
	payload = request.get_json()
	print(payload)

  	#make it so that emails and usernames will be changed to lowercase
  	#no matter what the user inputs
	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()  
	print(payload)


	try:
    #if the user exists:

    	#they should not be able to register
		models.User.get(models.User.email == payload['email'])
    	#the error ("models.DoesNotExist exception") if they don't already exist

    	#if that query doesn't cause that error, then the email is taken
		return jsonify(
			data={},
			message="A user with that email already exists",
			status=401
		), 401 

	except models.User.DoesNotExist:

		try:
			#they should not be able to register
			models.User.get(models.User.username == payload['username'])
			#the error ("models.DoesNotExist exception") if they don't already exist

    		#if that query doesn't cause that error, then the username is taken

			return jsonify(
				data={},
				message="A user with that username already exists",
				status=401
			), 401


		# but if we get the error, then user is not found, ("DoesNotExist"), so
		# that means we can go ahead and register them
		except models.User.DoesNotExist: 

			#we are able to create user
			created_user = models.User.create(
				name=payload['name'],
				username=payload['username'],
				email=payload['email'],
				password=generate_password_hash(payload['password'])
			)

			#user will now be in session
			login_user(created_user)

			#need to implement model to dict for user
			user_dict = model_to_dict(created_user)
			print(user_dict)

			#password type is "bytes" and it is unserializable
			#we should just .pop() the password and remove it
			user_dict.pop('password')


			return jsonify(
				data=user_dict,
				message=f"Successfully registered {user_dict['email']}",
				status=201
			), 201

#login route
#POST /

@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()

	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()  

	try: 
    #we need the user's email
		user = models.User.get(models.User.email == payload['email'])

		user_dict = model_to_dict(user)

		#check password using bcrypt
		#first is the encrypted password we are checking
		#second is the user input
		password_is_good = check_password_hash(user_dict['password'], payload['password'])

		if password_is_good: 
		#if the password is gooof then we can login the user
		#user is in session if password is correct
			login_user(user)

			user_dict.pop('password')

			return jsonify(
				data=user_dict,
				message="{} is currently logged in".format(user_dict['email']),
				status=200
				), 200

		else: 
			print('password invalid')

			return jsonify(
				data={},
				message="Email or password is incorrect", 
				status=401
			), 401


	except models.DoesNotExist: 
		print('username invalid') 
		return jsonify(
			data={},
			message="Email or password is incorrect", 
			status=401
		), 401



