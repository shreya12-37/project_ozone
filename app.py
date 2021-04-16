from flask import Flask, render_template, request, jsonify, session 
import json
import re
from db_query import *
from problem import *
from flask_cors import CORS
from codechecker import *
from datetime import datetime

config = {
  'ORIGINS': [
    'http://localhost:3000',  # React
    'http://127.0.0.1:3000',  # React
  ],

  'SECRET_KEY': 'Hello World'
}

app = Flask(__name__)

CORS(app, resources={ r'/*': {'origins': config['ORIGINS']}}, supports_credentials=True)

d1={"status":200, "msg":"OK"}
d2={"status":420, "msg":"ERROR"}

@app.route('/register', methods=['POST'])
def regsiter():
	data = request.get_json()
	#username = data['username']
	#fname = data['fname']
	#lname = data['lname']
	#email_id = data['email_id']
	#password = data['password']
	cpassword = data['cpassword']
	user={"username" : data['username'], "fname": data['fname'], "lname": data['lname'], "email_id": data['email_id'],"password": data['password']}

	regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
	#password should have at least one number
	#one uppercase and one lowercase character
	#one special symbol
	#between 8 to 20 character 

	regex_pass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
	if (re.search(regex_email,user['email_id'])) and (re.search(regex_pass,user['password'])):
		if user['password'] == cpassword:
			code,msg = UserExist(user)
			if code==200:
				d1['msg']="user already registered"
				return jsonify(d1)
			else:
				code,msg=registerUser(user)
				if code==200:
					d1['msg']="registered successfully"
					return jsonify(d1)
				else:
					d2['msg']="error while registering"
					jsonify(d2)
		else:
			d2['msg']="password does not match"
			return jsonify(d2)
	else:
		return jsonify(d2)
		
	
    
@app.route('/login', methods=['post'])
def login():
	data = request.get_json()
	email_id=data['username'] if "username" in data else None 
	password=data['password'] if "password" in data else None
	if email_id==None :
		d2['msg']="email required"
		return jsonify(d2)
	elif password==None:
		d2['msg']="password required"
		return jsonify(d2)
	else:
		user = {'email_id':email_id, "password":password}
		check_status,msg=checkUser(user)
		if check_status==200:
			session['user']= data['username']
			d1['msg']="successfully logged in"
			return jsonify(d1)
		if check_status==420:
			d2['msg']="wrong credentials"
			return jsonify(d2)

@app.route('/practice')
def displayProblems():
	code,result = displayAllProblems()
	if code==200:
		d1['msg']=result
		return jsonify(d1)
	else:
		return jsonify(d2)

@app.route('/practice/<problem_id>', methods=['get'])
def problemdisplay(problem_id):
	code,message=problemInfoDisplay(problem_id)
	if code==200:
		d1['msg']=message
		return jsonify(d1)
	else:
		return jsonify(d2)

@app.route('/contest/past')
def displayPastContest():
	code, res = showPastContest()
	if code==200:
		d1['msg']=res
		return jsonify(d1)
	else:
		return jsonify(d2)

@app.route('/contest/ongoing')
def displayLiveContest():
	code, res = showLiveContest()
	if code==200:
		d1['msg']=res
		return jsonify(d1)
	else:
		return jsonify(d2)

@app.route('/contest/upcoming')
def displayUpcomingContest():
	code, res = showUpcomingContest()
	if code==200:
		d1['msg']=res
		return jsonify(d1)
	else:
		return jsonify(d2)
		
#contest registration 
@app.route('/contest/register')
def registerInContest():
	data = request.get_json()
	username=data['username'] if "username" in data else None 
	d={"username": username, "contest_id": data['contest_id'], "contest_rating":'0',"rank":'0'}
	code,msg=registerInContest(d)
	if code==200:
		d1['msg']="user registered in contest"
		return jsonify(d1)
	else:
		d2['msg']="user not registered for contest"
		return jsonify(d2)

@app.route('/profile')
def profileupdate():
	data = request.get_json()
	cpassword = data['cpassword']
	user={"username" : data['username'],"email_id": data['email_id'],"password": data['password'],"phone_no" : data['phone_no'], "address" : data['address'], "inst_name" : data['inst_name'] }
	regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
	regex_pass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
	if (re.search(regex_email,user['email_id'])) and (re.search(regex_pass,user['password'])):
		if user['password'] == cpassword:
			code,msg= updateProfile(user)
			if code==200:
				d1['msg']="profile details updated successfully"
				return jsonify(d1)
			else:
				d2['msg']="error while updating profile"
				return jsonify(d2)
		else:
			d2['msg']="password and confirm password does not match"
			return jsonify(d2)
	else:
		d2['msg']="error in email or password"
		return jsonify(d2)

@app.route('/products')
def insertingProducts():
	data = request.get_json()
	pr={"product_id": data['product_id'],"product_name": data['product_name'],"price": data['price']}
	code, msg = insertProduct(pr)
	if code==200:
		d1['msg']="product inserted in database"
		return jsonify(d1)
	else :
		return jsonify(d2)

@app.route('/product/<product_id>', methods=['get'])
def displayProductDetails(product_id):
	code,message = displayProduct(product_id)
	if code==200:
		d1['msg']=message 
		return jsonify(d1)
	else:
		d2['msg']="product does not exists"
		return jsonify(d2)

@app.route('/logout')
def logout():
	session.pop('user')
	d1['msg']="cookies of username deleted"
	return jsonify(d1)


if __name__ == '__main__':
	app.run(debug=True)
	
	

		






