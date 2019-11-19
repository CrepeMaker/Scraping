import sys
import urllib
import xml.etree.ElementTree as ET
import json
import requests
import csv
import pandas as pd
import time

keyid = '8492abeadc7102c29c18b759e23a102c'
area = '東京'
page_size = 50

query = {
    "keyid": keyid, 
    "area": area,
    "hit_per_page": page_size,
    "offset_page": 1,
}

def rest_search(query):
    res_list = []
    # レスポンスがerror じゃない場合に処理を開始する
        #ヒットした店舗数をカウント
    for page in range(1):
        try:
            query["offset_page"] = page + 1
            res = json.loads(requests.get("https://api.gnavi.co.jp/PhotoSearchAPI/v3/", params=query).text)
            if "gnavi" in res and "error" in res["gnavi"]:
                break
            for i in range(res["response"]["hit_per_page"]):
                res_list.append(res["response"][str(i)])
            if res["response"]["hit_per_page"]==0:
                break
        except Exception as e:
            print(res)
            print(e)
            break
    return res_list
    
res = rest_search(query)

#リストを作成する
def extract_restaurant_info(restaurants: 'restaurant response') -> 'restaurant list':
    restaurant_list = []
    for i in range(len(res)):
        id = res[i]["photo"]["shop_id"]
        url = res[i]["photo"]["shop_url"]
        vote_id = res[i]["photo"]["vote_id"]
        if res[i]["photo"]["nickname"] == "ぐるなび会員":
            nickname = None
        else:
            nickname = res[i]["photo"]["nickname"]
        comment = res[i]["photo"]["comment"]
        total_score = res[i]["photo"]["total_score"]
        restaurant_list.append([id, url, vote_id, nickname, comment, total_score])
    return restaurant_list
    
restaurants_info = extract_restaurant_info(res)

#CSVファイルを出力する
with open('Tokyo_restaurants_comment_5.csv', 'w', newline='', encoding="utf_8_sig") as csvFile:
    csvwriter = csv.writer(csvFile,delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writerow(['店舗ID', 'URL', '投稿ID', 'ニックネーム', 'コメント', '評価'])
    for info in restaurants_info:
        csvwriter.writerow(info)
