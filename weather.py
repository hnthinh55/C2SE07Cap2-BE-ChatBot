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
data = []
today = datetime.now()
getToday = datetime.strftime(today, '%d/%m/%Y')
for result in list_weather:
    if getToday == datetime.strftime(result['DateTime'], '%d/%m/%Y'):
        kq = f"<h3>báo cáo thời tiết</h3><table><tr><th>Tổng quan thời tiết</th><td>{result['Description']}</td></tr><tr><th>Ngày</th><td>{datetime.strftime(result['DateTime'], '%d/%m/%Y')}</td></tr><tr><th>Nhiệt độ thấp nhất</th><td>{result['minTemp']} độ C</td></tr><tr><th>Nhiệt độ cao nhất</th><td>{result['maxTemp']} độ C</td></tr><tr><th>Độ ẩm</th><td>{result['humidity']}%</td></tr><tr><th>Tốc độ gió</th><td>{result['wind']} m/s</td></tr><tr><th>Lượng mưa</th><td>{result['Rain']} mm</td></tr></table>"
        data.append({
            "tag": tag.replace(" ", "_"),
            "patterns": [prefixes[0], prefixes[1], prefixes[2]],
            "responses": [kq],
            "context": []
        })
for d in data:
    print(d)
root_element = {"intents": data}

with open("./data/weather.json", "w") as outfile:
    json.dump(root_element, outfile)

print("Data saved to weather.json")