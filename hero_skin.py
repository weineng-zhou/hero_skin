# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:44:41 2020
# google 驱动模拟操作 需要下载google浏览器相应版本的驱动chromedriver.exe
@author: weineng.zhou
"""

import os
import re
import random
import time
import datetime
import requests
import urllib
import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

t1 = datetime.datetime.now()
print('开始时间:', t1.strftime('%Y-%m-%d %H:%M:%S'))

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

currentroot = os.getcwd()
try:
	os.mkdir('skin')
except FileExistsError:
	pass

# 母网页
url = 'https://lol.qq.com/data/info-heros.shtml'
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
driver.get(url)
eroot = etree.HTML(driver.page_source)
list_url = eroot.xpath('//*[@id="jSearchHeroDiv"]/li/a/@href')

# 子网页列表：全部英雄皮肤链接
list_url_hero =[]
for i in list_url:
    list_url_hero.append('https://lol.qq.com/data/'+i)


# 获取每个英雄的字典={皮肤名称, 皮肤链接}, 并merge合并字典
dic_all_hero = {}
for i, url in enumerate(list_url_hero):
    # debug
    # url = 'https://lol.qq.com/data/info-defail.shtml?id=1'
    # driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
    driver.get(url)
    # driver.maximize_window() # 页面最大化

    # 隐式等待
    driver.implicitly_wait(20)
    
    # 显式等待 
    # interstitial = True
    # while interstitial == True:                         
    #     try:
    #         WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.ID, "skinNAV")))
    #         # WebDriverWait(driver, 20, 0.5).until(EC.element_to_be_clickable((By.ID, "skinNAV")))
    #         interstitial = False
    #     except NoSuchElementException:
    #         interstitial = False
    #     except TimeoutException:
    #         break
    #     finally:
    #         driver.close()

    element = driver.find_element_by_xpath('//*[@id="skinNAV"]/li[2]/a/img')
    driver.execute_script("arguments[0].click();", element)
    eroot = etree.HTML(driver.page_source)
    list_img = eroot.xpath('//*[@id="skinBG"]/li/img/@src')
    list_name_ = eroot.xpath('//*[@id="skinBG"]/li/img/@alt')
    
    list_name = []
    for name in list_name_:
        # 去掉文件名特殊符号
        s = r"[\/\\\*\?\:\？\"\<\>\|\.\+\-\"\（\）\！\“\”\,\。\{\}\=\%\*\~\·\®\$\&\;\[\]\#\@]"
        title_clean = re.sub(s, '', name)
        list_name.append(title_clean)

    dic_one_hero = dict(zip(list_name,list_img))
    
    num=0
    for name, img_url in dic_one_hero.items():
        # print(name,img_url)
        try:
            request = urllib.request.Request(img_url, headers=headers)
            response = urllib.request.urlopen(request)
            img = response.read()
        except urllib.error.HTTPError as e:
            print(e.code)
        except urllib.error.URLError as e:
            print(e.reason)
        else:    
            with open('skin/{}.jpg'.format(name), 'wb') as f:
                f.write(img)
                num += 1
                time.sleep(random.randint(3,5))
                print('已完成下载第{}个图片: {}.jpg'.format(num, name))
            f.close()

    dic_all_hero.update(dic_one_hero)
    time.sleep(random.randint(4,5))

# 耗时计算

# 开始时间
print('开始时间:', t1.strftime('%Y-%m-%d %H:%M:%S'))
# 结束时间
t2 = datetime.datetime.now()
print('结束时间:', t2.strftime('%Y-%m-%d %H:%M:%S'))
delta = t2 - t1

if delta.seconds > 3600:
    if t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] < t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)) + '分'
              + str(delta.seconds % 60) + '秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] == t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)) + '分'
              + '0秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] > t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)-1) + '分'
              + str(delta.seconds % 60) + '秒')
        
elif delta.seconds > 60:
    if t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] < t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))) + '分'
              + str(delta.seconds % 60) + '秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] == t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))) + '分'
              + '0秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] > t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))-1) + '分'
              + str(delta.seconds % 60) + '秒')


