import urllib.request as request
import json
import mysql.connector


def main():
    
    mydb = mysql.connector.connect(
    host = "127.0.0.1",
    username = "root",
    password = "!123Qqweqwe",
    database = "information"
    )

    mycursor = mydb.cursor()

    doc = "taipei-attractions.json"
    with open (doc, 'r') as response:
        material = json.load(response)
    
    each_data = material["result"]["results"]

    for spot in each_data:

        series_no = spot["_id"]
        name = spot["stitle"]
        category = spot["CAT2"]
        description = spot["xbody"]
        address = spot["address"]
        transport = spot["info"]
        MRT = spot["MRT"]
        latitude = spot["latitude"]
        longitude = spot["longitude"]
        images = spot["file"]
        images = images.split("http")

        website = ''
        for web in images:
            if ".jpg" or ".JPG" or ".PNG" in web:
                website = website + "http" + web + ","
        
        table = "INSERT INTO location (id, name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (series_no, name, category, description, address, transport, MRT, latitude, longitude, website)
        mycursor.execute(table, val)
        mydb.commit()
                
    # src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions.json"
    # with request.urlopen(src) as response:
    #     data = json.load(response)

    # clist = data["result"]["results"]
    # with open("data1.txt", "w", encoding="utf-8") as file:
    #     for location in clist:
    #         file.write(location["stitle"]+","+location["longitude"]+","+location["latitude"]+",")
    #         jpg = location["file"].split('http')
    #         file.write("http"+jpg[1]+"\n")


if __name__ == '__main__':
    main()