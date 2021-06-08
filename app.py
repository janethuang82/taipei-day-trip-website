from codecs import register
from re import S
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session
from flask import jsonify
import mysql.connector
import json

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

app.secret_key = b'\xa8\x90\xba\x9e\x95\xbfh\x15\xee:\x14;'

mydb = mysql.connector.connect(
	host = "127.0.0.1",
	username = "root",
	password = "!123Qqweqwe",
	database = "information"
)

mycursor = mydb.cursor(buffered=True)

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")

@app.route("/booking")
def booking():
	return render_template("booking.html")
	
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


@app.route("/api/attractions")
def attraction_page():
	keyword = request.args.get("keyword", None)	
	if keyword is not None:
		page_id = request.args.get("page", None)
		page_id = int(page_id)
		page_id += 1

		dic_data = {}
		page_range = (page_id - 1)*12

		mycursor.execute(f"SELECT count(id) FROM location where name like '%{keyword}%' ")
		id_number = mycursor.fetchone()
		final_number = id_number [0]
		final_page = final_number//12
		if final_number%12 > 0:
			final_page += 1

		mycursor.execute(f"SELECT * FROM location where name like '%{keyword}%' order by id limit 12 offset {page_range}")
		page_result = mycursor.fetchall()

		page_list = []
		for i in range(len(page_result)):
			id = page_result[i][0]
			name = page_result[i][1]
			category = page_result[i][2]
			description = page_result[i][3]
			address = page_result[i][4]
			transport = page_result[i][5]
			mrt = page_result[i][6]
			latitude = page_result[i][7]
			longitude = page_result[i][8]
			images = page_result[i][9]
			images = images.split(",")
			images.pop()
			images.pop(0)

			dic_detail = {'id':id, 'name':name, 'category':category, 'description':description, 'address': address, 'transport':transport, 'MRT':mrt, 'latitude': latitude, 'longitude': longitude, 'images': images}
			page_list.append(dic_detail)
		
		if page_id > final_page - 1:
			dic_data["nextPage"] = "null"
		else:
			dic_data["nextPage"] = (page_id)
		dic_data["data"] = page_list
		return json.dumps(dic_data, ensure_ascii=False), 200
	else:
		page_id = request.args.get("page", None)
		page_id = int(page_id)
		page_id += 1

		dic_data = {}
		page_range = (page_id - 1)*12

		mycursor.execute(f"SELECT count(*) FROM location")
		id_number = mycursor.fetchone()
		final_number = id_number[0]
		final_page = final_number//12
		if final_number%12 > 0:
				final_page += 1

		mycursor.execute(f"SELECT * FROM location order by id limit 12 offset {page_range}")
		page_result = mycursor.fetchall()

		page_list = []
		for i in range(len(page_result)):
			id = page_result[i][0]
			name = page_result[i][1]
			category = page_result[i][2]
			description = page_result[i][3]
			address = page_result[i][4]
			transport = page_result[i][5]
			mrt = page_result[i][6]
			latitude = page_result[i][7]
			longitude = page_result[i][8]
			images = page_result[i][9]
			images = images.split(",")
			images.pop()
			images.pop(0)

			dic_detail = {'id':id, 'name':name, 'category':category, 'description':description, 'address': address, 'transport':transport, 'MRT': mrt, 'latitude': latitude, 'longitude': longitude, 'images': images}
			page_list.append(dic_detail)
		
		if page_id > final_page - 1:
			dic_data["nextPage"] = "null"
		else:
			dic_data["nextPage"] = (page_id)
		dic_data["data"] = page_list
		return json.dumps(dic_data, ensure_ascii=False), 200

	#return render_template("attraction.html")
@app.route("/api/attraction/<id>")
def attraction_id(id):
    mycursor.execute(f"SELECT * FROM location where id = {id}")
    id_result = mycursor.fetchone()
    dic_data = {}
    if id_result is not None:
    	name = id_result[1]
    	category = id_result[2]
    	description = id_result[3]
    	address = id_result[4]
    	transport = id_result[5]
    	mrt = id_result[6]
    	latitude = id_result[7]
    	longitude = id_result[8]
    	images = id_result[9]
    	images = images.split(",")
    	images.pop()
		# images.pop(0)

    	dic_data["data"] = {'id':id, 'name':name, 'category':category, 'description': description, 'address': address, 'transport': transport, 'MRT':
		mrt, 'latitude':latitude, 'longitude': longitude, 'images':images}
    	return json.dumps(dic_data, ensure_ascii=False), 200
    else:
    	dic_data["data"] = {'error': 'true', 'message': '景點編號不正確'}
    	return json.dumps(dic_data, ensure_ascii=False), 400
        # return render_template("attraction.html")



@app.route("/api/user", methods=["GET"])
def check_user():
	if request.method == "GET":
		print(session)
		if "email" in session:
			return jsonify({"info":{
				"id":session["id"], "name":session["name"], "email":session["email"]}})
		else:
			return jsonify({"info": None})	


@app.route("/api/user", methods=["POST"])
def register_user():
	info = request.get_json()
	print(info)
	print("1")
	name=info["name"]
	email=info["email"]
	password=info["password"]
	print(email)
	mycursor.execute(f"SELECT * FROM register where email = {email}")
	result=mycursor.fetchone()
	print(result)
	try:
		if result:
			return jsonify({"error":True, "message":"此信箱已被註冊過，註冊失敗"}), 400
		else:
			sql="INSERT INTO register(name, email, password) VALUES (%s, %s, %s)"
			val=(name, email, password)
			mycursor.execute(sql, val)
			mydb.commit()
			return jsonify({"ok":True})
	except:
		return jsonify({"error":True, "message":"伺服器內部錯誤"}), 500
    	

@app.route("/api/user", methods=["PATCH"])
def signin_user():
	info=request.get_json()
	email=info["email"]
	password=info["password"]
	print(info)
	mycursor.execute(f"SELECT * FROM register where email = {email} and password = {password}")
	register_result=mycursor.fetchone()
	print(register_result)
	try:
		if register_result:
			session["id"]=register_result[0]
			session["name"]=register_result[1]
			session["email"]=register_result[2]
			print("1")
			return jsonify({"ok":True})
		else:
			print("2")
			return jsonify({"error":True})
	except:
		print("3")
		return jsonify({"error":True, "message":"伺服器內部錯誤"}), 500
    	
@app.route("/api/user", methods=["DELETE"])
def delete_user():
	if "email" in session:
		session.pop("id")
		session.pop("name")
		session.pop("email")
		return jsonify({"ok":True})

app.run(host="0.0.0.0",port=3000)
