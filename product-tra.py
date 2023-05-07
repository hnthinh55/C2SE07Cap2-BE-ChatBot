import json
from flask import Flask
import pyodbc
server = '.'
database = 'NETFarm'
username = 'NETFarm'
password = 'password'
driver = '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';trusted_connection=Yes')
cursor = cnxn.cursor()

query = "SELECT pro.[Name],pro.[PlaceProduce],pro.[Price],pro.[InventoryNumber],pro.[IsAvailable],pro.[Category_ID],img.Url as [ImageURL] FROM [NETFarm].[dbo].[Product] as pro LEFT JOIN (SELECT    ProductId,    MAX(Id) AS MaxImageId FROM  [NETFarm].[dbo].[ProductImage] GROUP BY     ProductId) AS latest_img ON pro.Id = latest_img.ProductId LEFT JOIN [NETFarm].[dbo].[ProductImage] AS img ON latest_img.MaxImageId = img.Id"
cursor.execute(query)

results = cursor.fetchall()
for row in results:
    print(row)

cursor.close()
cnxn.close()
prefixes = ["sản phẩm", "cho tôi thông tin về", "giá của sản phẩm"]
data = []
for result in results:
    data.append({
        "tag": result[0].replace(" ", "_")+'_'+result[1].replace(" ", "_"),
        "patterns": [prefixes[0]+' '+result[0]+' '+result[1], prefixes[1]+' '+result[0]+' '+result[1], prefixes[2]+' '+result[0]+' '+result[1]],
        "responses": ["Thông tin về sản phẩm "+result[0]+":</br>"+"<p>- Nơi sản xuất: "+result[1]+"</p><p>- Giá: "+str(result[2])+" VND</p>"],
        "context": []
    })
for d in data:
    print(d)

root_element = {"intents": data}

with open("./data/product.json", "w") as outfile:
    json.dump(root_element, outfile)

print("Data saved to product.json")