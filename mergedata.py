import json

# Đọc dữ liệu từ file1.json và file2.json
with open('./data/cay_con.json', 'r') as f1:
    data1 = json.load(f1)
with open('./data/thu_hoach.json', 'r') as f2:
    data2 = json.load(f2)
with open('./data/cham_soc.json', 'r') as f3:
    data3 = json.load(f3)
with open('./data/trong_trot.json', 'r') as f4:
    data4 = json.load(f4)   
with open('./data/basic_comunication.json', 'r', encoding='utf-8') as f5:
    data5 = json.load(f5)
with open('./data/weather.json', 'r') as f6:
    data6 = json.load(f6)

# Kết hợp dữ liệu từ hai file JSON
merged_data = {"intents": data1["intents"] + data2["intents"] +data3["intents"] + data4["intents"] +data5["intents"]+ data6["intents"]}

# Tạo một file Python mới để lưu trữ dữ liệu kết hợp
with open("data.json", "w") as outfile:
    json.dump(merged_data, outfile)