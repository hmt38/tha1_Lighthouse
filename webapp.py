import logging
import base64
import time
import nmap
import json

class method_Dom:
    name = "webapp-Dom"

    def __init__(self, db, logger):
        self.db = db
        self.logger = logger
        import os

        if os.name == 'posix':
            if not os.path.exists("standardTree\\wordpress.html"):
                self.logger.warning("SERVICES: standardTree not found")
            else:
                self.logger.info("SERVICES: standardTree found")

        elif os.name == 'nt':
            if not os.path.exists("standardTree/wordpress.html"):
                self.logger.warning("SERVICES: standardTree not found")
            else:
                self.logger.info("SERVICES: standardTree found")
        else:
            self.logger.info("SERVICES: standardTree not support")

        if os.name == 'nt':
            if os.path.exists("tools\\chrome\\chromedriver.exe"):
                self.chrome_driver = "tools\\chrome\\chromedriver.exe"
                self.logger.info("SERVICES: chromedriver found")
            else:
                self.logger.warning("SERVICES: chromedriver not found")
            # filepath = "tmp\\fscan\\"
        elif os.name == 'posix':
            if os.path.exists("tools/chrome/chromedriver"):
                self.chrome_driver = "tools/chrome/chromedriver"
                self.logger.info("SERVICES: chromedriver found")
            else:
                self.logger.warning("SERVICES: chromedriver not found")
            # filepath = "tmp/fscan/"

        # todo 提示用户输入
        self.file = "C:\\xxxxx\\xxxx\\chrome.exe"

        self.logger.info("SERVICES: chrome binary found")


    def get_html(self, target):
        import requests
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
        from bs4 import BeautifulSoup
        from collections import Counter

        page_source = ""
        # request测试
        try:
            response = requests.get(target)
            if response.status_code != 200 or response.status_code == 404 or response.status_code == 502:
                return page_source

        except Exception:
            self.logger.debug("SERVICES: requests exception")
        # 配置
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        service = Service(executable_path=self.chrome_driver)
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(target)
            # 记录初始时间
            start_time = time.time()

            while True:
                # 暂时存储当前URL
                current_url = driver.current_url
                # 等待一小段时间（比如0.5秒），以减少CPU使用率
                time.sleep(0.5)
                # 检查是否已经过去5秒
                if time.time() - start_time > 5:
                    # 如果5秒内URL没有变化，则假定页面加载完成
                    break
                # 如果URL发生了变化，则重置计时器
                if current_url != driver.current_url:
                    start_time = time.time()

            # 此时可以认为页面已经稳定，可以进行后续操作
            # 例如，获取页面源码

            if "Not Found" not in driver.title and "not found" not in driver.title and "sorry" not in driver.title:
                page_source = driver.page_source

        finally:
            # 关闭浏览器
            driver.quit()

        return page_source

    def extract_features(self, dom):
        from collections import Counter

        features = []
        for tag in dom.find_all(True):
            features.append(tag.name)
        return Counter(features)

    def cosine_similarity(self, vec1, vec2):
        from collections import Counter
        import numpy as np

        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = np.sqrt(sum1) * np.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator


    def cal_cosine_similarity(self, html_doc1, html_doc2):
        from bs4 import BeautifulSoup
        from collections import Counter
        import numpy as np
        import requests
        import os

        # 解析DOM树
        dom1 = BeautifulSoup(html_doc1, 'lxml')
        dom2 = BeautifulSoup(html_doc2, 'lxml')

        # 提取特征
        vec1 = self.extract_features(dom1)
        vec2 = self.extract_features(dom2)

        # print(vec1," ",vec2)

        # 计算相似度
        similarity = self.cosine_similarity(vec1, vec2)
        # print(f"相似度: {similarity}")
        return similarity


    def get_similar_value(self, ip, port, schemal):
        import os


        directory = ""
        directories = ["", "wp-admin", "test"]
        similarity_max = 0.0
        web_framework = ""

        for directory in directories:

            html_doc1 = self.get_html(schemal + "://" + ip + ":" + port + "/" + directory)

            if html_doc1 == "":
                continue

            ## 列举standardTree目录下的文件
            # 指定目录路径
            filedirectory = 'standardTree'
            # 获取目录下的所有文件名
            files = os.listdir(filedirectory)

            # 打印文件名
            for file in files:
                filename = file[:-5:]

                with open(filedirectory + "/{0}.html".format(filename), "r", encoding="utf-8") as f:
                    html_doc2 = f.read()

                similarity = self.cal_cosine_similarity(html_doc1, html_doc2)
                if similarity <= 0.8:
                    continue
                if similarity >= 0.8:

                    if similarity_max < similarity:
                        similarity_max = similarity
                        web_framework = filename

            if similarity_max != 0.0 and web_framework != "":
                print("web_framework: ", web_framework)
                print("similarity_max: ", similarity_max)
                # break 这里需要优化算法的准确性

        if similarity_max == 0.0:
            self.logger.debug("未识别出")
            web_framework = "UnFind"
        else:
            self.logger.debug("识别得出 %s ， 相似度 %s" %(web_framework, similarity_max))
        return web_framework

    def services(self, ip, port, schemal):
        import os
        import output
        import re


        ## 正则匹配出所有@#之间的字符串，并输出为数组
        matches = re.findall(r'@#(\w*)', schemal)
        print(matches)
        for match in matches:
            if match == "http":
                schemal = "http"
                break
            elif match == "https":
                schemal = "https"
                break

        if not os.path.exists(self.file):
            self.logger.warning("SERVICES: chrome.exe not found")
            self.logger.warning("SERVICES: Please make sure you have the chrome, and add to this module")
        else:
            self.logger.debug("SERVICE: chrome run")

            return self.get_similar_value(ip,port,schemal)


class app:
    def __init__(self, db, logger,method='webapp-Dom-based'):
        self.db = db
        self.logger = logger
        if method == 'webapp-Dom-based':
            self.method = method_Dom(db,logger)
        else:
            self.method = method_kscan(db,logger)


    def run(self, sleep=60):
        while True:
            try:
                ip, port, schemal = self.db.get_ip_no_services_have_http(self.method.name)

                if ip is not None:
                    self.logger.info("WEBAPP-CHECK %s %s %s %s" % (self.method.name,ip,port,schemal))
                    self.db.update_ip_services_timestamp(self.method.name,ip,port)

                # try:
                    web_app=self.method.services(ip, port, schemal)

                    if not web_app is None:
                        self.db.add_service_app(ip, port, web_app)
                        self.logger.debug(str(web_app))


                    self.logger.info("SERVICES-CHECK %s %s %s SUCCESS" % (self.method.name,ip,port))

                else:
                    self.logger.debug("SERVICES: sleep")
                    time.sleep(sleep)
            except Exception:
                self.logger.debug("SERVICES: sleep")
                time.sleep(sleep)

