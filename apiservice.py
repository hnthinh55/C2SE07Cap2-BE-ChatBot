import pymongo
import pyodbc
import json
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["StandardDb"]
collection = db["apiweather"]
list_weather = []

for doc in collection.find():
    list_weather.append(doc)
server = '.'
database = 'NETFarm'
username = 'NETFarm'
password = 'password'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';trusted_connection=Yes')
cursor = cnxn.cursor()

query_cham_soc ='SELECT st.StageName,StandardName,av.Description,[MinTemp],[MaxTemp],[MinHumidity],[MaxHumidity],[Wind],[MaxRain],[Season] FROM [NETFarm].[dbo].[Standard] sd LEFT JOIN [NETFarm].[dbo].[Advice] av ON sd.Id = av.StandardId LEFT JOIN [NETFarm].[dbo].[Stage] st ON st.Id = av.StageId '
cursor.execute(query_cham_soc)

list_cham_soc = []
list_thu_hoach = []
list_caycon = []
list_gieo_trong = []
cham_soc = cursor.fetchall()
for row in cham_soc:
    if row[0] == 'Chăm sóc thường xuyên' :
        obj = {
            "StageName": row[0],
            "StandardName": row[1],
            "Description": row[2],
        }
        list_cham_soc.append(obj)
    if row[0] == 'Thu hoạch' :
        obj = {
            "StageName": row[0],
            "StandardName": row[1],
            "Description": row[2],
        }
        list_thu_hoach.append(obj)
    if row[0] == 'Nảy mầm cây con' :
        obj = {
            "StageName": row[0],
            "StandardName": row[1],
            "Description": row[2],
            "MinTemp":row[3] ,
            "MaxTemp":row[4],
            "MinHumidity":row[5],
            "MaxHumidity":row[6],
            "Wind":row[7],
            "MaxRain":row[8],
        }
        list_caycon.append(obj)

    if row[0] == 'Gieo trồng' :
        obj = {
            "StageName": row[0],
            "StandardName": row[1],
            "Description": row[2],
            "MinTemp":row[3] ,
            "MaxTemp":row[4],
            "MinHumidity":row[5],
            "MaxHumidity":row[6],
            "Wind":row[7],
            "MaxRain":row[8],
            "Season": row[9]
        }
        list_gieo_trong.append(obj)
cnxn.close()

#Cham soc
def ChamSoc():
    prefixes = ["Hôm nay tôi có thể", "Khi nào tôi có thể", "Trong những ngày tới tôi có thể", "Thời điểm thích hợp để"]
    data = []
    for result in list_cham_soc:
        data.append({
            "tag": result['StageName'].replace(" ", "_")+'_'+result['StandardName'].replace(" ", "_"),
            "patterns": [prefixes[0]+' '+result['StageName']+' '+result['StandardName'], prefixes[1]+' '+result['StageName']+' '+result['StandardName'], prefixes[2]+' '+result['StageName']+' '+result['StandardName']],
            "responses": ['<p style=\"text-align:center; font-weight:bold\">'+result['StandardName'] +' trong giai đoạn này bạn nên: '+' '+result['Description']],
            "context": []
        })

    root_element = {"intents": data}

    with open("./data/cham_soc.json", "w") as outfile:
        json.dump(root_element, outfile)    
    return "Data saved to cham_soc.json"
k = ChamSoc()
print(k)

#Thu hoach
def ThuHoach() :
    weatherlist = sorted(list_weather, key=lambda x: x['_id'])
    
    rainday = []
    data = []
    for j in range(7):
        if weatherlist[j]['Description'] == "Moderate rain" or weatherlist[j]['Description']  == "Heavy rain":
            rainday.append(weatherlist[j]['DateTime'].strftime("%d/%m/%Y"))
    combinedString = ",".join(rainday)
    prefixes = ["Hôm nay tôi có thể", "Khi nào tôi có thể", "Trong những ngày tới tôi có thể", "Thời điểm thích hợp để"]
    for counseling in list_thu_hoach:
        api = {
            "result": ""
        }
        if len(rainday) == 7:
            api['result'] += f"Người dân <span style ='font-weight:bold;'>không nên</span> thu hoạch vào 7 ngày tiếp theo vì thời tiết không đảm bảo cho sức khoẻ và nông sản thu hoạch." + \
                f"Nếu bắt buộc phải thu hoạch thì nên chú ý vì những ngày tiếp theo sẽ có mưa vừa và lớn." + \
                f" Trong giai đoạn thu hoạch {counseling['StandardName']} bạn nên : {counseling['Description']}"
        elif len(rainday) > 0:
            api['result'] += f"Trong những ngày: <span style ='font-weight:bold; color:red'>{combinedString}</span> có mưa từ trung bình đến to. Ảnh hưởng đến việc thu hoạch cây <span style ='font-weight:bold;'>{counseling['StandardName']}.</span>" + \
                f"Người dân nên xem xét thu hoạch vào những ngày khác." + \
                f" Trong giai đoạn thu hoạch {counseling['StandardName']} bạn nên : {counseling['Description']}"
        else:
            api['result'] += f"Trong 7 ngày tới có điều kiện thời tiết tốt thích hợp cho việc thu hoạch. " + \
                    f"Trong giai đoạn thu hoạch cây {counseling['StandardName']} bạn nên : {counseling['Description']}" + \
                    f"Chúc người dân có một vụ mùa thu hoạch thành công."
        data.append({
            "tag": counseling['StageName'].replace(" ", "_")+'_'+counseling['StandardName'].replace(" ", "_"),
            "patterns": [prefixes[0]+' '+counseling['StageName']+' '+counseling['StandardName'], prefixes[1]+' '+counseling['StageName']+' '+counseling['StandardName'], prefixes[2]+' '+counseling['StageName']+' '+counseling['StandardName']],
            "responses": [api['result']],
            "context": []
        })
    root_element = {"intents": data}

    with open("./data/thu_hoach.json", "w") as outfile:
        json.dump(root_element, outfile)    
    return "Data saved to thu_hoach.json"
k = ThuHoach()
print(k)

def check_day(goodDay,hotDate,warningDay):
    api=""
    hotDay = ", ".join(hotDate)
    good = ", ".join(goodDay)
    warning = ", ".join(warningDay)
    if len(goodDay) == 6:
        api += f"<span style='color:red; font-weight:bold; font-size:20px'>Lưu ý :</span><br/><span style='font-style:italic'>Trong 7 ngày tiếp theo thời tiết thuận lợi cho việc bón phân.</span>"
    elif len(goodDay) > 0:
        api += f"<span style='font-weight:bold; font-size:20px'>Lưu ý :</span><br/><span style='font-style:italic'>Nếu có ý định bón phân trong 7 ngày tiếp theo thì bạn nên bón vào ngày <span style='font-weight:bold;color:green;'>{good}</span>. </span>" + \
        f"<span style='font-style:italic'>Vì quá trình hấp thụ dinh dưỡng từ phân hữu cơ của cây chậm, khi gặp mưa, dinh dưỡng trong phân thường bị rửa trôi. Đặc biệt không nên bón phân hữu cơ.</span>"
    if hotDay != None and hotDay != "":
        api += f"<span style='font-style:italic'>Nhiệt độ các ngày: <span style='font-weight:bold;color:green;'>{hotDay}</span> cũng khá cao, bạn nên bón phân vào sáng sớm hoặc vào chiều tối vì khi nắng quá gắt sẽ làm phân bón bốc hơi, kèm theo là có thể làm cháy lá hoặc hỏng lá</span>"
    if warning != None and warning != "":
        api += f"<span style='font-style:italic'>Người dân lưu ý:<span style='font-weight:bold;color:red;'>{warning}</span> là những ngày có gió mạnh, nguy cơ cao ảnh hưởng đến cây non </span>"
    else:
        api += f"Điều kiện thời tiết trong 7 ngày tiếp theo mưa nên <span style='font-weight:bold;'>không phù hợp</span> cho việc bón phân. " + \
            f"Vì quá trình hấp thụ dinh dưỡng từ phân hữu cơ của cây chậm, khi gặp mưa, dinh dưỡng trong phân thường bị rửa trôi. Đặc biệt <span style=\"font-weight:bold;\">không nên</span> bón phân hữu cơ. "
    return api

def APICounseling_CayCon():
    weatherlist = sorted(list_weather, key=lambda x: x['_id'])
    data = []
    prefixes = ["Hôm nay tôi có thể", "Khi nào tôi có thể", "Trong những ngày tới tôi có thể", "Thời điểm thích hợp để"]
    for counseling in list_caycon:
        api = ""
        api = f'<p style="\text-align:center; font-weight:bold\">Đối với {counseling["StandardName"]} trong giai đoạn này bạn nên:</p> {counseling["Description"]}'
        hotDate = []
        goodDay = []
        warningDay = []
        for j in range(6):
            if ((weatherlist[j]['Description'] != "Moderate rain" and weatherlist[j]['Description'] != "Heavy rain") and
            (weatherlist[j+1]['Description'] != "Moderate rain" and weatherlist[j+1]['Description'] != "Heavy rain")):
                goodDay.append(weatherlist[j]['DateTime'].strftime("%d/%m/%Y"))
                if weatherlist[j]["maxTemp"] > counseling["MaxTemp"]:
                    hotDate.append(weatherlist[j]['DateTime'].strftime("%d/%m/%Y"))
                if weatherlist[j]["wind"] > counseling["Wind"]:
                    warningDay.append(weatherlist[j]['DateTime'].strftime("%d/%m/%Y"))
        # api.result += f"Nhiệt độ ngày này cũng khá cao, bạn nên bón phân vào sáng sớm hoặc vào chiều tối vì khi nắng quá gắt sẽ làm phân bón bốc hơi, kèm theo là có thể làm cháy lá hoặc hỏng lá"
        api += check_day(goodDay,hotDate,warningDay)
        data.append({
            "tag": counseling['StageName'].replace(" ", "_")+'_'+counseling['StandardName'].replace(" ", "_"),
            "patterns": [prefixes[0]+' '+counseling['StageName']+' '+counseling['StandardName'], prefixes[1]+' '+counseling['StageName']+' '+counseling['StandardName'], prefixes[2]+' '+counseling['StageName']+' '+counseling['StandardName']],
            "responses": [api],
            "context": []
        })
    root_element = {"intents": data}

    with open("./data/cay_con.json", "w") as outfile:
        json.dump(root_element, outfile)    
    return "Data saved to cay_con.json"
k = APICounseling_CayCon()
print(k)


def TrongTrot():
    weatherlist = sorted(list_weather, key=lambda x: x['_id'])
    hotDate = []
    goodDay = []
    data = []
    prefixes = ["Hôm nay tôi có thể", "Khi nào tôi có thể", "Trong những ngày tới tôi có thể", "Thời điểm thích hợp để"]
    for counseling in list_gieo_trong:
        not_good = []
        api = '<p style="font-weight:bold; text-align:center;">Thông qua dự đoán thời tiết các ngày tới: </p>'
        seasons = list(map(int, counseling['Season'].split(',')))
        for i in range(3):
            mintemp = 0.0
            maxtemp = 0.0
            avgrain = 0.0
            avghumidity = 0.0
            checkday = True
            value = weatherlist[i]['DateTime'].month
            if value not in seasons:
                not_good.append(datetime.strftime(weatherlist[i]['DateTime'], '%d/%m/%Y'))
            else:
                for j in range(i, i + 5):
                    mintemp += weatherlist[j]['minTemp']
                    maxtemp += weatherlist[j]['maxTemp']
                    avgrain += weatherlist[j]['Rain']
                    avghumidity += weatherlist[j]['humidity']
                    if (weatherlist[j]['Rain'] > counseling['MaxRain']) or (weatherlist[j]['maxTemp'] > counseling['MaxTemp'] and weatherlist[j]['humidity'] < counseling['MinHumidity']):
                        checkday = False
                        break
                    elif weatherlist[j]['maxTemp'] > counseling['MaxTemp'] and weatherlist[j]['humidity'] > counseling['MinHumidity']:
                        hotDate.append(datetime.strftime(weatherlist[j]['DateTime'], '%d/%m/%Y'))
                if checkday:
                    mintemp /= 5
                    maxtemp /= 5
                    avghumidity /= 5
                    if (mintemp > counseling['MinTemp'] and maxtemp < counseling['MaxTemp']) and (counseling['MaxHumidity'] > avghumidity and avghumidity > counseling['MinHumidity']) and avgrain > counseling['MaxRain']:
                        goodDay.append(datetime.strftime(weatherlist[i]['DateTime'], '%d/%m/%Y'))
                    else:
                        hotDate.clear()
                elif not checkday and i == 2:
                    api += f'Trong tuần này không thích hợp đẻ trồng trọt vì điều kiện thời tiết không thích hợp cho sự phát triển của cây <span style="font-weight:bold;">{counseling["StandardName"]}</span>'
        if len(not_good) <2:
            combined_string = ",".join(hotDate)
            good = ",".join(goodDay)
            if len(goodDay) > 0:
                api += f'Trong 3 ngày tới, nếu bạn muốn trồng <span style ="font-weight:bold;">{counseling["StandardName"]}</span> thì nên trồng vào những ngày <span style =\"color: green;\">{good}</span> để cây có thể phát triển trong điều kiện tốt nhất. Đối với loại cây này trong mùa gieo trồng bạn nên:{counseling["Description"]}'
            if len(hotDate) > 0:
                api += f" <span style ='font-weight:bold; color:red'>Lưu ý: </span> <br/>những ngày <span style ='font-weight:bold;'>{combined_string}</span> có nắng nóng, người dân nên chú ý việc tưới nước để tránh mất nước cho giống."
            else:
                api += f" Trong tuần này điều kiện thời tiết trung bình trong 7 ngày <span style ='font-weight:bold;'>không phù hợp</span> với sự phát triển cây con. Có nguy cơ ảnh hưởng đến năng xuất cây sau này.Đối với loại cây này trong mùa gieo trồng bạn nên:{counseling['Description']}"
        else:
            date_string = ', '.join(not_good)
            api += f'<span style ="font-weight:bold; color:red">{date_string}</span> không thích hợp để trồng {counseling["StandardName"].lower()}. Vì không năm trong thời vụ thích hợp. Bạn có thể trồng cây <span style="font-weight:bold;">{counseling["StandardName"].lower()}</span> vào những tháng sau: <span style="color: green;">{counseling["Season"]}</span>'
        data.append({
            "tag": counseling['StageName'].replace(" ", "_")+'_'+counseling['StandardName'].replace(" ", "_"),
            "patterns": [prefixes[0]+' '+counseling['StageName']+' '+counseling['StandardName'], prefixes[1]+' '+counseling['StageName']+' '+counseling['StandardName'], prefixes[2]+' '+counseling['StageName']+' '+counseling['StandardName']],
            "responses": [counseling['StandardName'] +' trong giai đoạn này bạn nên: '+' '+ api],
            "context": []
        })
    root_element = {"intents": data}

    with open("./data/trong_trot.json", "w") as outfile:
        json.dump(root_element, outfile)    
    return "Data saved to trong_trot.json"
k = TrongTrot()
print(k)
