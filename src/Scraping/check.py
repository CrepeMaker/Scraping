import pandas as pd
import numpy as np
import requests
import pandas
from bs4 import BeautifulSoup
import re
import time
import ast
import json
import copy
import os
import csv

from pprint import pprint

import re

def mysplit(text):
        subtext = re.sub(r'((?:。|\.|！|!|？|\?|☆)+)', '\\1\n', text)
        test_list = subtext.split('\n')
        sen_list = filter(lambda a: a !='', test_list)
        print(list(sen_list))

data = [['千代田区', 'https://retty.me/area/PRE13/city/13101/'], ['中央区', 'https://retty.me/area/PRE13/city/13102/'], ['港区', 'https://retty.me/area/PRE13/city/13103/'], ['新宿区', 'https://retty.me/area/PRE13/city/13104/'], ['文京区', 'https://retty.me/area/PRE13/city/13105/'], ['台東区', 'https://retty.me/area/PRE13/city/13106/'], ['墨田区', 'https://retty.me/area/PRE13/city/13107/'], ['江東区', 'https://retty.me/area/PRE13/city/13108/'], ['品川区', 'https://retty.me/area/PRE13/city/13109/'], ['目黒区', 'https://retty.me/area/PRE13/city/13110/'], ['大田区', 'https://retty.me/area/PRE13/city/13111/'], ['世田谷区', 'https://retty.me/area/PRE13/city/13112/'], ['渋谷区', 'https://retty.me/area/PRE13/city/13113/'], ['中野区', 'https://retty.me/area/PRE13/city/13114/'], ['杉並区', 'https://retty.me/area/PRE13/city/13115/'], ['豊島区', 'https://retty.me/area/PRE13/city/13116/'], ['北区', 'https://retty.me/area/PRE13/city/13117/'], ['荒川区', 'https://retty.me/area/PRE13/city/13118/'], ['板橋区', 'https://retty.me/area/PRE13/city/13119/'], ['練馬区', 'https://retty.me/area/PRE13/city/13120/'], ['足立区', 'https://retty.me/area/PRE13/city/13121/'], ['葛飾区', 'https://retty.me/area/PRE13/city/13122/'], ['江戸川区', 'https://retty.me/area/PRE13/city/13123/'], ['八王子市', 'https://retty.me/area/PRE13/city/13201/'], ['立川市', 'https://retty.me/area/PRE13/city/13202/'], ['武蔵野市', 'https://retty.me/area/PRE13/city/13203/'], ['三鷹市', 'https://retty.me/area/PRE13/city/13204/'], ['青梅市', 'https://retty.me/area/PRE13/city/13205/'], ['東京都 府中市', 'https://retty.me/area/PRE13/city/13206/'], ['昭島市', 'https://retty.me/area/PRE13/city/13207/'], ['調布市', 'https://retty.me/area/PRE13/city/13208/'], ['町田市', 'https://retty.me/area/PRE13/city/13209/'], ['小金井市', 'https://retty.me/area/PRE13/city/13210/'], ['小平市', 'https://retty.me/area/PRE13/city/13211/'], ['日野市', 'https://retty.me/area/PRE13/city/13212/'], ['東村山市', 'https://retty.me/area/PRE13/city/13213/'], ['国分寺市', 'https://retty.me/area/PRE13/city/13214/'], ['国立市', 'https://retty.me/area/PRE13/city/13215/'], ['福生市', 'https://retty.me/area/PRE13/city/13218/'], ['狛江市', 'https://retty.me/area/PRE13/city/13219/'], ['東大和市', 'https://retty.me/area/PRE13/city/13220/'], ['清瀬市', 'https://retty.me/area/PRE13/city/13221/'], ['東久留米市', 'https://retty.me/area/PRE13/city/13222/'], ['武蔵村山市', 'https://retty.me/area/PRE13/city/13223/'], ['多摩市', 'https://retty.me/area/PRE13/city/13224/'], ['稲城市', 'https://retty.me/area/PRE13/city/13225/'], ['羽村市', 'https://retty.me/area/PRE13/city/13227/'], ['あきる野市', 'https://retty.me/area/PRE13/city/13228/'], ['西東京市', 'https://retty.me/area/PRE13/city/13229/'], ['西多摩郡瑞穂町', 'https://retty.me/area/PRE13/city/13303/'], ['西多摩郡日の出町', 'https://retty.me/area/PRE13/city/13305/'], ['西多摩郡檜原村', 'https://retty.me/area/PRE13/city/13307/'], ['西多摩郡奥多摩町', 'https://retty.me/area/PRE13/city/13308/'], ['大島町', 'https://retty.me/area/PRE13/city/13361/'], ['利島村', 'https://retty.me/area/PRE13/city/13362/'], ['新島村', 'https://retty.me/area/PRE13/city/13363/'], ['神津島村', 'https://retty.me/area/PRE13/city/13364/'], ['三宅島三宅村', 'https://retty.me/area/PRE13/city/13381/'], ['御蔵島村', 'https://retty.me/area/PRE13/city/13382/'], ['八丈島八丈町', 'https://retty.me/area/PRE13/city/13401/'], ['小笠原村', 'https://retty.me/area/PRE13/city/13421/']]
channel = {}

if not os.path.exists("R_comment_"+"目黒区"+".csv"):
            print("まだ作成されていない")
            exit()

num = np.random.choice(range(1,66534), 100, replace=True)
print(num)

on = set()
with open("R_comment_"+"目黒区"+".csv", 'r') as f:
    i = 0
    reader = csv.reader((line.replace('\0','') for line in f))
    for com in reader:
        if i in num:
            print(i)
            if len(com) >= 3:
                print(mysplit(com[2]))
            on.add(i)
        i += 1
print(i)        
print(on-set(num))

print("--exit--")