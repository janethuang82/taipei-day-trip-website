from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session
import mysql.connector
import json

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

#app.secret_key = 

mydb = mysql.connector.connect(
	host = "127.0.0.1",
	username = "root",
	password = "!123Qqweqwe",
	database = "information"
)

mycursor = mydb.cursor()

# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/attraction/")
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

        dic_data["data"] = {'id':id, 'name':name, 'category':category, 'description': description, 'address': address, 'transport': transport, 'MRT':
		mrt, 'latitude':latitude, 'longitude': longitude, 'images':images}
        return json.dumps(dic_data, ensure_ascii=False), 200
    else:
        dic_data["data"] = {'error': 'true', 'message': '景點編號不正確'}
        return json.dumps(dic_data, ensure_ascii=False), 400
        # return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(port=3000)