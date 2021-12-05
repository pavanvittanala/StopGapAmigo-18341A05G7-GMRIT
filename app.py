from flask import Flask, render_template, url_for, request, Response,session
from flask_mysql_connector import MySQL
# from flask_bootstrap import Bootstrap
# from flask_nav import Nav
# from flask_nav.elements import *
# from dominate.tags import img
import os


app=Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'stopgapamigo'
mysql = MySQL(app)
# Bootstrap(app)

app.secret_key="stopgapamigo"
# UPLOAD_FOLDER='./Uploads'


@app.route('/')
def home():
	# session['user']='pavan'
	session.pop('user',None)
	return render_template('Home.html')


@app.route('/user')
def user():
	print(session)
	cur = mysql.new_cursor(dictionary=True)
	cur.execute("select * from userdetails")
	output = cur.fetchall()
	if session:
		print("yes")
	else:
		print("No")
	# return str(output)
	if output:
		print("1",output)
		print(output[0])
	else:
		print("0")
	return render_template('User.html')


@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == "POST":
		mail=request.form['mail']
		passcode=request.form['passcode']
		cur = mysql.new_cursor(dictionary=True)
		E="SELECT * from users where mailid='{0}' and passcode='{1}';".format(mail,passcode)
		cur.execute(E)
		data=cur.fetchall()
		return str(data)
	return "d--d"


@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == 'POST':
		fullname=request.form['name']
		mail=request.form['email']
		passcode=request.form['password']
		mobile=request.form['phno']
		location=request.form['location']
		cur=mysql.new_cursor(dictionary=True)
		E="SELECT * from userdetails where mailid='{0}';".format(mail)
		cur.execute(E)
		data=cur.fetchall()
		print(data)
		if data:
			return "User Already Exists"
		E="INSERT INTO userdetails (fullname,location,mailid,mobile,passcode) VALUES ('{0}','{1}','{2}','{3}','{4}');".format(fullname,location,mail,mobile,passcode)
		cur.execute(E)
		mysql.connection.commit()
		data=cur.fetchall()
		print(data)
		return "Registered Successfully"


@app.route('/lends',methods=['GET','POST'])
def lender():
	if request.method == 'POST':
		mail=request.form['email']
		if session:
			if session['user'] != mail:
				session['user'] = mail
		E="SELECT fullname from userdetails where mailid='{0}';".format(mail)
		cur=mysql.new_cursor(dictionary=True)
		cur.execute(E)
		output=cur.fetchall()
		cur.close()
		if output:
			fullname = output[0]['fullname']
		else:
			fullname = request.form['name']
		category=request.form['category']
		location=request.form['location']
		descp=request.form['description']
		cur=mysql.new_cursor(dictionary=True)
		E="INSERT INTO lends (name,mailid,location,category,description) VALUES ('{0}','{1}','{2}','{3}','{4}');".format(fullname,mail,location,category,descp)
		cur.execute(E)
		mysql.connection.commit()
		data=cur.fetchall()
		print(data)
		if data:
			return "ok"
		return "not ok	"


@app.route('/borrows',methods=['GET','POST'])
def borrower():
	if request.method == 'POST':
		mail=request.form['email']
		if session:
			if session['user'] != mail:
				session['user'] = mail
		E="SELECT fullname from userdetails where mailid='{0}';".format(mail)
		cur=mysql.new_cursor(dictionary=True)
		cur.execute(E)
		output=cur.fetchall()
		cur.close()
		if output:
			fullname = output[0]['fullname']
		else:
			fullname = request.form['name']
		category=request.form['category']
		location=request.form['location']
		descp=request.form['description']
		karmas=request.form['points']
		cur=mysql.new_cursor(dictionary=True)
		E="INSERT INTO lends (name,mailid,location,category,description,tender) VALUES ('{0}','{1}','{2}','{3}','{4}'.'{5}');".format(fullname,mail,location,category,descp,karma)
		cur.execute(E)
		mysql.connection.commit()
		data=cur.fetchall()
		print(data)
		if data:
			return "ok"
		return "not ok	"

@

@app.route
def feed():
	pass


# nav.init_app(app)
if __name__ == "__main__":
	app.run(debug=1)