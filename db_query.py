import psycopg2
import json
import datetime 
from psycopg2.extras import RealDictCursor
import base64

def connect():
	try:
		connection = psycopg2.connect(user="postgres",
			dbname="project",
			password="shreya12",
			host="127.0.0.1",
			port="5432")
		return 200, connection
	except:
		return 420, "connection error"

#adding details to database

def registerUser(user):
	print("enter")
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Coneection error"
		cursor = connection.cursor()
		cursor.execute("INSERT INTO users (username,fname,lname,email_id,password) Values (%s,%s,%s,%s,crypt(%s,gen_salt('bf')))", (user['username'],user['fname'],user['lname'],user['email_id'],user['password']))
		if (connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return 200, "OK"
	except (Exception, psycopg2.Error) as error:
		return 420, error

def checkUser(user):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Coneection error"
		cursor = connection.cursor()
		cursor.execute("SELECT username,email_id,password FROM users WHERE (email_id=%s OR username=%s) AND password=crypt(%s, password)",(user['email_id'],user['email_id'],user['password']))
		record = cursor.fetchall()
		if(connection):
			cursor.close()
			connection.close()
		if len(record) == 0:
			return 420, "empty"
		return 200, record[0]
	except (Exception, psycopg2.Error) as error:
		return 420, error

def UserExist(user):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Coneection error"
		cursor = connection.cursor()
		cursor.execute("SELECT username,email_id FROM users WHERE email_id=%s OR username=%s ",(user['email_id'],user['username']))
		record = cursor.fetchall()
		if(connection):
			cursor.close()
			connection.close()
		if len(record) == 0:
			return 420, "empty"
		return 200, record[0]
	except (Exception, psycopg2.Error) as error:
		return 420, error

def displayAllProblems():
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Connection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		cursor.execute("SELECT * FROM problem")
		record = cursor.fetchall()
		if(connection):
			cursor.close()
			connection.close()
		if len(record) == 0:
			return 420, "error"
		return 200, record
	except (Exception, psycopg2.Error) as error:
		return 420, error


def problemInfoDisplay(problem_id):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Coneection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		cursor.execute("SELECT problem.problem_title,problem.difficulty_level,problem.coins,problem.prob_desc,testcase.testcase_id,testcase.input,testcase.output FROM problem FULL JOIN testcase ON problem.problem_id= testcase.problem_id WHERE problem_id=%s and testcase.ishidden=False",(problem_id,))
		record = cursor.fetchall()
		if(connection):
			cursor.close()
			connection.close()
		if len(record) == 0:
			return 420, "problem does not exist"
		return 200, record
	except (Exception, psycopg2.Error) as error:
		return 420, error
		
def insertingInSolve(d):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Connection error"
		cursor = connection.cursor()
		cursor.execute("INSERT INTO solve (username,problem_id,verdict) Values (%s,%s,%s)", (d['username'],d['problem_id'],d['verdict']))
		if (connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return 200, "OK"
	except (Exception, psycopg2.Error) as error:
		return 420, error

def allTestcase(problem_id):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Connection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		cursor.execute("SELECT * FROM testcase WHERE problem_id=%s",(problem_id,))
		record = cursor.fetchall()
		if (connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return 200, record
	except (Exception, psycopg2.Error) as error:
		return 420, error

def showPastContest():
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Connection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		now = datetime.datetime.now()
		cursor.execute("SELECT * FROM contest WHERE %s>end_time",(now,))
		record = cursor.fetchall() 
		for i in record:
			i["cont_image"]=str(base64.b64encode(i["cont_image"]))
			if (connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")
			if len(record)==0:
				return 420, "0 records"
			return 200, record
	except (Exception, psycopg2.Error) as error:
		return 420, error

		
def showLiveContest():
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Connection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		now = datetime.datetime.now()
		cursor.execute("SELECT * FROM contest WHERE %s>=start_time and %s<end_time",(now,))
		record = cursor.fetchall() 
		for i in record:
			i["cont_image"]=str(base64.b64encode(i["cont_image"]))
			if (connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")
			if len(record)==0:
				return 420, "0 records"
			return 200, record
	except (Exception, psycopg2.Error) as error:
		return 420, error

		

def showUpcomingContest():
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Connection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		now = datetime.datetime.now()
		cursor.execute("SELECT * FROM contest WHERE start_time>%s",(now,))
		record = cursor.fetchall() 
		for i in record:
			i["cont_image"]=str(base64.b64encode(i["cont_image"]))
			if (connection):
				cursor.close()
				connection.close()
				print("PostgreSQL connection is closed")
			if len(record)==0: 
				return 420, "0 records"
			return 200, record
	except (Exception, psycopg2.Error) as error:
		return 420, error
		
#inserting contest registration details in participate table
def registerInContest(d):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Coneection error"
		cursor = connection.cursor()
		cursor.execute("INSERT INTO participate (username,contest_id,contest_rating,rank) Values (%s,%s,%s,%s)", (d['username'],d['contest_id'],d['contest_rating'],d['rank']))
		if (connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return 200, "OK"
	except (Exception, psycopg2.Error) as error:
		return 420, error

#updateing user details in database 
def updateProfile(user):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Coneection error"
		cursor = connection.cursor()
		cursor.execute("UPDATE users SET (username,email_id,phone_no,address,inst_name,password) Values (%s,%s,%s,%s,%s,crypt(%s,gen_salt('bf'))", (user['username'],user['email_id'],user['phone_no'],user['address'],user['inst_name'],user['password']))
		if (connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return 200, "OK"
	except (Exception, psycopg2.Error) as error:
		return 420, error

def insertProduct(pr):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "Connection error"
		cursor = connection.cursor()
		cursor.execute("INSERT INTO product (product_id,product_name,price) Values (%s,%s,%s)", (pr['product_id'],pr['product_name'],pr['price']))
		if (connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return 200, "OK"
	except (Exception, psycopg2.Error) as error:
		return 420, error

def displayProduct(product_id):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "connection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		cursor.execute("SELECT * FROM product WHERE product_id=%s",(product_id,))
		record = cursor.fetchall()
		for i in record:
			i['price']=str(i['price'])
			if(connection):
				cursor.close()
				connection.close()
			if len(record) == 0:
				return 420, "problem does not exist"
			return 200, record
    except (Exception, psycopg2.Error) as error:
    	return 420, error

def coinsUpdate(problem_id,username):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "connection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		cursor.execute("UPDATE users SET u_coins=u_coins + (SELECT coins FROM problem WHERE problem_id=%s) WHERE username=%s",(problem_id,username,))
		if (connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return 200, "OK"
	except (Exception, psycopg2.Error) as error:
		return 420, error

def coinsUpdateOnPurchase(redeem_coins):
	try:
		status, connection = connect()
		if status == 420:
			return 420, "connection error"
		cursor = connection.cursor(cursor_factory=RealDictCursor)
		cursor.execute("UPDATE users SET (u_coins=u_coins-redeem_coins) Values(%s)",(redeem_coins,))
		if (connection):
			connection.commit()
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")
		return 200, "OK"
	except (Exception, psycopg2.Error) as error:
		return 420, error


if __name__=="__main__":
	print("connected")
	usr = {"username" : "xyr", "fname": "xyz", "lname": "hyt", "email_id":"wvsdtf@gmail.com","password":"ajhw45"}
	code,res=registerUser(usr)
	print(code,res)
	


