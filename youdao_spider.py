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
