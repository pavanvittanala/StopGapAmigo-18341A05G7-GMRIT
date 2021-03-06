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
			return jsonify({1:"success"})
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
	if request.method == "POST":
		dd=request.get_json()
		print(dd)
		fullname=dd[0]['name']
		mail=dd[1]['email']
		passcode=dd[2]['passcode']
		location=dd[3]['location']
		mobile=dd[4]['mobile']
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
	E="SELECT * from borrows where mailid!='{0}';".format(session['user'])
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	# print(data)
	return render_template('Feed.html', catalogue=data)


@app.route("/ToBorrow")
def toBorrow():
	return render_template("ToBorrowForm.html")
@app.route("/ToLend")
def toLend():
	return render_template("ToLendForm.html")


@app.route('/MyBorrows')
def Borrow_Individual():
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT * from borrows where mailid='{0}';".format(session['user'])
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	return render_template('Borrows.html', catalogue=data)

@app.route('/MyLends')
def Lend_Individual():
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT * from amigos where from_user='{0}';".format(session['user'])
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	return render_template('Lends.html', catalogue=data)

@app.route('/MyLendStuff')
def LendStuff():
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT * from lends where mailid='{0}';".format(session['user'])
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	return render_template('LendStuff.html', catalogue=data)

@app.route('/Amigos')
def Amigo():
	cur=mysql.new_cursor(dictionary=True)
	E="SELECT * from amigos where from_user='{0}' or to_user='{0}';".format(session['user'])
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	return render_template('Amigos.html',catalogue=data)




@app.route('/lends',methods=['GET','POST'])
def lender():
	if request.method == 'POST':
		dt=request.get_json()
		dt=dt[0]
		E="SELECT unqid from lends where mailid='{0}' and name='{1}' and description='{2}' and location='{3}' and category='{4}';".format(session['user'],dt['prod'],dt['descp'],dt['loc'],dt['categ'])
		cur=mysql.new_cursor(dictionary=True)
		cur.execute(E)
		data=cur.fetchall()
		cur.close()
		if data:
			return jsonify({1:"prod_exists"})
		cur=mysql.new_cursor(dictionary=True)
		E="INSERT INTO lends (name,mailid,location,category,description) VALUES ('{0}','{1}','{2}','{3}','{4}');".format(dt['prod'],session['user'],dt['loc'],dt['categ'],dt['descp'])
		cur.execute(E)
		mysql.connection.commit()
		data=cur.fetchall()
		cur.close()
		print(data)
		return jsonify({1:"success"})
			







@app.route('/borrows',methods=['POST'])
def borrower():
	if request.method == 'POST':
		dt=request.get_json()
		dt=dt[0]
		E="SELECT unqid from borrows where mailid='{0}' and name='{1}' and description='{2}' and location='{3}' and category='{4}' and tender = '{5}';".format(session['user'],dt['prod'],dt['descp'],dt['loc'],dt['categ'],dt['karma_offered'])
		cur=mysql.new_cursor(dictionary=True)
		cur.execute(E)
		data=cur.fetchall()
		cur.close()
		if data:
			return jsonify({1:"prod_exists"})
		print("karma",session['karma'])
		if int(dt['karma_offered']) > int(session['karma']):
			return jsonify({1:"less_karma"})
		cur=mysql.new_cursor(dictionary=True)
		E="INSERT INTO borrows (name,mailid,location,category,description,tender) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}');".format(dt['prod'],session['user'],dt['loc'],dt['categ'],dt['descp'],dt['karma_offered'])
		cur.execute(E)
		mysql.connection.commit()
		data=cur.fetchall()
		cur.close()
		print(data)
		return jsonify({1:"success"})









@app.route('/lending',methods=['POST'])
def borrower_returned():
	dt=request.get_json()
	dt=dt[0]['unqid']
	E="SELECT * from borrows where unqid='{0}'".format(dt)
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	data=cur.fetchall()
	data=data[0]
	cur.close()
	if int(session['karma']) < int(data['tender']):
		return jsonify({1:"failed1"})
	print("data",data)


	E=f"select karma from userdetails where mailid='{ data['mailid'] }';"
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	kk=cur.fetchall()
	kk=kk[0]['karma']
	cur.close()


	karma_update = int(kk) - int(data['tender'])
	if karma_update<0:
		return jsonify({1:"failed2"})
	E=f"UPDATE userdetails SET karma = '{str(karma_update)}' where mailid='{data['mailid']}';"
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	mysql.connection.commit()
	cur.close()

	E="DELETE from borrows where unqid='{0}'".format(dt)
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	mysql.connection.commit()
	cur.close()


	E="INSERT INTO amigos (name,from_user,to_user,status,karmaoffered,idofborrower,location,category) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}');".format(data['name'],session['user'],data['mailid'],"pending",data['tender'],dt,data['location'],data['category'])
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	mysql.connection.commit()
	cur.close()


	karma_update= int(session['karma']) + int(data['tender'])
	session['karma']=str(karma_update)
	E=f"UPDATE userdetails SET karma = '{karma_update}' where mailid='{session['user']}';"
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	mysql.connection.commit()
	cur.close()


	return jsonify({1:"success"})






@app.route('/borrow_status',methods=['POST'])
def status():
	dt=request.get_json()
	if 'amigo' in dt[1]:
		E="SELECT status from amigos where from_user = '{0}' OR to_user = '{0}';".format(session['user'])
	else:
		E="SELECT status from amigos where from_user = '{0}'OR to_user = '{0}';".format(session['user'])
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	print(data)
	if data:
		data=data[0]
		return jsonify({1:data['status']})
	else:
		return jsonify({1:"fail"})



@app.route('/deleteBorrow',methods=['POST'])
def deleteBorrow():
	dt=request.get_json()
	dt=dt[0]
	cur=mysql.new_cursor(dictionary=True)
	E="DELETE from borrows where mailid='{0}' and unqid='{1}';".format(session['user'],dt['unqid'])
	cur.execute(E)
	mysql.connection.commit()
	data=cur.fetchall()
	cur.close()
	print(data)
	return jsonify({1:"success"})




@app.route('/deleteLendStuff',methods=['POST'])
def deleteStuff():
	dt=request.get_json()
	dt=dt[0]
	cur=mysql.new_cursor(dictionary=True)
	E="DELETE from lends where mailid='{0}' and unqid='{1}';".format(session['user'],dt['unqid'])
	cur.execute(E)
	mysql.connection.commit()
	data=cur.fetchall()
	cur.close()
	print(data)
	return jsonify({1:"success"})




@app.route('/mark_returned',methods=['POST'])
def change_status():
	dt=request.get_json()
	dt=dt[0]
	print(dt['unqid'],session['user'])
	E="UPDATE amigos SET status = '{0}' WHERE from_user = '{1}' AND name = '{2}';".format("returned",session['user'],dt['unqid'])
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	mysql.connection.commit()
	data=cur.fetchall()
	cur.close()
	print(data)
	return jsonify({1:"success"})





@app.route('/karma_curr',methods=['POST'])
def curKarms():
	dd=request.get_json()
	E="select karma from userdetails where mailid='{0}';".format(session['user'])
	cur=mysql.new_cursor(dictionary=True)
	cur.execute(E)
	data=cur.fetchall()
	cur.close()
	session['karma']=data[0]['karma']
	return jsonify({1:data[0]['karma'],2:session['user']})



if __name__ == "__main__":
	app.run(debug=1)