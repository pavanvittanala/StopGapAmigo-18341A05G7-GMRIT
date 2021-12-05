from flask import Flask, render_template, url_for, request, Response, session, jsonify
from flask_mysql_connector import MySQL
import os



app=Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'stopgapamigo'
mysql = MySQL(app)
app.secret_key="stopgapamigo"





@app.route('/')
def home():
	session.pop('user',None)
	return render_template('Home.html',qry=0)
@app.route('/signing')
def user():
	return render_template('Signing.html')








@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == "POST":
		dd=request.get_json()
		print(dd)
		mail=dd[0]['email']
		passcode=dd[1]['passcode']
		cur = mysql.new_cursor(dictionary=True)
		E="SELECT * from userdetails where mailid='{0}' and passcode='{1}';".format(mail,passcode)
		cur.execute(E)
		data=cur.fetchall()
		print(data)
		if data:
			session['user']=data[0]['mailid']
			session['karma']=data[0]['karma']
			return jsonify([{1:"success"},{2:"saradha"}])
		else:
			return jsonify({0:"failed"})
@app.route('/logout')
def logout():
	session.pop('user',None)
	session.pop('karma',None)
	return render_template('Home.html',qry=1)







@app.route('/check_user',methods=['POST'])
def check():
	dd=request.get_json()
	mail=dd[0]['email']
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT * from userdetails where mailid='{0}';".format(mail)
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	if data:
		return jsonify({1:"exists"})
	else:
		return jsonify({1:"Not exists"})









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
			return jsonify({1:"exists"})
		E="INSERT INTO userdetails (fullname,location,mailid,mobile,passcode) VALUES ('{0}','{1}','{2}','{3}','{4}');".format(fullname,location,mail,mobile,passcode)
		cur.execute(E)
		mysql.connection.commit()
		data=cur.fetchall()
		print(data)
		return jsonify({1:"success"})







@app.route('/HomeFeed')
def Home_feed():
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT * from borrows;"
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	return render_template('Feed.html', catalogue=data)





@app.route('/Borrows')
def Borrow_Individual():
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT * from borrows where mailid='{0}';".format(session['user'])
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	return render_template('Borrows.html', catalogue=data)

@app.route('/Lends')
def Lend_Individual():
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT * from lends where mailid='{0}';".format(session['user'])
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	return render_template('Lends.html', catalogue=data)






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
			return jsonify({1:"success"})
		else:
			return jsonify({0:"failed"})
			







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
		E="INSERT INTO borrows (name,mailid,location,category,description,tender) VALUES ('{0}','{1}','{2}','{3}','{4}'.'{5}');".format(fullname,mail,location,category,descp,karma)
		cur.execute(E)
		mysql.connection.commit()
		data=cur.fetchall()
		print(data)
		if data:
			return jsonify({1:"success"})
		else:
			return jsonify({1:"failed"})








@app.route('/lending',methods=['POST'])
def borrower_returned():
	dt=request.get_json()
	






	name=request.form['name']
	from_user=request.form['user_from']
	to_user=request.form['user_to']
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT tender FROM borrows where name='{0}' and mailid='{1}'".format(name,to_user)
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	data=data[0]
	karmas=data['tender']
	cur=mysql.new_cursor(dictionary=True)
	E="INSERT INTO amigos (name,from_user,to_user,status,karmaoffered) VALUES ('{0}','{1}','{2}','{3}','{4}');".format(name,from_user,to_user,"pending",karmas)
	cur.execute(E)
	data=cur.fetchall()
	print(data)



@app.route('/karma_curr',methods=['POST'])
def curKarms():
	dd=request.get_json()
	E="select karma from userdetails where mailid='{0}';".format(session['user'])
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	session['karma']=data[0]['karma']
	return jsonify({1:data[0]['karma']})



if __name__ == "__main__":
	app.run(debug=1)