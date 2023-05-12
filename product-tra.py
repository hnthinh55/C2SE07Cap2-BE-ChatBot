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
list_category = {}
query = "SELECT pro.[Name],pro.[PlaceProduce],pro.[Price],pro.[InventoryNumber],pro.[IsAvailable],pro.[Category_ID],img.Url as [ImageURL], pro.Unit FROM [NETFarm].[dbo].[Product] as pro LEFT JOIN (SELECT    ProductId,    MAX(Id) AS MaxImageId FROM  [NETFarm].[dbo].[ProductImage] GROUP BY     ProductId) AS latest_img ON pro.Id = latest_img.ProductId LEFT JOIN [NETFarm].[dbo].[ProductImage] AS img ON latest_img.MaxImageId = img.Id"
cursor.execute(query)
results = cursor.fetchall()
query = "SELECT TOP (1000) [CategoryId],[Display],[CategorySlug] FROM [NETFarm].[dbo].[Category]"
cursor.execute(query)
results2 = cursor.fetchall()
for row in results2:
    list_sp=[]
    for row2 in results:
        if row[0] == row2[5]:
            list_sp.append(row2)
    list_category[row[1]] = list_sp
cursor.close()
cnxn.close()
def Thong_tin_sp():
    prefixes = ["sản phẩm", "cho tôi thông tin về", "giá của sản phẩm"]
    data = []
    for result in results:
        data.append({
            "tag": result[0].replace(" ", "_")+'_'+result[1].replace(" ", "_"),
            "patterns": [prefixes[0]+' '+result[0]+' '+result[1], prefixes[1]+' '+result[0]+' '+result[1], prefixes[2]+' '+result[0]+' '+result[1]],
            "responses": ["Thông tin về sản phẩm "+result[0]+":</br>"+"<p>- Nơi sản xuất: "+result[1]+"</p><p>- Giá: "+str(result[2])+" VND</p>"+"<p>- Số lượng hàng hóa:" + str(result[3])+ result[7]+"</p>"],
            "context": []
        })
    for d in data:
        print(d)

    root_element = {"intents": data}

    with open("./data/product.json", "w") as outfile:
        json.dump(root_element, outfile)

    print("Data saved to product.json")
k= Thong_tin_sp()
print(k)

def Thong_tin_category_sp():
    prefixes = ["các sản phẩm", "cho tôi thông tin về", "loại sản phẩm"]
    data = []
    for result in list_category:
        lis_item="<p>Đây là danh sách các sản phẩm"+result+" có trong cửa hàng chúng tôi: </p>"
        for item in list_category[result]:
            output="<p><strong>"+item[0]+":</strong></p>"+"<p>- Nơi sản xuất: "+item[1]+"</p><p>- Giá: "+str(item[2])+" VND</p>"+"<p>- Số lượng hàng hóa:" + str(item[3])+ item[7]+"</p>"
            lis_item= lis_item + output
        data.append({
            "tag": result.replace(" ", "_"),
            "patterns": [prefixes[0]+' '+result, prefixes[1]+' '+result, prefixes[2]+' '+result],
            "responses": [lis_item],
            "context": []
        })
    for d in data:
        print(d)

    root_element = {"intents": data}

    with open("./data/category.json", "w") as outfile:
        json.dump(root_element, outfile)

    print("Data saved to category.json")
k1= Thong_tin_category_sp()
print(k1)