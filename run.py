# # import schedule
# import subprocess
# import time
# import pyodbc

# while True:
#     subprocess.run(['python', 'importdata.py'])
#     # subprocess.run(['python', 'mergedata.py'])
#     # subprocess.run(['python', 'training.py'])
# time.sleep(100)

# # def run_file(file_name):
# #     subprocess.run(["python", file_name])
# '''
# # Hàm để đặt lịch chạy các file sau mỗi 30 phút
# def schedule_files(file_list):
#     for file_name in file_list:
#         schedule.every(3).minutes.do(run_file, file_name)

# # Thực thi file app.py
# subprocess.run(["python", "app.py"])

# # Đặt lịch chạy các file
# file_list = ["importdata.py", "mergedata.py", "training.py"]
# schedule_files(file_list)

# # Vòng lặp để kiểm tra và thực thi các lịch chạy trong `schedule`
# while True:
#     schedule.run_pending()
#     time.sleep(1)
# '''


import subprocess
import time
import pyodbc
import json

while True:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI\SQLEXPRESS;DATABASE=NETFarm;trusted_connection=Yes')
    cursor = cnxn.cursor()

    query = "SELECT st.StageName,StandardName,av.Description FROM [NETFarm].[dbo].[Standard] sd LEFT JOIN [NETFarm].[dbo].[Advice] av ON sd.Id = av.StandardId LEFT JOIN [NETFarm].[dbo].[Stage] st ON st.Id = av.StageId"
    cursor.execute(query)

    results = cursor.fetchall()

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

    root_element = {"intents": data}

    with open("service.json", "w") as outfile:
        json.dump(root_element, outfile)

    print("Data saved to service.json")

    subprocess.run(['python', 'mergedata.py'])
    subprocess.run(['python', 'training.py'])

    time.sleep(100)