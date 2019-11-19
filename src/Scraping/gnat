import sys
import urllib
import xml.etree.ElementTree as ET
import json
import requests
import csv
import pandas as pd
import time

keyid = '8492abeadc7102c29c18b759e23a102c'
pref = 'PREF13' #東京
hit_per_page = 100

query = {
    "keyid": keyid, 
    "pref":pref,
    "hit_per_page":hit_per_page
}

def rest_search(query):
    res_list = []
    res = json.loads(requests.get("https://api.gnavi.co.jp/RestSearchAPI/v3/", params=query).text)
    # レスポンスがerror じゃない場合に処理を開始する
    if "error" not in res:
        #ヒットした店舗数をカウント    
        rest_count = res["total_hit_count"]/hit_per_page
        for i in range(int(rest_count)):
            if i*hit_per_page+1 < 500:
                offset = min(1000,i*hit_per_page+1)
                res = json.loads(requests.get("https://api.gnavi.co.jp/RestSearchAPI/v3/", params=query).text)
                if "error" not in res:    
                    res_list.extend(res["rest"])
    return res_list
    
res = rest_search(query)

def extract_restaurant_info(restaurants: 'restaurant response') -> 'restaurant list':
    restaurant_list = []
    for restaurant in restaurants:
        id = restaurant["id"]
        name = restaurant["name"]
        category = restaurant["category"]
        url = restaurant["url"]
        address = restaurant["address"]
        tel = restaurant["tel"]
        area_name_s = restaurant["code"]["areaname_s"]
        restaurant_list.append([id, name, category, url, address, tel, area_name_s])
    return restaurant_list
    
restaurants_info = extract_restaurant_info(res)

#CSVファイルを出力する
with open('Tokyo_restaurants_1000.csv', 'w', newline='', encoding="utf_8_sig") as csvFile:
    csvwriter = csv.writer(csvFile,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writerow(['店舗ID', '店舗名', 'カテゴリー', 'URL', '住所', '電話番号', '地区名小'])
    for info in restaurants_info:
        csvwriter.writerow(info)
