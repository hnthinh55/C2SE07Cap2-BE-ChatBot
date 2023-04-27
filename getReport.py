import requests

# Sử dụng FAOSTAT API để lấy thông tin về giá cả xuất khẩu gạo của Việt Nam trong năm 2020
url = "http://fenixservices.fao.org/faostat/api/v1/en/data/TP_Export/Country?area=237&item=296&year=2020"
params = {"fields": "Year,Value"}
headers = {"Content-Type": "application/json", "API_KEY": "YOUR_API_KEY"}

response = requests.get(url, headers=headers, params=params)
data = response.json()["data"][0]

print("Giá cả xuất khẩu gạo của Việt Nam trong năm 2020 là", data["Value"], "USD/tấn")