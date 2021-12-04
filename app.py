from flask import Flask, render_template, url_for, request, Response
from flask_mysql_connector import MySQL
import os,glob

app=Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'sys'
mysql = MySQL(app)

@app.route('/')
def home():
	return render_template('Home.html')

@app.route('/user')
def index():
	cur = mysql.new_cursor(dictionary=True)
	cur.execute("select column_name from information_schema.columns where table_schema='stopgapamigo' and table_name='userdetails'")
	output = cur.fetchall()
	print(type(output))
	return str(output)
	# return render_template('User.html')
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
	return ""

@app.route('/register',methods=['GET','POST'])
def register():
	if request.method == 'POST':
		fullname=request.form['']
		mail=request.form['']
		passcode=request.form['']
		mobile=request.form['']
		location=request.form['']
		cur=mysql.new_cursor(dictionary=True)
		E="SELECT * from users where mailid='{0}' and passcode='{1}';".format(mail,passcode)
		cur.execute(E)
		data=cur.fetchall()

		E="INSERT INTO userdetails (fullname,location,mailid,mobile,passcode) VALUES ('{0}','{1}','{2}','{3}','{4}');".format(fullname,location,mail,mobile,passcode)


if __name__ == "__main__":
	app.run(debug=1)