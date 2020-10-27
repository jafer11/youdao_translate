# 有道翻译破解

有道翻译官网（http://fanyi.youdao.com/）

## 破解步骤

### 第一步

使用Google浏览器进入有道翻译官网，按F12或者右击选择菜单中的“检查”，选择“Nerwork”，再选择XHR，如下图1所示。

![avatar](https://github.com/jafer11/youdao_translate/raw/main/images/图1.png)

### 第二步发送请求获取XHR数据包

在左侧框数据“hello”，敲击回车。就可以看到异步请求包，如下图所示。

![avatar](https://github.com/jafer11/youdao_translate/raw/main/images/图2.png)

### 第三步点击XHR数据包，分析数据

点击抓取到的XHR包，可以发现翻译请求的URL地址一起POST提交的数据

请求URL：http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule

method：POST

![avatar](images\图3.png)

经过多次尝试与分析salt、sign、lts字段时暂时无法获取的。此时就要思考以下怎么获取到。其实这三个字段的获取方法也很简单。因为这三个字段都是有JS生成的，可以搜索JS文件是否存在这三个字段。

### 第四步，获取salt、sign、lts字段

在开发者工具最上面的菜单选项的右上角的“X”左边点击选择“Search”。在下方弹出的输入框输入"salt",敲击回车，如下图。

![avatar](images\图4.png)

在搜索到的文件中选择第一个点击，进入到”Sources“，点击代码框的左下角”{}“，格式化代码，方便找想要的代码。

![avatar](images\图5.png)

按照Ctrl+F进入搜索框输入salt，找到如下代码段

![avatar](images\图6.png)



```javascript
ts："" + (new Date).getTime()

salt：ts+ parseInt(10 * Math.random(), 10);

sign: n.md5("fanyideskweb" + e + i + "]BjuETDhU)zqSxf-=B#7m")
```

这三个字段就找到了。

### 第五步，用python解析salt、ts、sign三个字段的生成方法

```python
ts = str(int(time.time() * 1000))
# salt
salt = ts + str(random.randint(0, 9))
# sign
string = "fanyideskweb" + word + salt + "]BjuETDhU)zqSxf-=B#7m"
s = md5()
s.update(string.encode())
sign = s.hexdigest()
```

生成这三个字段后将其加入请求头的data中发起请求，完成有道翻译的破解。

源码示例

```python
"""有道翻译破解"""
import requests
import time, random, json
from hashlib import md5


class YdSpider(object):
    def __init__(self):
        self.post_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6",
            "Connection": "keep-alive",
            # "Content-Length": "239",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "OUTFOX_SEARCH_USER_ID=1127085569@10.108.160.18; JSESSIONID=aaajxKEhtqnSt46qknvqx; OUTFOX_SEARCH_USER_ID_NCOO=1641745235.7750268; ___rl__test__cookies=1598086639410",
            "Host": "fanyi.youdao.com",
            "Origin": "http://fanyi.youdao.com",
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            "X-Requested-With": "XMLHttpReques",
        }

    def get_ts_salt_sign(self, word):
        # ts
        ts = str(int(time.time() * 1000))
        # salt
        salt = ts + str(random.randint(0, 9))
        # sign
        string = "fanyideskweb" + word + salt + "]BjuETDhU)zqSxf-=B#7m"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()

        return ts, salt, sign

    # 攻克有道
    def attack_yd(self, word):
        ts, salt, sign = self.get_ts_salt_sign(word)

        data = {"i": word,
                "from": "AUTO",
                "to": "AUTO",
                "smartresult": "dict",
                "client": "fanyideskweb",
                "salt": salt,
                "sign": sign,
                "lts": ts,
                "bv": "aa510f0fd141e8aee98da89f3b8bad73",
                "doctype": "json",
                "version": "2.1",
                "keyfrom": "fanyi.web",
                "action": "FY_BY_REALTlME",
                }

        res = requests.post(
            url=self.post_url,
            data=data,
            headers=self.headers
        )
        # {"translateResult":[[{"tgt":"头","src":"header"}]],"errorCode":0,"type":"en2zh-CHS","smartResult":{"entries":["","n. 头球；页眉；数据头；收割台\r\n"],"type":1}}
        html = res.json()
        result = html["translateResult"][0][0]['tgt']
        print('翻译结果：', result)

    def run(self):
        word = input('请输入要翻译的单词：')
        self.attack_yd(word)


if __name__ == '__main__':
    start = time.time()
    spider = YdSpider()
    spider.run()
    end = time.time() - start
    print('运行时间：', end)

```

