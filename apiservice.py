import pymongo
import pyodbc
import json

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["StandardDb"]
collection = db["apiweather"]
list_weather = []

for doc in collection.find():
    list_weather.append(doc)

server = 'MSI\SQLEXPRESS'
database = 'NETFarm'
username = 'NETFarm'
password = 'password'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';trusted_connection=Yes')
cursor = cnxn.cursor()

query = "SELECT TOP (1000) [Id] ,[StandardName],[MinTemp],[MaxTemp],[MinHumidity],[MaxHumidity],[Wind],[MaxRain],[Season] FROM [NETFarm].[dbo].[Standard]"
cursor.execute(query)

list_objects = []

results = cursor.fetchall()
for row in results:
    obj = {
        "Id": row[0],
        "StandardName": row[1],
        "MinTemp": row[2],
        "MaxTemp": row[3],
        "MinHumidity": row[4],
        "MaxHumidity": row[5],
        "Wind": row[6],
        "MaxRain": row[7],
        "Season": row[8]
    }
    list_objects.append(obj)

query_advice = "SELECT TOP (1000) [Id],[Description],[StageId],[StandardId] FROM [NETFarm].[dbo].[Advice]"
cursor.execute(query_advice)
list_advice = []

advices = cursor.fetchall()
for row in advices:
    obj = {
        "Id": row[0],
        "Description": row[1],
        "StageId": row[2],
        "StandardId": row[3]
    }
    list_advice.append(obj)

query_stages = "SELECT TOP (1000) [Id],[StageName] FROM [NETFarm].[dbo].[Stage]"
cursor.execute(query_stages)
list_stages = []

stages = cursor.fetchall()
for row in stages:
    obj = {
        "Id": row[0],
        "StageName": row[1],
    }
    list_stages.append(obj)


def ChamSoc(loaicay, stageIndex):
    st = next((x for x in results if x["StandardName"] == loaicay), None)
    des = next((x for x in list_advice if x["Standardid"] == loaicay and x["StageId"] == stageIndex), None)
    prefixes = ["Cách", "Trong giai đoạn", "Tư vấn cho tôi về"]
    data = []
    for result in results:
        data.append({
            "tag": result[0].replace(" ", "_")+'_'+result[1].replace(" ", "_"),
            "patterns": [prefixes[0]+' '+list_stages[stageIndex]["StageName"]+' '+loaicay, prefixes[1]+' '+list_stages[stageIndex]["StageName"]+' '+loaicay, prefixes[2]+' '+list_stages[stageIndex]["StageName"]+' '+loaicay],
            "responses": [{loaicay.lower()} +' trong giai đoạn này bạn nên: '+' '+{des["Description"]}],
            "context": []
        })
    for d in data:
        print(d)

    root_element = {"intents": data}

    with open("service.json", "w") as outfile:
        json.dump(root_element, outfile)    
    return "Data saved to output.json"


def GetResult(loaicay, name):
    checkStage = _context.Stages.SingleOrDefault(lambda st: st.StageName == name)

    if checkStage is not None:
        if checkStage.StageName == "Gieo Trồng":
            api1 = TrongTrot(loaicay, checkStage.Id)
            return api1
        if checkStage.StageName == "Nảy mầm Cây con":
            return CayCon(loaicay, checkStage.Id)
        if checkStage.StageName == "Chăm sóc thường xuyên":
            return ChamSoc(loaicay, checkStage.Id)
        if checkStage.StageName == "Thu hoạch":
            return ThuHoach(loaicay, checkStage.Id)
    return api