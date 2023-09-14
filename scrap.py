from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
load_dotenv()


def insertdb(name,dictionary):
    uri = os.getenv('db_uri')
    client = MongoClient(uri, server_api=ServerApi('1'))
    beta = client[os.getenv('dbbeta')]
    b_name = beta[os.getenv('list')]
    b_details = beta[os.getenv('collection')]
    b_name.insert_one({'name':name,'time':time.ctime()})
    b_details.insert_one(dictionary)
       
def extract_section_details(sections):
    section_list=[]
    for section in sections:
        d={}
        d['section']=section.find_element(By.TAG_NAME,'span').text
        print(section.find_element(By.TAG_NAME,'span').text)
        d['section_title']=section.text.replace(d['section'],'').strip()
        section.find_element(By.CLASS_NAME,'title').click()
        print('next page')
        windows=driver.window_handles
        for w in windows[1:]:
            driver.switch_to.window(w)
            time.sleep(10)
            d['footnotes']=driver.find_element(By.CLASS_NAME,'panel-body').find_elements(By.TAG_NAME,'p')[1].text
            d['description']=driver.find_element(By.CLASS_NAME,'panel-body').find_elements(By.TAG_NAME,'p')[0].text
            driver.close()
        driver.switch_to.window(parent_window_id)
        time.sleep(6)
        section_list.append(d)
    return section_list

def Act_details():
    Act_detail={}
    Act_detail['Act']=driver.find_element(By.CLASS_NAME,'preambletitle').text
    details={}
    driver.find_element(By.LINK_TEXT,'Actdetails').click()
    rows=driver.find_element(By.CLASS_NAME,'itemDisplayTable').find_elements(By.TAG_NAME,'tr')
    for row in rows:
        value = row.find_elements(By.TAG_NAME,'td')
        details[value[0].text]=value[1].text
    Act_detail['Act_Details']=details
    return Act_detail


url='https://www.indiacode.nic.in/handle/123456789/1631?sam_handle=123456789/1362'

driver=webdriver.Firefox()
driver.get(url)
time.sleep(10)
parent_window_id=driver.current_window_handle

file_name=driver.find_element(By.CLASS_NAME,'preambletitle').text


act=[]
act.append(Act_details())
driver.find_element(By.LINK_TEXT,'Sections').click()
time.sleep(10)
def ext():
    chapters=driver.find_element(By.CLASS_NAME,'col-sm-4').find_elements(By.TAG_NAME,'a')
    for chapter in chapters[2:]:
        chapter_details={}
        print(chapter.text)
        chapter_details['Chapter name']=chapter.text
        chapter.click()
        time.sleep(10)
        driver.find_element(By.NAME,'myTableActChapterIndexSection_length').send_keys('100')
        number_of_pages=int(driver.find_element(By.ID,'myTableActChapterIndexSection_paginate').find_elements(By.TAG_NAME,'a')[-2].text)
        for page in range(number_of_pages):
            section=driver.find_element(By.XPATH,'//*[@id="myTableActChapterIndexSection"]').find_elements(By.TAG_NAME,'td')
            chapter_details['Section']=extract_section_details(section)
            driver.find_element(By.ID,'myTableActChapterIndexSection_next').click() 
        act.append(chapter_details)
        
ext()

driver.close()
dictionary={"act url":url,"act content":act}
insertdb(file_name,dictionary)



