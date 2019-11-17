# ettyScriping

## Retty用のスクレイピング(rettyScriping)

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
from pprint import pprint
```

### 使用方法

class"rettyScriping"を用いる。

基本的にはgetData()を用いてcsvを作成する。

引数は"都道府県名(str)","どこから(int)","どこまで(int)","csv名/None(追記する時、ないときはNone)"

出力されるcsv名は追記でない限り"PRE{数字}".csvとなっている。
