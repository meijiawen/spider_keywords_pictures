import json
import os
import time
import traceback
import pyautogui

from selenium import webdriver  # 导入selenium包
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
from settings import bilibili_cookie_path, bilibili_video_path, bilibili_video_screen_shot_path, bilibili_article_picture_path, \
    record_url_pic, record_url_local, record_tags, requests_timeout
from tools import log, getResModel, download_pic, excel, download_video
import requests

requests.DEFAULT_RETRIES = 5  # 增加重试连接次数


# bilibili
class Bilibili_video:

    def __init__(self):
        # self.keyword = " ".join(keyword)
        if not os.path.exists(bilibili_video_path):
            os.mkdir(bilibili_video_path)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches",
                                               ['enable-automation'])
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        s = Service('./chromedriver')
        # # s = Service("Driver/geckodriver.exe")
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        # self.driver = webdriver.Chrome(options=chrome_options)

        self.__updateCookie()

    def setKeyword(self, keywords: list):
        self.keyword = " ".join(keywords)

    def __updateCookie(self):
        self.driver.get('https://search.bilibili.com/video')
        time.sleep(5)
        if not os.path.exists(bilibili_cookie_path):
            time.sleep(40)  # 留够时间来手动登录
            with open(bilibili_cookie_path, 'w') as f:
                # 将cookies保存为json格式在cookies.txt中
                f.write(json.dumps(self.driver.get_cookies()))
        else:
            self.driver.delete_all_cookies()
            with open(bilibili_cookie_path, 'r') as f:
                cookies_list = json.load(f)  # 读取cookies
                for cookie in cookies_list:
                    if isinstance(cookie.get('expiry'), float):
                        cookie['expiry'] = int(cookie['expiry'])
                    try:
                        self.driver.add_cookie(cookie)  # 加入cookies
                    except:
                        print(cookie)
            self.driver.refresh()

    def __scrollToBottom(self, scrollTime: int):
        for i in range(scrollTime):
            pos = pyautogui.size()
            pyautogui.moveTo(pos.width / 2, pos.height / 2)
            pyautogui.scroll(-400)
            time.sleep(0.2)

    def searchVideo(self, scrollTime: int):
        self.driver.get('https://search.bilibili.com/video?keyword={}'.format(
            self.keyword))
        self.driver.maximize_window()
        print("开始搜索")
        time.sleep(2)
        self.__scrollToBottom(scrollTime)

        with open("video_list.txt", "w") as f:
            urls = []
            introductions = []
            for video in self.driver.find_elements(By.CLASS_NAME,
                                                   "bili-video-card"):
                title = video.find_element(By.CSS_SELECTOR,
                                           '[target="_blank"]')
                url = title.get_attribute('href')
                urls.append(url)
                print(url)
                f.write(url + "\n")

        time.sleep(2)
        print(urls)
        return
