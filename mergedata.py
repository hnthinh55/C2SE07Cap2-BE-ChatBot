import json

# Đọc dữ liệu từ file1.json và file2.json
with open('service.json', 'r') as f1:
    data1 = json.load(f1)
with open('basic_comunication.json', 'r') as f2:
    data2 = json.load(f2)

# Kết hợp dữ liệu từ hai file JSON
merged_data = {"intents": data1["intents"] + data2["intents"]}

# Tạo một file Python mới để lưu trữ dữ liệu kết hợp
with open("data.json", "w") as outfile:
    json.dump(merged_data, outfile)