import json

# Đọc dữ liệu từ file1.json và file2.json
with open('cay_con.json', 'r') as f1:
    data1 = json.load(f1)
with open('thu_hoach.json', 'r') as f2:
    data2 = json.load(f2)
with open('cham_soc.json', 'r') as f3:
    data3 = json.load(f3)
with open('trong_trot.json', 'r') as f4:
    data4 = json.load(f4)   
with open('basic_comunication.json', 'r') as f5:
    data5 = json.load(f5)

# Kết hợp dữ liệu từ hai file JSON
merged_data = {"intents": data1["intents"] + data2["intents"] +data3["intents"] + data4["intents"] +data5["intents"] }

# Tạo một file Python mới để lưu trữ dữ liệu kết hợp
with open("data.json", "w") as outfile:
    json.dump(merged_data, outfile)