import json
import flask
import pyodbc
server = 'MSI\SQLEXPRESS'
database = 'NETFarm'
username = 'NETFarm'
password = 'password'
driver = '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';trusted_connection=Yes')
cursor = cnxn.cursor()

query = "SELECT st.StageName,StandardName,av.Description FROM [NETFarm].[dbo].[Standard] sd LEFT JOIN [NETFarm].[dbo].[Advice] av ON sd.Id = av.StandardId LEFT JOIN [NETFarm].[dbo].[Stage] st ON st.Id = av.StageId"
cursor.execute(query)

results = cursor.fetchall()
# for row in results:
#     print(row)

cursor.close()
cnxn.close()
prefixes = ["Cách", "Trong giai đoạn", "Tư vấn cho tôi về"]
data = []
for result in results:
    data.append({
        "tag": result[0].replace(" ", "_")+'_'+result[1].replace(" ", "_"),
        "patterns": [prefixes[0]+result[0]+' '+result[1], prefixes[1]+result[0]+' '+result[1], prefixes[2]+result[0]+' '+result[1]],
        "responses": [result[1] +'trong giai đoạn này bạn nên: '+' '+result[2]],
        "context": []
    })
for d in data:
    print(d)

root_element = {"intents": data}

with open("service.json", "w") as outfile:
    json.dump(root_element, outfile)

print("Data saved to output.json")