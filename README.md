# Scraping(Retty,食べログ,ぐるなび)

パッケージインストール(対応:tabeLogScraping.py rettyScraping.py)

```
pip install git+https://github.com/BDA2019TeamA/Scraping
```

使用方法(ぐるなびはAPIの都合上不可能)

```
from Scraping import *
retty = rettyScraping()
tabe = tabeLogScraping()
```

### 調子が悪かったらsetup.pyのinstall_requiresの部分を消して手動で必要なライブラリを入れる

## Retty用の都道府県別スクレイピング(rettyScraping)

### 使用に必要なライブラリ
```
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
import sys
from pprint import pprint
```

### 使用方法


class `rettyScraping` を用いる。

基本的にはgetData()を用いてcsvを作成する。

引数は `都道府県名(str)`, `どこから(int)`, `どこまで(int)`, `csv名/None(追記する時、ないときはNone)`


出力されるcsv名は追記でない限り`PRE{数字}.csv`となっている。

### csvの中身
#### column

- category:食べ物のカテゴリー
- comment:コメント
- name:店の名前
- phone:電話番号
- restaurantId:Rettyにおける店id
- score:1~3の評価値
- url:url
- userId:コメントした人のid


## 食べログ用の都道府県別スクレイピング(tabeLogScraping.py)

### 使用に必要なライブラリ
```
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
import sys
from pprint import pprint
```

### 使用方法

class `tabeLogScraping` を用いる。

基本的にはgetData()を用いてcsvを作成する。

引数は `都道府県名(str)`, `どこから(int)`, `どこまで(int)`, `csv名/None(追記する時、ないときはNone)`

出力されるcsv名は追記を行わない限り`AREA{都道府県のローマ字}.csv`となっている。

### csvの中身
#### column

- category:食べ物のカテゴリー
- comment:コメント
- name:店の名前
- phone:電話番号
- restaurantId:Rettyにおける店id
- score:0~5の評価値

---
###### 個別score
- 料理・味:0~5の評価値
- サービス:0~5の評価値
- 雰囲気:0~5の評価値
- CP(コスパ):0~5の評価値
- 酒・ドリンク:0~5の評価値
---
- url:url
- userId:コメントした人のid



## Retty用の東京都内スクレイピング(rettyScraping)


#### retty_restaurantTokyo_Scraping.py

##### 取得できるcsvの中身

- '店舗ID'
- '店舗名'
- 'カテゴリー'
- 'URL'
- '住所'
- '電話番号'
- '地区名小'


#### retty_commentTokyo_Scraping.py

##### 取得できるcsvの中身

- '店舗ID'
- 'URL'
- '投稿ID'
- 'ニックネーム'
- 'コメント'
- '評価'




## 食べログ用の東京都内スクレイピング(tabeLogScraping.py)

#### tabeLog_restaurantTokyo_Scraping.py

##### 取得できるcsvの中身

- '店舗ID'
- '店舗名'
- 'カテゴリー'
- 'URL'
- '住所'
- '電話番号'
- '地区名小'


#### tabeLog_commentTokyo_Scraping.py


- '店舗ID'
- 'URL'
- '投稿ID'
- 'ニックネーム'
- 'コメント'
- '評価'
- '料理・味'
- 'サービス'
- '雰囲気'
- 'CP(コスパ)'
- '酒・ドリンク'





## ぐるなび用のスクレイピング(gnavi_comment_Scraping,gnavi_restaurant_Scraping.py)

### 使用に必要なライブラリ

```
import sys
import urllib
import xml.etree.ElementTree as ET
import json
import requests
import csv
import pandas as pd
import time
```

### 使用方法

ぐるなびの[API登録](https://api.gnavi.co.jp/api/use/)をする

#### gnavi_comment_Scraping.py

#### gnavi_restaurant_Scraping.py

それぞれ実行すると対応するcsvが取得できる

### csvの中身
#### column(gnavi_comment_Scraping.py)

- '店舗ID'
- 'URL'
- '投稿ID'
- 'ニックネーム'
- 'コメント'
- '評価'

#### column(gnavi_restaurant_Scraping.py)


- '店舗ID'
- '店舗名'
- 'カテゴリー'
- 'URL'
- '住所'
- '電話番号'
- '地区名小'
