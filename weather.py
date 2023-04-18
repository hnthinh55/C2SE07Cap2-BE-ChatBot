import pymongo
import json
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["StandardDb"]
collection = db["apiweather"]
list_weather = []

for doc in collection.find():
    list_weather.append(doc)
print(list_weather)

prefixes = ["thời tiết hôm nay thế nào", "hôm nay thời tiết như thế nào", "nhiệt độ hôm nay"]
tag = "thời tiết hôm nay"
tagAll = "thời tiết các ngày tới"
prefixes_2= ["thời tiết các ngày tới thế nào", "cho tôi biết thời tiết 7 ngày đến", "nhiệt độ 7 ngày tiếp theo ra sao"]
data = []
kqtmp=""
today = datetime.now()
getToday = datetime.strftime(today, '%d/%m/%Y')
for result in list_weather:
    if getToday == datetime.strftime(result['DateTime'], '%d/%m/%Y'):
        kq = f"<p><strong>Báo cáo thời tiết ngày {datetime.strftime(result['DateTime'], '%d/%m/%Y')} </strong>:</br>-	Tổng quan:{result['Description']} </br>-	Nhiệt độ cao nhất: {result['minTemp']}</br>-	Nhiệt độ thấp nhất: {result['minTemp']} </br>-	Độ ẩm: {result['humidity']}</br>-	Tốc độ gió:{result['wind']} </br>-	Lượng mưa:{result['Rain']} </br></p>"
        data.append({
            "tag": tag.replace(" ", "_"),
            "patterns": [prefixes[0], prefixes[1], prefixes[2]],
            "responses": [kq],
            "context": []
        })
    kqtmp += f"<p><strong>Báo cáo thời tiết ngày {datetime.strftime(result['DateTime'], '%d/%m/%Y')} </strong> :</br>-	Tổng quan:{result['Description']} </br>-	Nhiệt độ cao nhất: {result['minTemp']} độ C</br>-	Nhiệt độ thấp nhất: {result['minTemp']} độ C</br>-	Độ ẩm: {result['humidity']}%</br>-	Tốc độ gió:{result['wind']} m/s</br>-	Lượng mưa:{result['Rain']} mm</br></p>"

data.append({
        "tag": tagAll.replace(" ", "_"),
        "patterns": [prefixes_2[0], prefixes_2[1], prefixes_2[2]],
        "responses": [kqtmp],
        "context": []
    })
root_element = {"intents": data}

with open("./data/weather.json", "w") as outfile:
    json.dump(root_element, outfile)

print("Data saved to weather.json")