import requests
import selenium
from selenium import webdriver
import pyquery
import tesserocr  
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import bs4
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
import time
import wget

driver = webdriver.Chrome(executable_path="/usr/local/chromedriver/chromedriver4")
driver.get("https://www.douyin.com/discover?modal_id=7117181704892058887")
html = driver.page_source
time.sleep(2)

SoupedHtml=BeautifulSoup(html,features='html.parser')

PatternVideo = re.compile('<source class="" src="//www..*?type="',re.S)
DF_PatternVideo_With_Redundancy = pd.DataFrame(re.findall(PatternVideo, str(SoupedHtml)))
DF_PatternVideo_With_Redundancy
DF_PatternVideo = pd.DataFrame(DF_PatternVideo_With_Redundancy[0].apply(lambda x:x[24:-8]).tolist())

CurrentTime = time.strftime("%Y%m%d_%H:%M:%S", time.localtime()).replace(' ','')
DownloadLink = "http://" + str(DF_PatternVideo.loc[0,0])
DownloadPath='/Users/zhanglu/Desktop/CODE/Formal/Video/'+ str(CurrentTime) + '.mp4'
wget.download(DownloadLink,DownloadPath)

# Loop Below
actions = ActionChains(driver)
ActionChains(driver).key_down(Keys.DOWN).send_keys("s").perform()

driver.get(driver.current_url)
htmlNew = driver.page_source

SoupedHtmlNew=BeautifulSoup(htmlNew,features='html.parser')

PatternVideo = re.compile('<source class="" src="//www..*?type="',re.S)
DF_PatternVideo_With_Redundancy = pd.DataFrame(re.findall(PatternVideo, str(SoupedHtmlNew)))
DF_PatternVideo_With_Redundancy
DF_PatternVideo = pd.DataFrame(DF_PatternVideo_With_Redundancy[0].apply(lambda x:x[24:-8]).tolist())

CurrentTime = time.strftime("%Y%m%d_%H:%M:%S", time.localtime()).replace(' ','')

DownloadLink = "http://" + str(DF_PatternVideo.loc[0,0])
DownloadPath='/Users/zhanglu/Desktop/CODE/Formal/Video/'+ str(CurrentTime) + '.mp4'


wget.download(DownloadLink,DownloadPath)