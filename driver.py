#-*- coding: utf-8 -*-
from re import X
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time, datetime, os, platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By

#현재 폴더 경로 받아옴
path = os.getcwd()

service=(['message', 'accounts', 'contacts', 'schedule', 'communication', 'mail', 'todo',
        'wecrm', 'wepms', 'note', 'approval', 'corporateCard', 'personalCard', 'attendance', 
        'meet', 'companyboard', 'invoice', 'fax', 'sms', 'westudio', 'webot', 'webuilder', 'other'])

serviceTest=({'message': False, 'accounts': False, 'contacts': False, 'schedule': False, 'communication': False, 
        'mail': False, 'todo': False, 'wecrm': False, 'wepms': False, 'note': False, 
        'approval': False, 'corporateCard': False, 'personalCard': False, 'attendance': False, 'meet': False, 
        'companyboard': False, 'invoice': False, 'fax': False, 'sms': False, 'westudio': False, 'webot': False,
        'webuilder' : True, 'other' : True})

ID='id'; CSS='CSS'; CLASS_NAME='class'; TAG_NAME='tag_name'

def wehagoID(version, brand=None) :
    if brand == 3 :
        id = 'vqatest'
    elif brand == 4 :
        id = 'iqatest'
    else :
        if version == 1 :
            if brand == 1 :
                id = 'qatest'
            elif brand == 2 :
                id = 'tqatest'
        elif version == 2 or version == 3 :
            with open(path +'/id.txt') as f:
                id = f.read()
    print(id)
    return id

def chromeBrowser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('--start-maximized')

    if platform.system() == 'Windows' :
        browser = webdriver.Chrome(path + '\\chromedriver.exe', options=chrome_options)
    elif platform.system() == 'Darwin' :
        browser = webdriver.Chrome(path + '/chromedriver', options=chrome_options)

    # # 사이즈 조정 
    # browser.maximize_window()
    return browser

def browser_click (browser, xpath, by=None) :
    if by == CLASS_NAME :
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, xpath))).click()
    elif by == ID :
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, xpath))).click()
    elif by == CSS :
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, xpath))).click()
    else :
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

def btn_click(browser, xpath, text, number=True) :
    btn = browser.find_elements(By.CLASS_NAME, xpath)
    # btn = browser.find_elements_by_class_name(xpath)
    for i in btn :
        if text in i.text :
            i.click()
            time.sleep(0.5)
            if number : break

def li_click(browser, text) :
    # browser.find_element_by_xpath(f'//li[contains(., "{text}")]').click()
    browser.find_element(By.XPATH, f'//li[contains(., "{text}")]').click()
    time.sleep(1)

def browser_sendKey(browser, xpath, text, by=None) :
    if by == CLASS_NAME :
        browser.find_element(By.CLASS_NAME, xpath).send_keys(text)
    elif by == ID :
        browser.find_element(By.ID, xpath).send_keys(text)
    elif by == CSS :
        browser.find_element(By.CSS_SELECTOR, xpath).send_keys(text)
    elif by == TAG_NAME :
        browser.find_element(By.TAG_NAME, xpath).send_keys(text)
    else :
        browser.find_element(By.XPATH, xpath).send_keys(text)
    time.sleep(0.1)

def hasxpath(browser, xpath, by=None) :
    try : 
        if by == CLASS_NAME :
            browser.find_element(By.CLASS_NAME, xpath)
        elif by == CSS :
            browser.find_element(By.CSS_SELECTOR, xpath)
        elif by == ID :
            browser.find_element(By.ID, xpath)
        else :
            browser.find_element(By.XPATH, xpath)
        return True
    except :
        return False

def currentTime() : 
    now = datetime.datetime.now()
    now = now + datetime.timedelta(minutes=5)
    return now

def progress(browser) :
    count = 1
    for i in range(0,30) :
        if count == 30 : 
            browser.refresh()
            time.sleep(5)
            try :
                browser.switch_to_alert()
                browser.switch_to_alert().accept()
            finally : raise Exception('30초 동안 무한로딩중,,')
        if hasxpath(browser, 'WSC_LUXCircularProgress', 'class') :
            time.sleep(1)
            count = count + 1
        else : 
            break
    time.sleep(1)

def checkSerivce(num=None, invoice=None) :
    if num :
        for i in num : 
            serviceTest[service[i]]= True
    else :
        if invoice : 
            for i in service :
                serviceTest[i] = True
        else : 
            for i in service[:-7] :
                serviceTest[i] = True