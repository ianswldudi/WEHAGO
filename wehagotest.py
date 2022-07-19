from cgi import print_environ
from ctypes import wstring_at
import datetime, time, os, sys, platform
from pickle import NONE
from random import randrange
from email.headerregistry import ContentTransferEncodingHeader
from tkinter import E, W
from typing import Protocol, Tuple, final
from numpy.core.fromnumeric import clip, var
from numpy.core.numeric import _rollaxis_dispatcher
from numpy.lib.polynomial import RankWarning
from numpy.lib.twodim_base import vander
from numpy.lib.utils import deprecate
import selenium
from selenium.webdriver import common
from selenium.webdriver.common import keys

from urllib3.packages.six import b
import varname
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.common.exceptions import NoSuchElementException
import pyperclip, clipboard
import re
from driver import browser_click, hasxpath, currentTime, chromeBrowser, wehagoID, btn_click, progress, li_click, browser_sendKey
wehagoBrand = ''; userid = ''
path = os.getcwd()

userList = ([['이름', '통신사', '생년월일', '성별(1,2)', '핸드폰번호', '결제은행'],
        ['김성욱', 'sk', '941105', '1', '01037150653'], ['문지영', 'kt', '950209', '2', '01045681896'],
        ['김성은', 'sk', '900315', '2', '01062906271'], ['한초희', 'kt', '910810', '2', '01092787445'],
        ['박용민', 'kt', '861117', '1', '01028899587'], ['주소라', 'kt', '940926', '2', '01088095036'],
        ['유형록', 'sk', '830625', '1', '01093388179'], ['김신태', 'sk', '830329', '1', '01020718831'],
        ['박종민', 'sk', '910814', '1', '01021737519'], ['길차현', 'sk', '900419', '2', '01050505970'],
        ['김병용', 'sk', '910823', '1', '01099119485']])
userNameList = []

confirm='확인'; save='저장'; delete='삭제'; setting='서비스관리'
WSC_LUXButton = 'WSC_LUXButton '
ID='id'; CSS='CSS'; CLASS_NAME='class'; TAG_NAME='tag_name'

def user() :
    for i in range(len(userList)) :
        userNameList.append(userList[i][0])

def userNumber(name) :
    user()
    return userNameList.index(name)

def enter (browser, xpath, text, by=None, sec=None) :
    if not sec : sec = 1
    browser_sendKey(browser, xpath, text, by)
    time.sleep(sec)
    browser_sendKey(browser, xpath, Keys.ENTER, by)
    time.sleep(1)

def context(browser, xpath, by=None) :
    if by == CLASS_NAME :
        text = browser.find_element(By.CLASS_NAME, xpath).text
    else :
        text = browser.find_element(By.XPATH, xpath).text
    return text

def helperText(browser, xpath, content) : 
    browser_sendKey(browser, xpath, content)
    browser_sendKey(browser, xpath, Keys.TAB)
    time.sleep(1)

def sameText(browser, text) :
    # 중복 팝업 창 문구
    if hasxpath(browser, varname.duplicatePopup) :
        context = browser.find_element(By.XPATH, varname.duplicatePopup).text
        if text in context :
            return True
        else :
            return False
    else :
        return False

def textClear(browser, xpath) :
    text = browser.find_element(By.XPATH, xpath)

    if platform.system() == 'Windows' :
        text.send_keys(Keys.CONTROL + "a")
    elif platform.system() == 'Darwin' :
        text.send_keys(Keys.COMMAND, "a")
    text.send_keys(Keys.DELETE)
    time.sleep(0.5)

def inputUser(browser, xpath, by=None, sec=None) :
    name = usersName(browser)
    if name == '한초희' :
        enter(browser, xpath, '문지영', by, sec)
    else :
        enter(browser, xpath, '한초희', by, sec)
    
def usersName (browser) :
    name = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_userprofile'))).text
    return name[0:3]

def waitseconds(second) :
    for i in range(second,0,-1) :
        print(str(i) + '초남음')
        time.sleep(1)

def address(browser) :
    action = ActionChains(browser)
    action.send_keys(Keys.TAB).send_keys(Keys.ENTER).pause(1).send_keys(' 버들1길130').pause(0.5).send_keys(Keys.ENTER).pause(1)
    action.send_keys(Keys.TAB*3).send_keys(Keys.ENTER).perform()
    action.reset_actions()

def getUrl(service, by=True) :
    url = 'https://www.wehago'
    if by :
        if wehagoBrand == 3 :
            url = url + 'v.com/#/'
        elif wehagoBrand == 2 :
            url = url + 't.com/#/'
        else: 
            url = url + '.com/#/'
        url = url + service
    else :
        if wehagoBrand == 3 :
            url = url + 'v.com/'
        elif wehagoBrand == 2 :
            url = url + 't.com/'
        else: 
            url = url + '.com/'
        url = url + service  + '/#/'
    return url

def progress(browser) :
    count = 1
    for i in range(0,60) :
        if count == 60 : 
            browser.refresh()
            time.sleep(5)
            raise Exception('60초 동안 무한로딩중,,')
        if hasxpath(browser, 'WSC_LUXCircularProgress', CLASS_NAME) :
            time.sleep(1)
            count = count + 1
        else : 
            break
    time.sleep(1)

def checkText(browser, xpath, text) :
    btn = browser.find_elements(By.CLASS_NAME, xpath)
    btnText = []
    for i in btn :
        btnText.append(i.text)
    time.sleep(1)
    if any(text in s for s in btnText):
        return True
    else :
        return False

def pageDown(browser, xpath, by=None) :
    browser_click(browser, xpath, by)
    action = ActionChains(browser)
    action.send_keys(Keys.END).perform()
    action.reset_actions()
    time.sleep(1)

class Common :
    def set_wehagoBrand(self, version, brand) :
        global wehagoBrand
        global userid
        wehagoBrand = brand
        userid = wehagoID(version, brand)

    def fileUpload(self, browser, fileName) :
        f = path + '/' + fileName
        browser.find_element(By.CSS_SELECTOR, 'input[type="file"]').send_keys(f)
        time.sleep(3)

    def setPassword(self, browser) :
        browser.find_element(By.XPATH, '//button[text()="1"]').click()
        browser.find_element(By.XPATH, '//button[text()="2"]').click()
        browser.find_element(By.XPATH, '//button[text()="1"]').click()
        browser.find_element(By.XPATH, '//button[text()="2"]').click()
        browser.find_element(By.XPATH, '//button[text()="1"]').click()
        browser.find_element(By.XPATH, '//button[text()="2"]').click()
        time.sleep(1)
    
    def close(self, browser) :
        action = ActionChains(browser)
        action.send_keys(Keys.ESCAPE).perform()
        action.reset_actions()
        time.sleep(1)

    def searchUser(self, browser, name) :
        enter(browser, '//*[@id="inputSearch-TK"]', usersName(browser))
        browser_click(browser, 'point_color', CLASS_NAME)

    def user(self, browser) :
        id = Company().cs_approvalID(browser)
        path = os.getcwd()
        if platform.system() == 'Windows' :
            browser2 = webdriver.Chrome(path + '\\chromedriver.exe')
        elif platform.system() == 'Darwin' :
            browser2 = webdriver.Chrome(path + '/chromedriver')
        browser2.maximize_window()
        Login().login(browser2, id)
        return browser2

    def tabClose(self, browser) :
        count = len(browser.window_handles)
        if count != 1 :
            for i in range(count, 1, -1) :
                browser.switch_to.window(browser.window_handles[i-1])
                browser.close()
            browser.switch_to.window(browser.window_handles[0])
        browser.refresh()
        time.sleep(5)

    def undistribute(self, browser) :
        Company().cs_open(browser)
        Company().cs_distribution(browser)
        self.tabClose(browser)
        browser.refresh()
        time.sleep(3)

    def canvasClick(self, browser, xpath, xoffset, yoffset, by=None) :
        # x,y 선택하는 canvas
        action = ActionChains(browser)
        if by == CLASS_NAME :
            service = browser.find_element(By.CLASS_NAME, xpath)
        else :
            service = browser.find_element(By.XPATH, xpath)
        action.move_to_element_with_offset(service, xoffset, yoffset).click().perform()
        action.reset_actions()
        time.sleep(3)

class Login :
    def logout(self, browser) :
        browser.get(getUrl('personal'))
        time.sleep(3)
        if '개인설정' in browser.title :
            browser_sendKey(browser, 'btn.btn_userprofile', Keys.ENTER, CLASS_NAME)
            browser_sendKey(browser, 'btn_logout', Keys.ENTER, CLASS_NAME)
            time.sleep(5)
        else : print('로그아웃상태,,')

    def login(self, browser, id) :
        print("login s")
        if id == 'hancho1' :
            browser.get('https://www.wehago.com/#/login')
        else :
            browser.get(getUrl('login'))
        time.sleep(3)
        if '로그인 : WEHAGO' in browser.title :
            #아이디,비밀번호 입력
            browser_sendKey(browser, 'inputId', id, ID)
            if id == 'ianswldudi' or 'qatest' in id : pwd = 'ckacl118*'
            elif id == 'hancho1' or id == 'hancho01' : pwd = '1q2w3e4r!'
            else : pwd = '1q2w3e4r'
            browser_sendKey(browser, 'inputPw', pwd, ID)
            browser_sendKey(browser, 'inputPw', Keys.ENTER, ID)
            time.sleep(1)

            #중복 로그인 창 뜨면 확인 버튼 클릭
            if hasxpath(browser, varname.duplicateBtn) :
                browser_click(browser, varname.duplicateBtn)
            time.sleep(5)

            # 로그아웃 하고 세션 만료 된 경우 새로고침 추가
            if id != browser.get_cookie('h_portal_id')['value'] :
                browser.refresh()
                time.sleep(5)
        else :
            print('로그인 상태')

    def dev_login(self, browser, id) :
        print("login s")
        browser.get('http://dev.wehago.com/#/login')
        time.sleep(5)

        #아이디,비밀번호 입력
        browser.find_element(By.ID, "inputId").send_keys(id)
        browser.find_element(By.ID, "inputPw").send_keys('ckacl118*')

        #로그인 버튼 클릭 
        browser.find_element(By.ID, "inputPw").send_keys(Keys.ENTER)
        #중복 로그인 창 뜨면 확인 버튼 클릭
        if hasxpath(browser, varname.duplicateBtn) :
            browser_click(browser, varname.duplicateBtn)
        time.sleep(10)

    def dev_logout(self, browser) :
        browser.get(getUrl('http://dev.wehago.com/#/company/management/info'))
        time.sleep(3)
        if '회사정보 : 회사정보관리' in browser.title :
            browser_click(browser, 'btn_userprofile', CLASS_NAME)
            browser_click(browser, 'btn_logout', CLASS_NAME)
            time.sleep(5)
        else :
            print('로그아웃상태,,')

    def naver_login(self, browser) :
        browser.execute_script('window.open("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com");')
        time.sleep(3)
        browser.switch_to.window(browser.window_handles[1])
        pyperclip.copy('smile_1896')
        browser_sendKey(browser, 'id', Keys.CONTROL + 'V', ID)
        time.sleep(1)
        pyperclip.copy('ckacl118*')
        browser_sendKey(browser, 'pw', Keys.CONTROL + 'V', ID)
        time.sleep(1)
        browser.find_element(By.ID, 'log.login').click()
        time.sleep(1)

    def inputCompany(self, browser, number) :
        browser.get('http://dev.wehago.com/#/company/management/info')
        time.sleep(5)
        browser_click(browser, varname.modifyCompany)
        browser_click(browser, varname.inputRepresentative)
        action = ActionChains(browser)
        action.send_keys('김병용').send_keys(Keys.TAB).send_keys('722000').pause(1).send_keys(Keys.ENTER).pause(1).send_keys(Keys.TAB*3)
        action.send_keys('02').send_keys(Keys.TAB).send_keys('6233').send_keys(Keys.TAB).send_keys(number).perform()
        action.reset_actions()
        browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[2]/div[2]/div[1]/table/tbody/tr[11]/td/div[1]/div[1]/button')
        time.sleep(1)
        action = ActionChains(browser)
        action.send_keys(' 버들1길 130').pause(1).send_keys(Keys.ENTER).pause(1).send_keys(Keys.TAB*3).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[2]/div[2]/div[3]/button[2]')
        browser_click(browser, varname.confirm)
    
    def og_login(self, browser, version, brand) :
        id = wehagoID(version, brand)
        self.logout(browser)
        self.login(browser, id)

class Other :
    def ot_login(self, browser, version) :
        if version == 1 :
            id = userid + '01'
        else :
            id = 'qatest123'
        Login().logout(browser)
        time.sleep(1)
        Login().login(browser, id)
        time.sleep(1)

    def ot_deleteNote(self, browser) :
        browser.get(getUrl('note', False))
        time.sleep(5)
        while hasxpath(browser, varname.shardNoteList) :
            browser_click(browser, varname.shardNoteList)
            time.sleep(1)
            browser_click(browser, 'btn_edit', CLASS_NAME)
            browser_click(browser, varname.ot_deleteSharedNote)
            browser_click(browser, varname.confirm)
            time.sleep(1)

        if hasxpath(browser, varname.shardNoteList) :
            raise Exception('공유지식공간 삭제 확인 필요')

    def ot_deleteMail(self, browser) :
        browser.get(getUrl('mail'))
        time.sleep(5)
        Mail().ma_deleteMail(browser)

    def ot_deleteMessage(self, browser) :
        browser.get(getUrl('communication2/message/inbox'))
        time.sleep(5)
        Message().ms_deleteReceiveMessage(browser)

    def ot_checkUserCreateIssue(self, browser) :
        browser.get(getUrl('wepms/projectmng'))
        time.sleep(3)
        Wepms().pms_searchProject(browser, varname.name_addUser)
        Wepms().pms_createIssue(browser)

    def ot_checkUserProjectManager(self, browser):
        browser.get(getUrl('wepms/projectmng'))
        time.sleep(5)
        textClear(browser, '//*[@id="project_search_input"]')
        if not Wepms().pms_searchProject(browser, varname.name_userManager) :
            raise Exception('다른 사용자가 프로젝트 매니저일때 확인 필요')

    def ot_checkPostApproval(self, browser) :
        browser.get(getUrl('eapprovals'))
        time.sleep(3)
        Approval().ap_searchApproval(browser, '후결')
        if hasxpath(browser, varname.reject) :
            raise Exception('후결 확인 필요')
        else :
            browser_click(browser, varname.approve)
            time.sleep(1)
            browser_click(browser, varname.checkApproval)
            time.sleep(1)
        time.sleep(1)
    
    def ot_checkMailConnect(self, browser) :
        browser.get(getUrl('mail'))
        time.sleep(5)
        if context(browser, varname.companyMailCreate) == '다음에':
            browser_click(browser, varname.companyMailCreate)
            time.sleep(1)
        enter(browser, varname.mailSearch, 'WEHAGO 화상회의 초대안내')
        time.sleep(5)
        browser_click(browser, 'mail_list_item_0', ID)
        browser_click(browser, varname.meetingMail)
        time.sleep(5)

    def ot_checkTodoAddBoard(self, browser) :
        browser.get(getUrl('todo', False))
        time.sleep(5)
        Todo().td_close(browser)
        browser_click(browser, varname.projectList)
        if hasxpath(browser, varname.addTodoBoard) :
            raise Exception('그룹 관리자 아닌 경우 할일 보드 생성 확인 필요')
    
    def ot_checkTodoDeleteBoard(self, browser) :
        browser.get(getUrl('todo', False))
        time.sleep(5)
        browser_click(browser, varname.projectList)
        time.sleep(1)
        if hasxpath(browser, 'sp_td.op', CLASS_NAME) :
            raise Exception('그룹 관리자 아닌 경우 할일 보드 삭제 확인 필요')

    def ot_participationChat(self, browser) :
        browser.get(getUrl('communication2'))
        time.sleep(5)
        Common().close(browser)
        if hasxpath(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME) : 
            browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
            time.sleep(1)
        browser_click(browser, 'roomSearch', ID)
        time.sleep(3)
        btn_click(browser, 'common_round_btn', '참여요청', False)
        # 한초희 계정으로 대화방 목록 클릭 > 연락처로 만든 대화방에 참여요청 > 마스터한테 잘 보이는지, 수락 시 참여 되는지,
    
    def ot_addUserChat(self, browser) :
        browser.get(getUrl('communication2'))
        time.sleep(5)
        Common().close(browser)
        if hasxpath(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME) : 
            browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
            time.sleep(1)
        Communication().cc_searchChatRoom(browser, '조직도')
        # 김혜린 추가하기
        browser_click(browser, 'icon.ico_member', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '참여자 추가')
        if wehagoBrand == 3 : enter(browser, varname.cc_searchMember, '김성욱')
        else : enter(browser, varname.cc_searchMember, '김혜린')
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        time.sleep(1)

class Company :
    def cs_addEmplyeeDetail(self, browser, name=None, number=None, mail=None) :
        if not mail : mail = 'smile_1896@naver.com'
        browser_click(browser, varname.organizationuser)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '직원등록')
        enter(browser, varname.employeeName, name)
        browser_click(browser, varname.employeeDepartment)
        time.sleep(3)
        browser_click(browser, varname.employeeCompany)
        time.sleep(3)
        if number : browser_sendKey(browser, varname.employeeNumber, number)
        browser_sendKey(browser, varname.employeeMail, mail)
        browser_click(browser, varname.registerEmployeeBtn)
        time.sleep(1)
        browser_click(browser, varname.confirm)
        time.sleep(5)
    
    def addEmpolyeeExcel(self, browser, userInfo: list) :
        browser.get('https://www.wehago.com/#/company/organizationuser')
        time.sleep(5)
        for i in userInfo :
            self.cs_addEmplyeeDetail(browser, name=i[0], mail=i[1], number=i[2])
            time.sleep(1)

    def cs_addEmpolyee(self, browser) :
        name = usersName(browser)
        if name == '한초희' :
            self.cs_addEmplyeeDetail(browser, name='문지영')
        else :
            self.cs_addEmplyeeDetail(browser, name='한초희')
        # 퇴사자용 추가
        self.cs_addEmplyeeDetail(browser, name='주소라')

    def cs_resignation(self, browser) :
        browser_click(browser, varname.organizationuser)
        time.sleep(1)
        enter(browser, '//*[@id="inputSearch"]', '주소라')
        Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div/canvas', 100, 45)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '퇴사')
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        textClear(browser, '//*[@id="inputSearch"]')
        enter(browser, '//*[@id="inputSearch"]', '주소라')
        try :
            if not sameText(browser, '검색결과가 없습니다.') : raise Exception('퇴사 처리 확인 필요')
        finally :
            Common().close(browser)
        
    def cs_searchRetiree(self, browser) :
        browser_click(browser, varname.organizationuser)
        time.sleep(1)
        browser_click(browser, varname.searchRetiree)
        time.sleep(1)
        Common().canvasClick(browser, '//*[@id="gridBase"]/div/canvas', 15, 60)
        if delete != context(browser, '//*[@id="app"]/div/div[2]/div[2]/div[2]/div/button') :
            raise Exception('퇴사자 조회 확인 필요')

    def cs_userDistribution(self, browser) :
        service = browser.find_elements(By.CLASS_NAME, 'choice_market_item')
        # 배포가능한게 있을때만 클릭
        if service :
            for s in service :
                s.click()
                time.sleep(0.1)
            browser_click(browser, varname.serviceDistribution)
        time.sleep(1)

    def cs_distribution(self, browser) :
        browser_click(browser, varname.serviceManagement)
        time.sleep(1)
        browser_click(browser, varname.distribute)
        time.sleep(0.5)
        enter(browser, '//*[@id="inputSearch"]', usersName(browser))
        # 배포가능 서비스 클릭
        self.cs_userDistribution(browser)
        browser_click(browser, varname.undistributedService)
        # 입력되어 있는 내용 지우기
        textClear(browser, '//*[@id="inputSearch"]')
        inputUser(browser, '//*[@id="inputSearch"]')
        # 배포가능 서비스 클릭
        self.cs_userDistribution(browser)

    def cs_setAdministor(self, browser) :
        browser_click(browser, varname.companyManagement)
        browser_click(browser, varname.administor)
        time.sleep(1)
        service = browser.find_elements(By.CLASS_NAME, 'choice_market_item')
        time.sleep(1)
        print(len(service))
        if service :
            for s in service :
                s.click()
                time.sleep(1)
                if usersName(browser) == '한초희' :
                    browser_click(browser, 'memberbx_1', ID)
                else :
                    browser_click(browser, 'memberbx_0', ID)
                browser_click(browser, varname.addAdministor)
                time.sleep(1)
                text = '이미 관리자로 설정된 사용자 입니다.'
                if sameText(browser, text) :
                    browser_click(browser, varname.confirm)
                else :
                    browser_click(browser, varname.saveAdministorBtn)
                time.sleep(1.5)

    def cs_domainRegister(self, browser) :
        browser_click(browser, varname.domainSetting)
        browser_click(browser, varname.registerDomain)
        browser_click(browser, 'domain_bx.purchase', CLASS_NAME)
        browser_click(browser, varname.confirmDomain)
        address = 'qatest' + currentTime().strftime('%m%d%M') + '.co.kr'
        enter(browser, varname.domainAddress, address)
        time.sleep(1)
        browser_click(browser, varname.selectDomain)
        browser_click(browser, varname.nextDomain)
        browser_click(browser, varname.inputDomain)
        action = ActionChains(browser)
        action.send_keys('1111111119').send_keys(Keys.TAB).send_keys('테스트'+currentTime().strftime('%m%d')).send_keys(Keys.TAB).send_keys('qatest'+currentTime().strftime('%m%d'))
        action.send_keys(Keys.TAB).send_keys('korea').send_keys(Keys.TAB*2).send_keys('smile_1896@naver.com').send_keys(Keys.TAB).send_keys('0262333301')
        action.send_keys(Keys.TAB*2).send_keys(Keys.ENTER).pause(1).send_keys('버들1길 130').send_keys(Keys.ENTER).pause(1).send_keys(Keys.TAB*3).send_keys(Keys.ENTER).pause(1).send_keys(Keys.TAB*4).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        browser_click(browser, varname.adminInfo)
        browser_click(browser, varname.agreementDomain)
        browser_click(browser, varname.nextDomain)
        time.sleep(1)
        # browser_click(browser, varname.domainPayOthers)
        # browser_click(browser, 'inputElement', ID)
        # browser_click(browser, '//*[@id="scrollElement"]/div/ul/div/li')
        browser_click(browser, varname.agreementDomain2)
        browser_click(browser, varname.paymentDomain)
        time.sleep(1)
        Pay().pay_shinhan(browser)
        # 파일에 도메인 주소 쓰기
        path = os.getcwd()
        f = open(path+'/domain.txt', 'w')
        f.write(address)
        f.close()
        time.sleep(5)
        browser_click(browser, varname.domainManagement)
        
    def cs_useCompanyMail(self, browser) :
        browser_click(browser, varname.domainSetting)
        browser_click(browser, varname.useCompanyMail)
        browser_click(browser, varname.confirm)
        time.sleep(1)
        browser_click(browser, varname.statusCheck)
        time.sleep(3)
        browser_click(browser, varname.companyMailConfirm)
        browser_click(browser, varname.confirm)
        browser.refresh()
        time.sleep(3)

    def cs_distributeDomain(self, browser) :
        browser_click(browser, varname.domainSetting)
        browser_click(browser, varname.distributeDomain)
        Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div/canvas', 16, 16)
        browser_click(browser, varname.serviceDistribute)
        browser_click(browser, varname.confirm)
        browser.refresh()
        time.sleep(3)

    def cs_sharedMailSetting(self, browser) :
        browser_click(browser, varname.domainSetting)
        time.sleep(1)
        browser_click(browser, varname.sharedMailSetting)
        browser_click(browser, 'box_area.add_new', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.sharedMailAddress)
        action = ActionChains(browser)
        action.send_keys('wehago' + currentTime().strftime('%H%M')).send_keys(Keys.TAB*4).send_keys(currentTime().strftime('%m%d')+'테스트으').send_keys(Keys.TAB).send_keys('공용메일확인').perform()
        action.reset_actions()
        browser_click(browser, varname.sharedMailAddUser)
        time.sleep(1)
        browser_click(browser, varname.sharedMailAddButton)
        browser_click(browser, varname.sharedMailConfirm)
        browser_click(browser, 'sp_cs.edit', CLASS_NAME)
        time.sleep(1)

    def cs_billingManagement(self, browser) :
        browser_click(browser, varname.managementPlan)
        time.sleep(1)
        browser_click(browser, varname.billingInformation)
        browser_click(browser, varname.registerPayment)
        browser_click(browser, varname.authenticationButton)
        browser_click(browser, varname.confirm)
        while True :
            waitseconds(15)
            browser_click(browser, varname.authConfirm)
            if sameText(browser, '정확한 인증번호를 입력해주세요.') :
                browser_click(browser, varname.confirm)
            else :
                break
        # 간편 비밀번호 설정
        Common().setPassword(browser)
        # 간편 비밀번호 재확인
        Common().setPassword(browser)
        browser_click(browser, varname.confirm)
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[1])
        browser_click(browser, varname.payAgree)
        browser_click(browser, varname.payNext)
        action = ActionChains(browser)
        action.send_keys(Keys.TAB).send_keys('5594').send_keys(Keys.TAB).send_keys('1000').send_keys(Keys.TAB).send_keys('0563').send_keys(Keys.TAB).send_keys('5916')
        action.send_keys(Keys.TAB).pause(0.5).send_keys(Keys.DOWN*2).send_keys(Keys.TAB*2).send_keys('2025').send_keys(Keys.TAB).send_keys('950209').send_keys(Keys.TAB).send_keys('31').perform()
        action.reset_actions()
        browser_click(browser, 'bpTerms5', ID)
        browser_click(browser, 'btn_confirm', CLASS_NAME)
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[0])

    def cs_open(self, browser, type=None) :
        if wehagoBrand == 2 :
            browser.execute_script('window.open("https://www.wehagot.com/#/company/management");')
        elif wehagoBrand == 3 :
            browser.execute_script('window.open("https://www.wehagov.com/#/company/management");')
        else :
            browser.execute_script('window.open("https://www.wehago.com/#/company/management");')
        time.sleep(3)
        if type : 
            browser.switch_to.window(browser.window_handles[type])
        else :
            browser.switch_to.window(browser.window_handles[1])

    def cs_approvalID(self, browser, type=None) :
        # 새탭열기
        self.cs_open(browser, type)
        browser_click(browser, varname.organizationuser)
        time.sleep(1)
        inputUser(browser, '//*[@id="inputSearch"]')
        Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div/canvas', 100, 45)
        time.sleep(1)
        id = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/span'
        approvalId = context(browser, id)
        if not type :
            Common().tabClose(browser)
        else :
            browser.close()
            browser.switch_to_window(browser.window_handles[type-1])
        return approvalId

class Communication : 
    contacts='연락처'; organization='조직도'; inp='입력'
    def cc_createRoom(self, browser, room) :
        Common().close(browser)
        if hasxpath(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME) : 
            browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
            time.sleep(1)
        browser_click(browser, 'button_new', CLASS_NAME)
        time.sleep(0.5)
        browser_click(browser, varname.newGroupChat)
        time.sleep(3)
        browser_sendKey(browser, varname.groupChatName, '메신저그룹'+room+'생성')
        browser_sendKey(browser, varname.groupChatName, Keys.TAB)
        time.sleep(1)
        #대화방이 정상적으로 삭제되지 않아 동일한 대화방명이 있는 경우
        if context(browser, varname.isGroupChatName) != '사용 가능한 대화방명 입니다.' :
            browser_sendKey(browser, varname.groupChatName, str(currentTime())[11:16])
        time.sleep(1)
        
        #검색 허용
        browser_click(browser, 'WSC_LUXCheckBox', CLASS_NAME)

        # 사용자 추가
        if room == self.contacts :
            self.cc_addUserByContacts(browser)
        elif room == self.organization :
            self.cc_addUserByOrganization(browser)
        else :
            self.cc_addUserByInput(browser)
        btn_click(browser, 'common_round_btn.blue.btn38', '대화시작')
        time.sleep(3)

        if hasxpath(browser, varname.cc_noneUser) :
            browser.refresh()
            time.sleep(5)
            self.cc_createRoom(browser, room)

        if context(browser, varname.duplicateMessage) == '동일한 그룹이름이 존재합니다.' :
            browser_click(browser, varname.confirmMessage2)
            raise Exception('메신저 대화방 생성 확인필요')
        
        time.sleep(1)
        try : self.cc_searchChatRoom(browser, room)
        except : self.cc_createRoom(browser, room)

    def cc_addUserByContacts(self, browser) :
        btn_click(browser, 'common_round_btn', '주소록')
        time.sleep(1)
        browser_click(browser, 'destitem.ico4', CLASS_NAME)
        time.sleep(3)
        # 연락처에 김혜린없어서 대화방 생성 안된경우
        if not hasxpath(browser, '//*[@id="contact_0"]/button') :
            browser.execute_script('window.open("'+getUrl('contacts')+'");')
            time.sleep(5)
            browser.switch_to.window(browser.window_handles[1])
            Contacts().ct_registerContacts(browser)
            time.sleep(1)
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            Common().close(browser)
        else : 
            browser_click(browser, '//*[@id="contact_0"]/button')
            btn_click(browser, WSC_LUXButton, '추가')
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(1)

    def cc_addUserByOrganization(self, browser) :
        btn_click(browser, 'common_round_btn', '주소록')
        time.sleep(1)
        inputUser(browser, '//*[@id="inputSearch-TK"]')
        if '검색결과가 없습니다.' in context(browser, varname.duplicatePopup) :
            browser_click(browser, varname.confirm)
            Common().close(browser)
            raise Exception('가입확인,,')
        browser_click(browser, 'point_color', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, '추가')
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)

    def cc_addUserByInput(self, browser) :
        if wehagoBrand == 3 :
            enter(browser, varname.cc_addUserInput, '김성욱', sec=3)
        else :
            enter(browser, varname.cc_addUserInput, '김혜린', sec=3)

    def cc_createRoomByContacts(self, browser) :
        self.cc_createRoom(browser, self.contacts)

    def cc_createRoomByOrganization(self, browser) :
        self.cc_createRoom(browser, self.organization)

    def cc_createRoomByInput(self, browser) :
        self.cc_createRoom(browser, self.inp) 

    def cc_sendChat (self, browser) :
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(3)
        
        browser_click(browser, 'mentiony-content.chat', CLASS_NAME)
        action = ActionChains(browser)
        action.send_keys('1').send_keys(Keys.ENTER).pause(1).send_keys('2').send_keys(Keys.ENTER).pause(1).send_keys('3').send_keys(Keys.ENTER).pause(1).send_keys('4').send_keys(Keys.ENTER).pause(1).perform()
        action.send_keys('5').send_keys(Keys.ENTER).pause(1).send_keys('6').send_keys(Keys.ENTER).pause(1).send_keys('7').send_keys(Keys.ENTER).pause(1).send_keys('8').send_keys(Keys.ENTER).pause(1).perform()

        name = usersName(browser)
        browser_click(browser, 'mentiony-content.chat', CLASS_NAME)
        action = ActionChains(browser)
        action.send_keys('@').send_keys(name).pause(1).send_keys(Keys.ENTER).send_keys('자동 테스트 대화방 Contacts').perform()
        action.reset_actions()
        browser_click(browser, 'chat_menuitem.ico_emoji', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.emojiBtn)
        browser_click(browser, 'emoji_inner.emoji_1f643', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.sendChatBtn)
        time.sleep(3)

        if hasxpath(browser, 'LUX_basic_btn.btn_chat_func.resend', CLASS_NAME) :
            raise Exception('대화 전송 확인 필요')
        browser_click(browser, 'chat_menuitem.ico_emoji', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, '//*[@id="chatInputBox"]/div/div[2]/div[2]/div/div/ul/li[1]')
        browser_click(browser, 'charemo_inner.we_tired', CLASS_NAME)
        if hasxpath(browser, 'LUX_basic_btn.btn_chat_func.resend', CLASS_NAME) :
            raise Exception('대화 전송 확인 필요')
        time.sleep(3)

    def cc_moreBtn(self, browser, xpath) :
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'chat_inner', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, xpath, CLASS_NAME)
        time.sleep(1)

    def cc_copyChat(self, browser) :
        self.cc_moreBtn(browser, 'btn_new_copy')
        time.sleep(3)
        chat = clipboard.paste()          
        browser_click(browser, 'mentiony-content.chat', CLASS_NAME)
        action = ActionChains(browser)
        action.send_keys(chat).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(1)
        chat = browser.find_elements(By.CLASS_NAME, 'co_balloon_box')
        if chat[0].text != chat[-1].text :
            raise Exception('메신저 복사 확인 필요')

    def cc_addNotice(self, browser) :
        time.sleep(1)
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'chat_inner', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, 'btn_new_func', CLASS_NAME)
        notice = browser.find_element(By.CLASS_NAME, 'chat_inner')
        action = ActionChains(browser)
        action.move_by_offset.move_to_element_with_offset(notice, 50, 10).click().perform()
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)
        if not hasxpath(browser, 'notice_topbox.single', CLASS_NAME) :
            raise Exception('공지 등록 확인 필요')

        browser_click(browser, 'tabitem.ico_noti', CLASS_NAME)
        time.sleep(1)
        if '1' not in context(browser, 'search_result', CLASS_NAME) :
            raise Exception('공지 등록 확인 필요')
        
        browser_click(browser, 'item_btn', CLASS_NAME)
        time.sleep(1)
        if not hasxpath(browser, 'common_round_btn', CLASS_NAME) :
            browser.refresh()
            time.sleep(5)
            raise Exception('공지 모아보기 상세 확인')
        else : 
            btn_click(browser, 'common_round_btn', '목록')
            time.sleep(1)

    def cc_addComment(self, browser) :
        time.sleep(1)
        self.cc_moreBtn(browser, 'btn_new_reply')
        enter(browser, 'mentiony-content.input_comment_msgbox.reply_inputbox.chat', '댓글댓글', CLASS_NAME)
        time.sleep(3)
        if hasxpath(browser, 'empty_area', CLASS_NAME) :
            raise Exception('메신저 댓글 확인 필요')

        # 해당 댓글로 이동되는지 확인
        browser_click(browser, '//*[@id="comment_chat"]/div/a/div[2]/p/div')
        time.sleep(1)
        if not hasxpath(browser, 'cochat_findtext', CLASS_NAME) :
            raise Exception('메신저 댓글 이동 확인 필요')        

    def cc_addReaction(self, browser) :
        # !! 여기 
        self.cc_moreBtn(browser, 'btn_new_reaction')
        time.sleep(1)
        browser_click(browser, 'emoji_inner.emoji_1f600', CLASS_NAME)
        
        if not hasxpath(browser, 'btn_reaction my_reaction', CLASS_NAME) :
            raise Exception('메신저 반응 확인 필요')
    
    def cc_sharedChat(self, browser) :
        self.cc_moreBtn(browser, 'listitem.icon_func1')
        time.sleep(1)
        enter(browser, varname.sharedChat, self.contacts)
        if hasxpath(browser, 'list_item.type2', CLASS_NAME) :
            browser_click(browser, 'list_item.type2', CLASS_NAME)
            browser_click(browser, 'common_round_btn.blue.btn38', CLASS_NAME)
            time.sleep(3)
            self.cc_searchChatRoom(browser, self.contacts)

            time.sleep(1)
            chat = browser.find_elements(By.CLASS_NAME, 'co_balloon_box')
            if not chat :
                raise Exception('메신저 공유 확인 필요')
        else : raise Exception('대화방 확인 필요')

    def cc_appending(self, browser, className, btn) :
        if hasxpath(browser, className, CLASS_NAME) :
            browser_click(browser, className, CLASS_NAME)
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, btn)
            time.sleep(1)
        else :
            Common().close(browser)
            raise Exception(btn + '확인 필요')
        time.sleep(1)      

    def cc_appendingAccount(self, browser) :
        # 거래처 첨부
        time.sleep(3)
        browser_click(browser, 'chat_menuitem.ico_more', CLASS_NAME)
        browser_click(browser, 'moreitem_btn.ico_spondent', CLASS_NAME)
        time.sleep(3)
        self.cc_appending(browser, 'sp_diana', '거래처 첨부')

    def cc_appendingContact(self, browser) :
        # 연락처 첨부
        time.sleep(1)
        browser_click(browser, 'chat_menuitem.ico_more', CLASS_NAME)
        browser_click(browser, 'moreitem_btn.ico_contact', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, 'sp_diana', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[1]/div[3]/div[4]/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/button')

    def cc_appendingSchedule(self, browser) :
        Common().close(browser)
        # 일정 첨부
        time.sleep(1)
        browser_click(browser, 'chat_menuitem.ico_more', CLASS_NAME)
        browser_click(browser, 'moreitem_btn.ico_schedule', CLASS_NAME)
        time.sleep(3)
        self.cc_appending(browser, 'item_text', '일정첨부')
        time.sleep(1)
        btn_click(browser, 'common_round_btn', '서비스 이동', CLASS_NAME)

        # cal = browser.find_element(By.CLASS_NAME, 'LS_icons.small.hasbg.bg_purple.svc_ca')
        # action = ActionChains(browser)
        # action.move_to_element_with_offset(cal, 0, 170).click().perform()
        # time.sleep(5)
        browser.switch_to.window(browser.window_handles[1])
        if '일정관리' not in browser.title :
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            raise Exception('메신저 일정관리 서비스이동 확인 필요')

        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(1)
        
    def cc_appendingMeet(self, browser) :
        # 화상회의 
        time.sleep(1)
        browser_click(browser, 'chat_menuitem.ico_more', CLASS_NAME)
        browser_click(browser, 'moreitem_btn.ico_rtc', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
        
        time.sleep(3)
        # 대화방에서 화상회의 시작으로 찍히는지 확인
        if '화상회의 시작' != context(browser, 'topbox.video', CLASS_NAME) :
            raise Exception('메신저 화상회의 시작 확인 필요')
        browser.switch_to.window(browser.window_handles[1])
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        Meet().meet_documentShare(browser)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        browser.refresh()
        time.sleep(10)
        if '화상회의 종료' != context(browser, 'topbox.video_disabled', CLASS_NAME) :
            raise Exception('메신저 화상회의 종료 확인 필요')

    def cc_vote(self, browser) :
        browser_sendKey(browser, varname.cc_voteName, '메신저에서 투표생성')
        browser_sendKey(browser, varname.cc_vote1, '투표합시다1')
        browser_sendKey(browser, varname.cc_vote2, '투표합시다2')
        browser_click(browser, varname.cc_createVoteBtn)
        time.sleep(1)

    def cc_appendingVote(self, browser) :
        # 투표
        browser_click(browser, 'chat_menuitem.ico_more', CLASS_NAME)
        browser_click(browser, 'moreitem_btn.ico_vote', CLASS_NAME)
        time.sleep(1)
        self.cc_vote(browser)
        browser_click(browser, 'vote_title', CLASS_NAME)
        time.sleep(1)
        vote = browser.find_elements(By.CLASS_NAME, 'vote_text_box')
        vote[-1].click()
        btn_click(browser, WSC_LUXButton, '투표하기')
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '투표 종료')
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)

        if '투표 종료' not in context(browser, 'vote_title', CLASS_NAME) :
            raise Exception('메신저 투표 확인 필요')

    def cc_listVote(self, browser) :
        browser_click(browser, 'tabitem.ico_poll', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, 'common_round_btn.blue ', '투표등록')
        self.cc_vote(browser)
        browser_click(browser, 'section_item.pollitem', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'polllist_item', CLASS_NAME)
        btn_click(browser, 'common_round_btn.blue', '투표하기')
        time.sleep(1)
        btn_click(browser, 'common_round_btn', '투표종료')
        btn_click(browser, 'common_round_btn', '목록')
        time.sleep(1)
        if not hasxpath(browser, 'subject_label.end', CLASS_NAME) :
            raise Exception('투표 탭에서 투표 확인 필요')
    
    def cc_appendingVideo(self, browser) :
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)
        # 비디오 첨부
        browser_click(browser, 'chat_menuitem.ico_more', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'moreitem_btn.ico_filevideo', CLASS_NAME)
        time.sleep(1)
        browser_sendKey(browser, varname.cc_link, 'https://www.youtube.com/watch?v=e2hfX_Yr6Wg')
        time.sleep(1)
        browser_click(browser, varname.cc_linkBtn)
        time.sleep(1)

    def cc_uploadLocal(self, browser) :
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(3)
        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        time.sleep(1)
        Common().fileUpload(browser, '_1ReadME.txt')
        time.sleep(1)
        Common().fileUpload(browser, 'btn_webot.png')
        time.sleep(1)
        browser_click(browser, 'tabitem.ico_file', CLASS_NAME)
        time.sleep(1)
        if hasxpath(browser, 'empty_area', CLASS_NAME) :
            Common().close(browser)
            raise Exception('파일 첨부 확인 필요')
        browser_click(browser, 'imgitem.ico_2', CLASS_NAME)
        # 웹스토리지에 저장
        browser_click(browser, '//*[@id="sectionFileList"]/div/div[3]/div/button[2]')
        time.sleep(1)
        browser_click(browser, '//*[@id="weDriveForm2"]/div[1]/div[2]/div/div/div[1]/div[2]/div/button[2]')
        progress(browser)
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)

    def cc_uploadWedrive(self, browser) :
        Common().close(browser)
        browser_click(browser, 'chat_menuitem.ico_more', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'moreitem_btn.ico_storage', CLASS_NAME)
        time.sleep(1)
        if hasxpath(browser, '//*[@id="WeDriveTableList"]/div[1]/div[1]/span') :
            browser_click(browser, '//*[@id="WeDriveTableList"]/div[1]/div[1]/span')
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(10)
        else :
            btn_click(browser, WSC_LUXButton, '취소')
            time.sleep(0.5)
            raise Exception('메신저 웹스토리지 파일 첨부 확인 필요')

    def cc_uploadFileTab(self, browser) :
        browser_click(browser, 'tabitem.ico_file', CLASS_NAME)
        time.sleep(1)
        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        time.sleep(3)
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)

    def cc_fileName(self, browser) :
        fileList = []
        for i in range(1,10) :
            filename = '//*[@id="sectionFileList"]/div/div['
            filename = filename + str(i) + ']/a/div[2]/div[1]/div[1]/div'   
            if hasxpath(browser, filename) :
                fileList.append(browser.find_element(By.XPATH, filename).text)
            else :
                break
        return fileList

    def cc_collectFile(self, browser) :
        browser_click(browser, 'tabitem.ico_file', CLASS_NAME)
        time.sleep(1)
        defaultFile = self.cc_fileName(browser)
        try :
            # 오래된 순으로 정렬
            browser_click(browser, varname.cc_order)
            time.sleep(1)
            browser_click(browser, varname.cc_oldOrder)
            time.sleep(3)
            oldFile = self.cc_fileName(browser)
            if list(reversed(defaultFile)) != oldFile :
                raise Exception('오래된 순 파일 정렬 확인 필요')
            # 보기방식 변경
            browser_click(browser, 'imgitem.ico_2', CLASS_NAME)
            time.sleep(3)
            if not hasxpath(browser, 'section_filelist.st_listfiles', CLASS_NAME) :
                raise Exception('메신저 보기방식 변경 확인 필요')
            # 이미지 있는지 확인
            browser_click(browser, 'LUX_basic_select.LUX_renewal.filetype', CLASS_NAME)
            time.sleep(1) 
            browser_click(browser, varname.cc_image)
            time.sleep(3)
            if not checkText(browser, 'title', 'btn_webot.png') :
                raise Exception('메신저 이미지 파일 확인 필요')
        finally :
            Common().close(browser)
            browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
            time.sleep(1)

    def cc_deleteChat(self, browser) :
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)
        browser_sendKey(browser, 'body', Keys.HOME, TAG_NAME)
        time.sleep(1)
        btn = browser.find_elements(By.CLASS_NAME, 'chat_inner')
        btn[1].click()
        browser_click(browser, 'listitem.icon_func5', CLASS_NAME)
        time.sleep(1)
        btn_click(browser,WSC_LUXButton, confirm)
        if not hasxpath(browser, 'co_delmsg_box.co_sp2x_bf', CLASS_NAME) :
            raise Exception('메시지 대화 삭제 확인 필요')
    
    def cc_openWebOffice(self, browser) :
        if wehagoBrand == 3 :
            print('wehagov 오피스 미제공')
        else :
            Common().close(browser)
            browser.refresh()
            time.sleep(5)
            browser_click(browser, 'attach_filebg.image_alignment', CLASS_NAME)
            time.sleep(1)
            filename = browser.find_element(By.CLASS_NAME, 'title_filename.ellipsis').text
            browser_click(browser, 'LS_btn.Small.basic', CLASS_NAME)
            time.sleep(10)
            browser.switch_to.window(browser.window_handles[1])
            if filename not in browser.title :
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
                raise Exception('메신저 웹오피스 확인 필요')

            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            Common().close(browser)

    def cc_recentChat(self, browser) :
        browser.refresh()
        time.sleep(10)
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'co_container.renewal.new_st.dz_font', CLASS_NAME)
        browser_sendKey(browser, 'body', Keys.HOME, TAG_NAME)
        time.sleep(3)
        if not hasxpath(browser, 'recently_chat_btn', CLASS_NAME) :
            raise Exception('최신대화 이동버튼 확인 필요')
        else :
            browser_click(browser, 'recently_chat_btn', CLASS_NAME)
            time.sleep(1)
            if  hasxpath(browser, 'recently_chat_btn', CLASS_NAME) :
                raise Exception('메신저 최신 대화로 이동 확인 필요')
        time.sleep(1)

    def cc_searchChat(self, browser) :
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)
        enter(browser, '//*[@id="search_input"]', 'Contacts')
        time.sleep(3)
        
        if hasxpath(browser, 'empty_area', CLASS_NAME) :
            browser.refresh()
            time.sleep(5)
            raise Exception('대화 검색 확인 필요')
        browser_click(browser, 'content_box', CLASS_NAME)
        time.sleep(1)
        if not hasxpath(browser, 'cochat_findtext', CLASS_NAME) :
            raise Exception('대화 검색 후 이동 확인 필요')

    def cc_searchChatRoom(self, browser, room) :
        browser_click(browser, 'roomSearch', ID)
        time.sleep(3)
        enter(browser, varname.cc_searchChatRoom, room)
        if hasxpath(browser, 'empty_txt.v2', CLASS_NAME) : 
            Common().close(browser)
            raise Exception('해당 대화방 없음!')
        else :
            btn_click(browser, 'common_round_btn', '바로가기')

    def cc_settingGroup(self, browser) :
        browser_click(browser, 'tabitem.ico_chat', CLASS_NAME)
        time.sleep(1)
        for i in range(0,2) :
            # 공개로 변경 > 비공개로 변경
            browser_click(browser, 'icon.ico_set', CLASS_NAME)
            time.sleep(1)
            browser_click(browser, 'WSC_LUXToggle', CLASS_NAME)
            browser_click(browser, varname.cc_saveSetting)
            time.sleep(3)
        browser.refresh()
        time.sleep(10)
        
        if not checkText(browser, 'chat_new_notibox', '공개 대화방으로 변경') :
            raise Exception('그룹 설정 변경 확인 필요')

    def cc_searchMention(self, browser) :
        browser_click(browser, 'moreTalkItem', ID)
        time.sleep(5)
        if not hasxpath(browser, 'threaditem', CLASS_NAME) :
            browser.get(getUrl('communication2'))
            time.sleep(5)
            raise Exception('메신저 멘션 확인 필요')

        browser_click(browser, 'threaditem', CLASS_NAME)
        time.sleep(1)
        if '멘션 및 댓글' in context(browser, 'title_txt.ellipsis', CLASS_NAME) :
            raise Exception('메신저 멘션이동 확인 필요')

    def cc_searchGroup(self, browser) :
        browser_click(browser, 'grp_search', CLASS_NAME)
        time.sleep(1)
        enter(browser, varname.cc_searchGroup, '연락처')
        if hasxpath(browser, 'empty_area',' class') :
            raise Exception('대화방 생성 확인 필요')

    def chatCount(self, browser) :
        chat = browser.find_elements(By.CLASS_NAME, 'title_box')
        for i in chat :
            if '즐겨찾는 대화' in i.text :
                text = re.sub('\n즐겨찾는 대화', '',i.text)
                break
        return text

    def cc_favoriteConversation(self, browser) :
        browser_click(browser, 'list_item', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'button_more', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.cc_favorite)
        time.sleep(1)
        count = self.chatCount(browser)
        if count == '0' :
            raise Exception('즐겨찾기 추가 확인 필요')

    def cc_unfavoriteConversation(self, browser) :
        browser_click(browser, 'list_item', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'button_more', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.cc_favorite)
        browser_click(browser, varname.confirm_ms)
        time.sleep(1)
        count = self.chatCount(browser)
        if count != '0' :
            raise Exception('즐겨찾기 해제 확인 필요')
        time.sleep(1)
    
    def cc_checkUserProfile(self, browser) :
        Common().close(browser)
        if not hasxpath(browser, 'icon.ico_member', CLASS_NAME) :
            browser.refresh()
            time.sleep(5)
        browser_click(browser, 'icon.ico_member', CLASS_NAME)
        browser_click(browser, 'user_1', ID)
        browser_click(browser, '//*[@id="participant_menu_1"]/div/div/ul/li[1]')
        time.sleep(1)
        
        if not hasxpath(browser, 'LSnamecard_wrap', CLASS_NAME) :
            raise Exception('메신저 프로필 확인 필요')
        Common().close(browser)

    def cc_master(self, browser) :
        Common().close(browser)
        browser_click(browser, 'icon.ico_member', CLASS_NAME)
        time.sleep(1)
        inputUser(browser, varname.cc_searchUser)
        browser_click(browser, 'user_0', ID)
        browser_click(browser, '//*[@id="participant_menu_0"]/div/div/ul/li[3]')
        time.sleep(1)

    def cc_setAsMaster(self, browser) :
        self.cc_searchChatRoom(browser, self.organization)
        # 마스터로 설정
        self.cc_master(browser)
        master = browser.find_elements(By.CLASS_NAME, 'label_lv.master')
        if len(master) != 2 : raise Exception('메신저 마스터 설정 확인 필요')
        time.sleep(1)
        # 마스터 해제
        self.cc_master(browser)
        master = browser.find_elements(By.CLASS_NAME, 'label_lv.master')
        if len(master) != 1 : raise Exception('메신저 마스터 해제 확인 필요')
        
    def cc_leaveChatRoom (self, browser, option=None) :
        Common().close(browser)
        while hasxpath(browser, 'icon.ico_member', CLASS_NAME) :
            time.sleep(1)
            browser_click(browser, 'icon.ico_member', CLASS_NAME)
            time.sleep(0.5)
            # browser_click(browser, 'user_1', ID)
            member = browser.find_elements(By.CLASS_NAME, 'item_box')
            leave = browser.find_elements(By.CLASS_NAME, 'sp_co_v2.icon_leave')
            member.reverse()
            leave.reverse()
            for i in range(len(member)) :
                member[i].click()
                time.sleep(1)
                leave[i].click()
                btn_click(browser, WSC_LUXButton, confirm)
                time.sleep(1)
            time.sleep(1)
            if option : break
    
    def cc_exportUser(self, browser) :
        Common().close(browser)
        if hasxpath(browser, 'icon.ico_member', CLASS_NAME) :
            browser_click(browser, 'icon.ico_member', CLASS_NAME)
            btn_click(browser, WSC_LUXButton, '일괄내보내기')
            time.sleep(0.5)
            browser_click(browser, 'common_round_btn.button_select_all', CLASS_NAME)
            btn_click(browser, WSC_LUXButton, '일괄내보내기')
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(3)
            btn_click(browser, WSC_LUXButton, '목록 돌아가기')
            if hasxpath(browser, 'user_1', ID) :
                raise Exception('일괄 내보내기 확인 필요')
            time.sleep(1)
            self.cc_leaveChatRoom(browser, True)
        else :
            print('대화방 없음??')

    def cc_willAccept(self, browser, accept) :
        browser_click(browser, 'icon.ico_member', CLASS_NAME)
        time.sleep(3)
        try :
            if checkText(browser, WSC_LUXButton, '참여자 추가') :
                if not hasxpath(browser, 'rnbset_alram', CLASS_NAME) :
                    raise Exception('메신저 참여자 추가 확인 필요')
                else :
                    btn_click(browser, WSC_LUXButton, accept)
                    time.sleep(3)
            else :
                self.cc_willAccept(browser, accept)
        finally : Common().close(browser)
        
    def cc_acceptInvitedUser(self, browser) :
        self.cc_searchChatRoom(browser, self.organization)
        self.cc_willAccept(browser, '수락')
        time.sleep(3)

        if context(browser, 'member_counter', CLASS_NAME) != '3' :
            raise Exception('메신저 참여자 추가 수락 확인 필요')

    def cc_acceptParticipation(self, browser) :
        self.cc_searchChatRoom(browser, self.contacts)
        self.cc_willAccept(browser, '수락')
        time.sleep(3)

        if context(browser, 'member_counter', CLASS_NAME) != '3' :
            raise Exception('참여요청 수락 확인 필요')

    def cc_refusalParticipation(self, browser) :
        self.cc_searchChatRoom(browser, self.inp)
        self.cc_willAccept(browser, '거절')
        time.sleep(3)

        if context(browser, 'member_counter', CLASS_NAME) != '2' :
            raise Exception('참여요청 거절 확인 필요')

    def cc_createChat(self, browser) :
        Common().close(browser)
        browser_click(browser, 'button_new', CLASS_NAME)
        time.sleep(0.5)
        browser_click(browser, varname.newChat)
        inputUser(browser, '//*[@id="inputSearch-TK"]')
        browser_click(browser, 'point_color', CLASS_NAME)
        browser_click(browser, 'sp_rnb.btn_add', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '대화시작')
        time.sleep(3)
        if '한초희' not in browser.title : 
            raise Exception('1:1 대화 생성 확인 필요')

    def cc_leaveChat(self, browser) :
        Common().close(browser)
        browser_click(browser, 'icon.ico_set', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'LUX_basic_btn.Confirm.basic', CLASS_NAME)
        time.sleep(3)
        if '한초희' in browser.title : 
            raise Exception('1:1 대화 삭제 확인 필요')

class Companyboard :
    basic='기본'; blog='블로그'; gallery='갤러리'; feed='피드'
    management='게시판관리'; addBoard='게시판 추가'; deleteBoard='게시판 삭제'
    exit='나가기'
    def cb_progress(self, browser) :
        count = 1
        for i in range(0,30) :
            if count == 30 : 
                browser.refresh()
                time.sleep(5)
                raise Exception('30초 동안 무한로딩중,,')
            if hasxpath(browser, 'WSC_LUXCircularProgress', CLASS_NAME) :
                time.sleep(1)
                count = count + 1
            else : 
                break
        time.sleep(1)
   
    def cb_createBoardDetail(self, browser, boardType, boardName) :
        btn_click(browser, 'btn_snb', self.management)
        self.cb_progress(browser)
        btn_click(browser, 'LUX_basic_btn.Default.basic', self.addBoard)
        self.cb_progress(browser)
        browser_click(browser, boardType)
        # 게시판 추가 공통 사항 
        textClear(browser, varname.boardName)
        browser_sendKey(browser, varname.boardName, boardName + '게시판')
        browser_sendKey(browser, varname.boardDescription, boardName + '설명입니다,,')
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(3)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic', self.exit)
        time.sleep(1)
        browser.refresh()
        time.sleep(5)

    def cb_createBoard(self, browser) :
        #블로그게시판 추가
        self.cb_createBoardDetail(browser, varname.blogBoard, self.blog)

        #갤러리게시판추가
        self.cb_createBoardDetail(browser, varname.galleryBoard, self.gallery)

        #피드게시판추가
        self.cb_createBoardDetail(browser, varname.feedBoard, self.feed)
    
    def cb_inputTitle(self, browser, boardName) :
        time.sleep(3)
        browser_click(browser, 'btn_write', CLASS_NAME)
        browser.implicitly_wait(5)
        browser_sendKey(browser, varname.postTitle, boardName + '게시글테스트')
        action = ActionChains(browser)
        action.send_keys(Keys.TAB).pause(0.5).send_keys(boardName + '게시글에 입력').perform()
        action.reset_actions()
        time.sleep(3)

    def cb_uploadFile(self, browser) :
        # 본문에 이미지 추가
        browser_click(browser,'note-icon-picture', CLASS_NAME)
        time.sleep(1)
        fileUp = browser.find_elements_by_css_selector('input[type="file"]')
        fileUp[1].send_keys(path+'//btn_webot.png')
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '업로드')
        time.sleep(3)
        # 하단에 파일 추가
        fileUp[2].send_keys(path+'/Contacts_SampleFile.xlsx')
        time.sleep(3)
        if hasxpath(browser, varname.cb_uploadBtn) :
            raise Exception('회사게시판 하단 파일 추가 확인 필요')

    def cb_createPost(self, browser, boardName) :
        self.cb_inputTitle(browser, boardName)
        self.cb_uploadFile(browser)
        self.cb_vote(browser)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        self.cb_progress(browser)
        if hasxpath(browser, varname.boardListBtn) :
            self.cb_votingProgress(browser)
            #게시글 작성하고 목록으로 이동하기위함
            browser_click(browser, varname.boardListBtn)
            time.sleep(3)
        else :
            browser.get(getUrl('companyboard', False))
            try :
                browser.switch_to.alert.accept()
            except : pass
            raise Exception('게시판 글쓰기 확인 필요')

    def cb_createPost_basic(self, browser) :
        #기본게시판 클릭하여 글쓰기
        browser_click(browser, 'sp_wf.ico_newboard', CLASS_NAME)
        self.cb_createPost(browser, self.basic)

    def cb_createPost_blog(self, browser) :
        if hasxpath(browser, 'sp_wf.ico_notice', CLASS_NAME) :
            #블로그형게시판 클릭하여 글쓰기
            browser_click(browser, 'sp_wf.ico_notice', CLASS_NAME)
            self.cb_createPost(browser, self.blog)
        else :
            raise Exception('블로그 게시판 없음')

    def cb_createPost_gall(self, browser) :
        #갤러리형게시판 클릭하여 글쓰기
        browser_click(browser, 'sp_wf.ico_gallery', CLASS_NAME)
        self.cb_createPost(browser, self.gallery)

    def cb_createPost_feed(self, browser) :
        if hasxpath(browser, 'sp_wf.ico_community', CLASS_NAME) :
            #피드게시판 클릭하여 글쓰기
            browser_click(browser, 'sp_wf.ico_community', CLASS_NAME)
            time.sleep(3)
            browser_sendKey(browser, varname.feedContent, ' 피드형게시글')
            time.sleep(3)
            browser_click(browser, 'btn_submit', CLASS_NAME)
        else :
            raise Exception('피드 게시판 없음')

    def cb_modifyPost(self, browser) :
        browser_click(browser, 'sp_wf.ico_newboard', CLASS_NAME)
        browser_click(browser, 'btn_go', CLASS_NAME)
        browser_click(browser, varname.modifyBoardBtn)
        time.sleep(0.5)
        browser_sendKey(browser, varname.postTitle, '수정~~')
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)
        if not hasxpath(browser, 'file_bx', CLASS_NAME) :
            raise Exception('게시글 수정 후 파일 확인 필요')

    def cb_deletePost(self, browser) :
        browser_click(browser, 'sp_wf.ico_newboard', CLASS_NAME)
        time.sleep(3)
        while hasxpath(browser, 'btn_go', CLASS_NAME):
            browser_click(browser, 'btn_go', CLASS_NAME)  
            time.sleep(0.5)
            btn_click(browser, WSC_LUXButton, delete)
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(1)

    def cb_removeBoard(self, browser) :
        btn_click(browser, 'btn_snb', self.management)
        time.sleep(3)
        while hasxpath(browser, varname.boardList) :
            browser_click(browser, varname.boardList)
            time.sleep(1)
            btn_click(browser, 'LUX_basic_btn.Default.basic', self.deleteBoard)
            btn_click(browser, WSC_LUXButton, confirm)
            self.cb_progress(browser)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm basic', self.exit)

    def cb_vote(self, browser) :
        browser_click(browser, 'sp_wf.ico_vote', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)
        browser_sendKey(browser, varname.voteTitle, '투우표오')
        browser_click(browser, varname.voteItem)
        action = ActionChains(browser)
        action.send_keys('항목1번').send_keys(Keys.TAB*2).send_keys('항목2번').perform()
        action.reset_actions()
        time.sleep(1)

    def cb_votingProgress(self, browser) :
        browser_click(browser, varname.vote)
        browser_click(browser, varname.seleteItem)
        time.sleep(1)
        browser_click(browser, varname.closeVote)
        browser_click(browser, varname.close_cb)
        time.sleep(3)

    def cb_addComment_normal(self, browser) :
        browser_sendKey(browser, 'body', Keys.END, TAG_NAME)
        time.sleep(0.5)
        browser_click(browser, varname.cb_comment)
        action = ActionChains(browser)
        action.send_keys('여기에 댓글을 입력').perform()
        action.reset_actions()
        browser_click(browser, varname.cb_commentBtn)
        time.sleep(3)

        if '1' not in context(browser, varname.cb_commentCount) : 
            raise Exception('회사게시판 댓글 입력 확인 필요')

    def cb_addComment_feed(self, browser) :
        browser_click(browser, 'btn_profile', CLASS_NAME)
        action = ActionChains(browser)
        action.send_keys(Keys.TAB*5).send_keys(' 여기에 댓글을 입력').send_keys(Keys.TAB).pause(1).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        browser_click(browser, '//*[@id="body"]/div[4]')
        time.sleep(1)

        if '1' not in context(browser, varname.cb_feedCommentCount) : 
            raise Exception('회사게시판 댓글 입력 확인 필요')

    def cb_addComment(self, browser, boardType) :
        if boardType == self.feed :
            self.cb_addComment_feed(browser)
        else :
            self.cb_addComment_normal(browser)

    def cb_modifyComment(self, browser, boardType) :
        if boardType == self.feed :
            modify = varname.cb_feedModifyComment
            modifyBtn = varname.cb_feedModifyCommentBtn
        else :
            modify = varname.cb_modifyComment
            modifyBtn = varname.cb_modifyCommentBtn
        browser_click(browser, 'btn_modify', CLASS_NAME)
        browser_click(browser, modify)
        action = ActionChains(browser)
        action.send_keys('수정 수정').perform()
        action.reset_actions()
        browser_click(browser, modifyBtn)
        if boardType == self.feed :
            time.sleep(1)
            browser_click(browser, varname.close_cb)
        time.sleep(1)

        if '수정 수정' not in context(browser, 'msg_bx', CLASS_NAME) :
            raise Exception('회사게시판 댓글 수정 확인 필요')

    def cb_replyComment(self, browser, boardType) :
        if boardType == self.feed :
            reply = 'sub_btn_reply'
            replyInput = varname.cb_feedReplyCommnet
            replyBtn = varname.cb_feedReplyCommnetBtn
        else :
            reply = 'btn_reply_depth2'
            replyInput = varname.cb_replyComment
            replyBtn = varname.cb_replyCommentBtn

        browser_click(browser, reply, CLASS_NAME)
        browser_click(browser, replyInput)
        action = ActionChains(browser)
        action.send_keys('대대대대댓글').perform()
        action.reset_actions()
        browser_click(browser, replyBtn)
        time.sleep(1)

        if '1' not in context(browser, reply, CLASS_NAME) :
            raise Exception('회사게시판 대댓글 입력 확인 필요')

    def cb_deleteComment(self, browser, boardType) :
        browser_click(browser, 'btn_delete', CLASS_NAME)
        browser_click(browser, varname.close_cb)
        time.sleep(1)

        if boardType == self.feed :
            if '삭제된 댓글입니다.' not in context(browser, 'deleted_bx', CLASS_NAME) :
                raise Exception('회사게시판 댓글 삭제 확인 필요')
        else :
            if '삭제된 댓글입니다.' not in context(browser, 'msg_bx', CLASS_NAME) :
                raise Exception('회사게시판 댓글 삭제 확인 필요')

    def cb_comment(self, browser, boardType) :
        time.sleep(1)
        self.cb_addComment(browser, boardType)
        self.cb_modifyComment(browser, boardType)
        self.cb_replyComment(browser, boardType)
        self.cb_deleteComment(browser, boardType)

    def cb_comment_basic(self, browser) :
        if hasxpath(browser, 'sp_wf.ico_newboard', CLASS_NAME) :
            browser_click(browser, 'sp_wf.ico_newboard', CLASS_NAME)
            browser_click(browser, 'btn_go', CLASS_NAME)
            time.sleep(1)
            self.cb_comment(browser, self.basic)
        else :
            raise Exception('기본 게시판 없음')

    def cb_comment_blog(self, browser) :
        if hasxpath(browser, 'sp_wf.ico_notice', CLASS_NAME) :
            browser_click(browser, 'sp_wf.ico_notice', CLASS_NAME)
            browser_click(browser, 'btn_go', CLASS_NAME)
            self.cb_comment(browser, self.blog)
        else :
            raise Exception('블로그 게시판 없음')
    
    def cb_comment_gall(self, browser) :
        if hasxpath(browser, 'sp_wf.ico_gallery', CLASS_NAME) :
            browser_click(browser, 'sp_wf.ico_gallery', CLASS_NAME)
            browser_click(browser, 'btn_go', CLASS_NAME)
            self.cb_comment(browser, self.gallery)
        else :
            raise Exception('블로그 게시판 없음')

    def cb_comment_feed(self, browser) :
        if hasxpath(browser, 'sp_wf.ico_community', CLASS_NAME) :
            browser_click(browser, 'sp_wf.ico_community', CLASS_NAME)
            self.cb_comment(browser, self.feed)
        else :
            raise Exception('피드 게시판 없음')

class Message :
    boilerplate = '여기가 바로 상용구입니다'
    allreply='전체회신'; reply='회신'; forward='전달'
    def ms_recipient(self, browser, apply=True) :
        #받는 사람 목록에 사용자 추가
        if apply :
            browser_click(browser, 'button_new', CLASS_NAME)
            time.sleep(1)
        btn_click(browser, WSC_LUXButton, '찾기')
        time.sleep(1)
        browser_click(browser, 'destitem.ico3', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, '추가')
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)
        
    def ms_undistribute(self, browser) :
        # 서비스 미배포인 경우
        if sameText(browser, '해당 대상은 제외됩니다.') :
            browser_click(browser, varname.confirm)
            Common().undistribute(browser)
            self.ms_recipient(browser)

    def ms_sendBtn(self, browser) :
        browser_click(browser, 'sendbtn', CLASS_NAME)
        # 파일 첨부하면서 로딩바
        progress(browser)
        time.sleep(1)
        # 메시지 보내면서 로딩바
        progress(browser)

    def ms_sendMessageDetail(self, browser, name) :
        browser_sendKey(browser, varname.content_ms, name + '메시지 입력 테스트')
        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        browser_click(browser, 'funcbtn.ico_wdupload', CLASS_NAME)
        time.sleep(3)
        if hasxpath(browser, '//*[@id="WeDriveTableList"]/div/div[1]/span') :
            browser_click(browser, '//*[@id="WeDriveTableList"]/div/div[1]/span')
            btn_click(browser, WSC_LUXButton, confirm)
        else :
            btn_click(browser, WSC_LUXButton, '취소')
        self.ms_sendBtn(browser)

    def ms_sendMessage(self, browser, apply=True) :
        self.ms_recipient(browser, apply)
        self.ms_sendMessageDetail(browser, '일반')

    def ms_sendSecurityMessage(self, browser, apply=True) :
        self.ms_recipient(browser, apply)
        browser_click(browser, 'funcbtn.ico_secumsg', CLASS_NAME)
        time.sleep(1)
        self.ms_sendMessageDetail(browser, '보안')

    def ms_sendImportantMessage(self, browser, apply=True) :
        self.ms_recipient(browser, apply)
        browser_click(browser, 'funcbtn.ico_imptmsg', CLASS_NAME)
        time.sleep(1)
        self.ms_sendMessageDetail(browser, '중요')
        if not hasxpath(browser, 'sp_co_x2.icon_important', CLASS_NAME) :
            raise Exception('중요 메시지 확인 필요')

    def ms_sendReservationMessage(self, browser) :
        self.ms_recipient(browser)
        browser_click(browser, 'funcbtn.ico_reservmsg', CLASS_NAME)
        time.sleep(1)
        hour = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[1]/div[3]/div/div[3]/div[7]/div/div[2]/div[1]/div[2]/span[2]'
        min = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[1]/div[3]/div/div[3]/div[7]/div/div[2]/div[1]/div[2]/span[4]'
        browser_sendKey(browser, hour, currentTime().strftime('%I'))
        browser_sendKey(browser, min, currentTime().strftime('%M'))
        time.sleep(3)                            
        self.ms_sendMessageDetail(browser, '예약')

    def ms_sendMore(self, browser, type) :
        browser_click(browser, varname.receiveMessageTab)
        time.sleep(1)
        browser_click(browser, 'msg_item', CLASS_NAME)
        time.sleep(1)
        if hasxpath(browser, 'WSC_LUXPasswordField', CLASS_NAME) :
            self.ms_readSecurityMessage(browser)
            time.sleep(1)
        if type == self.allreply :
            browser_click(browser, 'icon.ico_allrep', CLASS_NAME)
        elif type == self.reply :
            browser_click(browser, 'icon.ico_rep', CLASS_NAME)
        elif type == self.forward :
            browser_click(browser, 'icon.ico_fw', CLASS_NAME)
            time.sleep(1)
            self.ms_recipient(browser, False)
        time.sleep(1)
        self.ms_sendMessageDetail(browser, type)

    def ms_replyAllMessage(self, browser) :
        self.ms_sendMore(browser, self.allreply)

    def ms_replyMessage(self, browser) :
        self.ms_sendMore(browser, self.reply)

    def ms_forwardMessage(self, browser) :
        self.ms_sendMore(browser, self.forward)

    def ms_resendMessage(self, browser) :
        # 다시 보내기
        browser_click(browser, varname.sendMessageTab)
        time.sleep(1)
        browser_click(browser, 'msg_item', CLASS_NAME)
        time.sleep(1)
        if hasxpath(browser, 'WSC_LUXPasswordField', CLASS_NAME) :
            self.ms_readSecurityMessage(browser)
            time.sleep(1)
        browser_click(browser, 'icon.ico_rep', CLASS_NAME)
        time.sleep(1)
        self.ms_sendBtn(browser)

    def ms_readMessageAll(self, browser) :
        #받은 메시지 클릭
        browser_click(browser, varname.receiveMessageTab)
        time.sleep(1)
        browser_click(browser, varname.popverbxMessage)
        browser_click(browser, varname.readAllMessage)
        browser_click(browser, varname.confirm)
        time.sleep(3)

    def ms_readSecurityMessage(self, browser) :
        time.sleep(1)
        browser_click(browser, 'sp_co_x2.icon_secret', CLASS_NAME)
        id = userid
        if id == 'ianswldudi' or 'qatest' in id :
            enter(browser, varname.securityPass, 'ckacl118*')
        else : 
            enter(browser, varname.securityPass, '1q2w3e4r')
        if context(browser, varname.duplicateMessage) == '패스워드가 일치하지 않습니다.' :
            browser_click(browser, varname.confirmMessage2)

    def ms_searchMessage(self, browser) :
        browser_click(browser, varname.receiveMessageTab)
        time.sleep(1)
        # 메시지 내용에 중요가 포함된 메시지 검색
        browser_click(browser, varname.searchMessage)
        browser_click(browser, varname.searchMessageContent)
        enter(browser, varname.searchInput_ms, '중요')
        time.sleep(3)

        if hasxpath(browser, 'empty_txt.v2', CLASS_NAME) :
            raise Exception('메시지 검색 확인 필요')

    def ms_deleteMessage(self, browser, send) :
        Common().close(browser)
        if send == 'receive' : btn = varname.receiveMessageTab
        elif send == 'send' : btn = varname.sendMessageTab
        for i in range(0,30) :
            browser_click(browser, btn)
            time.sleep(0.5)
            browser_click(browser, 'WSC_LUXCheckBox', CLASS_NAME)
            time.sleep(0.5)
            if checkText(browser, WSC_LUXButton, confirm) : browser_click(browser, varname.confirmMessage2)
            if checkText(browser, WSC_LUXButton, delete) :
                btn_click(browser, WSC_LUXButton, delete)
                browser_click(browser, varname.confirm_ms)
                progress(browser)
            else : break
            time.sleep(3)

        if not hasxpath(browser, 'empty_txt.v2', CLASS_NAME) :
            raise Exception('메시지 삭제 확인 필요')

    def ms_deleteReceiveMessage(self, browser) :
        self.ms_deleteMessage(browser, 'receive')

    def ms_deleteSendMessage(self, browser) :
        self.ms_deleteMessage(browser, 'send')

    def ms_bookmark(self, browser) :
        browser_click(browser, varname.receiveMessageTab)
        time.sleep(3)
        browser_click(browser, varname.messageList)
        time.sleep(1)
        if hasxpath(browser, 'WSC_LUXPasswordField', CLASS_NAME) :
            self.ms_readSecurityMessage(browser)
            time.sleep(1)
        browser_click(browser, 'common_checkswitch.check_fav', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, varname.bookmarkMessage)
        time.sleep(3)
        if hasxpath(browser, 'empty_txt.v2', CLASS_NAME) :
            raise Exception('메시지 즐겨찾기 확인 필요')

    def ms_recipientInfo(self, browser) :
        browser_click(browser, varname.sendMessageTab)
        time.sleep(1)
        browser_click(browser, 'msg_item', CLASS_NAME)
        browser_click(browser, 'icon.ico_member', CLASS_NAME)
        time.sleep(1)
        try :
            if not hasxpath(browser, 'dialog_content.co_v2_dialog.ssm.roundstyle', CLASS_NAME) :
                raise Exception('메시지 수신자 정보 확인 필요')
        finally : Common().close(browser)

    def ms_addBoilerplate(self, browser) :
        browser_click(browser, 'button_new', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'funcbtn.ico_macro', CLASS_NAME)
        browser_click(browser, 'button_add', CLASS_NAME)
        browser_sendKey(browser, '//*[contains(@id, "textArea")]', self.boilerplate)
        browser_click(browser, 'button_regist', CLASS_NAME)
        time.sleep(1)
        if not hasxpath(browser, '0_contentTemplate', ID) :
            raise Exception('메시지 상용구 추가 확인 필요')
        Common().close(browser)

    def ms_delBoilerplate(self, browser) :
        browser_click(browser, 'button_new', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'funcbtn.ico_macro', CLASS_NAME)
        while True :
            if hasxpath(browser, '0_contentTemplate', ID) :  
                browser_click(browser, '0_contentTemplate', ID)
                time.sleep(1)
                browser_click(browser, 'button_more', CLASS_NAME)
                time.sleep(1)
                browser_click(browser, 'sp_co_v2.icon_del', CLASS_NAME)
                btn_click(browser, WSC_LUXButton, confirm)
                time.sleep(1)
            else :
                break
        Common().close(browser)
    
    def ms_applyBoilerplate(self, browser) :
        browser_click(browser, 'button_new', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'funcbtn.ico_macro', CLASS_NAME)
        browser_click(browser, '0_contentTemplate', ID)
        btn_click(browser, 'common_round_btn.blue.btn38', '적용')
        time.sleep(3)
        message = browser.find_element(By.XPATH, '//*[@id="msgTextArea"]').text
        if message != self.boilerplate :
            Common().close(browser)
            raise Exception('메시지 상용구 적용 확인 필요')     
        self.ms_sendMessage(browser, False)

    def ms_readBoilerplate(self, browser) :
        browser_click(browser, varname.receiveMessageTab)
        time.sleep(1)
        browser_click(browser, varname.messageList)
        time.sleep(1)
        if self.boilerplate not in context(browser, 'new_received_con', CLASS_NAME) :
            raise Exception('메시지 상용구적용하여 보내기 확인 필요')

class Accounts :
    def ac_registAccount (self, browser) :
        progress(browser)
        browser_click(browser, varname.registerAccount)
        time.sleep(3)
        browser_sendKey(browser, varname.accountName, '(주)더존비즈온')
        browser_sendKey(browser, varname.representativeName, '김용우')
        browser_click(browser, varname.register)
        progress(browser)
        enter(browser, varname.searchAccount, '더존비즈온')
        count = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[3]/div[1]/h2'
        if '검색결과0' == context(browser, count) :
            raise Exception('거래처 등록 확인 필요')

    def ac_modifyAccount (self, browser) :
        textClear(browser, varname.searchAccount)
        enter(browser, varname.searchAccount, '더존비즈온')
        browser_click(browser, varname.modifyAccount)
        browser_sendKey(browser, varname.enterpriseNumber, '1348108473')
        time.sleep(1)

        #사용자 그룹 추가
        browser_click(browser, varname.accountGroupSelect)
        Common().canvasClick(browser, varname.accountGroup, 16, 16)
        time.sleep(1)
        browser_click(browser, varname.accountConfirm)
        time.sleep(3)
        browser_click(browser, varname.register)
        progress(browser)
    
    def ac_deleteAccount (self, browser) :
        while True :
            textClear(browser, varname.searchAccount)
            enter(browser, varname.searchAccount, '더존')
            time.sleep(1)
            if not hasxpath(browser, 'data_none', CLASS_NAME) :
                browser_click(browser, varname.clickAccount)
                browser_click(browser, varname.deleteAccount)
                browser_click(browser, varname.confirm_ac)
                progress(browser)
            else :
                break
    
    def ac_createGroup (self, browser) :
        browser_click(browser, varname.accountAddUserGroup)
        time.sleep(1)
        action = ActionChains(browser)
        action.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACK_SPACE).send_keys('거래처그룹').send_keys(Keys.ENTER).perform()
        time.sleep(3)
        if not hasxpath(browser, varname.accountList) :
            raise Exception('거래처 사용자 그룹 생성 확인 필요')

    def ac_deleteGroup (self, browser) :
        time.sleep(1)
        while hasxpath(browser, varname.accountList) :
            time.sleep(1)
            browser_click(browser, varname.accountList)
            time.sleep(3)
            browser_click(browser, varname.accountOption)
            time.sleep(1)
            browser_click(browser, varname.accountDeleteGroup)
            browser_click(browser, varname.confirm)
            browser.refresh()
            time.sleep(3)
        time.sleep(1)
        if hasxpath(browser, varname.accountList) :
            raise Exception('거래처 사용자 그룹 생성 확인 필요')

    def ac_createSharedGroup (self, browser) :
        browser_click(browser, varname.accountAddSharedGroup)
        time.sleep(1)
        browser_click(browser, varname.accountSharedGroupName)
        action = ActionChains(browser)
        action.send_keys('공유거래처그룹').send_keys(Keys.TAB).send_keys('한초희').pause(1).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(1)
        browser_click(browser, varname.accountCreateGroup)
        if sameText(browser, '공유그룹의 참여자를 추가해주세요.') :
            browser_click(browser, varname.confirm)
            browser_click(browser, varname.accountCloseButton)
            raise Exception('사용자 미초대!!')

    def ac_deleteSharedGroup(self, browser) :
        time.sleep(3)
        while hasxpath(browser, varname.accountSharedList) :
            time.sleep(1)
            browser_click(browser, varname.accountSharedList)
            time.sleep(1)
            browser_click(browser, varname.accountSharedOption)
            browser_click(browser, varname.accountDeleteSharedGroup)
            browser_click(browser, varname.confirm)
            time.sleep(1)

class Contacts :
    def businessCard(self, browser) :
        path = os.getcwd()
        f = path + '/test11.png'
        browser.find_element(By.ID, 'inputFile_front0').send_keys(f)
        time.sleep(1)

    def ct_registerContacts (self, browser) :
        browser_click(browser, varname.registerContact)
        time.sleep(1)
        # Common().fileUpload(browser, 'btn_webot.png')
        browser_sendKey(browser, 'enroll_lastName', '김', ID)
        browser_sendKey(browser, 'enroll_firstName', '혜린', ID)
        browser_sendKey(browser, 'phoneInputField0', '01038181299', ID)
        browser_sendKey(browser, 'emailInputField0', 'aaaa@naver.com', ID)
        browser_sendKey(browser, 'enroll_company_name0', '더존홀딩스', ID)
        browser_sendKey(browser, 'enroll_full_path0', '2센터', ID)
        browser_sendKey(browser, 'enroll_position_name0', '사원', ID)
        browser_sendKey(browser, 'enroll_task0', 'QA', ID)
        browser_click(browser, varname.register)
        progress(browser)

        time.sleep(3)
        count = browser.find_element(By.CLASS_NAME, 'number').text
        if count != '1' :
            raise Exception('연락처 등록 확인 필요')

    def ct_searchUser(self, browser, name) :
        enter(browser, varname.ct_searchUser, name)
        if hasxpath(browser, 'data_none', CLASS_NAME) : return False
        else : return True
    
    def ct_createGroup (self, browser) :
        browser_click(browser, varname.ct_createGroup)
        time.sleep(1)
        enter(browser, '//*[@id="input_new_group"]', '테스트폴더')
        if not hasxpath(browser, '//*[@id="group_box0"]/a') :
            raise Exception('연락처 사용자 그룹 생성 확인 필요')

    def ct_modifyGroup(self, browser) :
        browser_click(browser, '//*[@id="group_box0"]/a')
        browser_click(browser, '//*[@id="btn_edit0"]')
        time.sleep(1)
        browser_click(browser, varname.ct_modifyGroup)
        textClear(browser, '//*[@id="group_name0"]')
        enter(browser, '//*[@id="group_name0"]', '연락처 폴더 수정')
        time.sleep(3)

        name = browser.find_element(By.XPATH, '//*[@id="group_box0"]/a').text
        if not '연락처 폴더 수정' in name :
            raise Exception('연락처 그룹 수정 확인 필요')

    def ct_deleteGroup (self, browser) :
        while hasxpath(browser, '//*[@id="group_box0"]/a') :
            browser_click(browser, '//*[@id="group_box0"]/a')
            browser_click(browser, '//*[@id="btn_edit0"]')
            time.sleep(1)
            browser_click(browser, varname.ct_deleteGroup)
            browser_click(browser, varname.confirm)
            progress(browser)

        if hasxpath(browser, '//*[@id="group_box0"]/a') :
            raise Exception('연락처 사용자 그룹 삭제 확인 필요')

    def ct_createSharedGroup (self, browser) :
        browser_click(browser, varname.createSharedGroup)
        browser.implicitly_wait(5)
        browser_sendKey(browser, varname.groupName, '공유그룹테스트')
        if hasxpath(browser, varname.contactSameGroupName) :
            browser_sendKey(browser, varname.groupName, str(currentTime())[5:16])
        inputUser(browser, varname.groupParticipantContact)
        browser_click(browser, varname.checkContact)
        if sameText(browser, '공유 대상을 선택해주세요.') :
            browser_click(browser, varname.confirm)
            browser_click(browser, varname.contactCloseGroup)

        time.sleep(1)
        if not hasxpath(browser, '//*[@id="shared_group_box0"]') :
            raise Exception('연락처 사용자 공유그룹 생성 확인 필요')
    
    def ct_deleteSharedGroup (self, browser) :
        while hasxpath(browser, '//*[@id="shared_group_box0"]') :
            browser_click(browser, '//*[@id="shared_group_box0"]')
            browser_click(browser, '//*[@id="shared_btn_edit0"]')
            browser_click(browser, '//*[@id="shared_edit_list0"]/div/div/div/ul/li[3]/button')
            browser_click(browser, varname.confirm)
            progress(browser)

        if hasxpath(browser, '//*[@id="shared_group_box0"]') :
            raise Exception('연락처 사용자 공유그룹 삭제 확인 필요')

    def ct_deleteContact(self, browser) :
        time.sleep(3)
        browser_click(browser, 'group_box.is_num', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.selectContact)
        if hasxpath(browser, varname.deleteContact) :
            browser_click(browser, varname.deleteContact)
            browser_click(browser, varname.confirm_ct)
            progress(browser)
            browser_click(browser, varname.contactTrash)
            browser_click(browser, varname.confirm_ct)
        else :
            print('삭제할 연락처 없음!')

    def ct_contactImport(self, browser) :
        time.sleep(3)
        browser_click(browser, varname.contactSetting)
        time.sleep(3)
        browser_click(browser, 'tab_import', ID)
        time.sleep(3)
        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        time.sleep(5)
        browser_click(browser, varname.contactNext)
        progress(browser)
        Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div/canvas', 16, 16)
        time.sleep(1)
        browser_click(browser, varname.importButton)
        progress(browser)
        time.sleep(3)
        if hasxpath(browser, varname.cancelContact) :
            browser_click(browser, varname.cancelContact)

        time.sleep(3)
        count = browser.find_element(By.CLASS_NAME, 'number').text
        if count != '6' :
            raise Exception('연락처 가져오기 확인 필요')

    def ct_organizeContact(self, browser) :
        time.sleep(3)
        for i in range(1,4) :
            organize = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[1]/div[3]/div[3]/div/ul/li['
            organize = organize + str(i) + ']' 
            browser_click(browser, varname.contactSetting)
            browser_click(browser, 'tab_organization', ID)
            progress(browser)
            browser_click(browser, organize)
            progress(browser)
            organize = browser.find_element(By.XPATH, varname.combine).text
            if organize == '모두 합치기' or organize == '전체삭제':
                browser_click(browser, varname.combine)
                browser_click(browser, varname.confirm_ct)
            else :
                print('연락처 정리 내용 없음')
            progress(browser)

        time.sleep(3)
        count = browser.find_element(By.CLASS_NAME, 'number').text
        if count != '3' :
            raise Exception('연락처 정리하기 확인 필요')

class Schedule :
    def calenderName(self, browser) :
        calList = []
        calender = browser.find_elements(By.CLASS_NAME, 'group_box')
        for i in calender :
            calList.append(i.text[3:])
        return calList

    def sc_createCalendar (self, browser) :
        name = '캘린더 생성1'
        browser_click(browser, varname.createCalendar)
        browser.implicitly_wait(5)
        #동일 캘린더 명으로 생성가능하여 수정x
        browser_sendKey(browser, varname.calendarName, name)
        browser_sendKey(browser, varname.calendarExplan, '캘린더생성중입니다')
        browser_click(browser, '//*[@id="scrollCalendar"]/div[2]/div/div/div/div/ul/li[8]/span')
        btn_click(browser, WSC_LUXButton, save)
        time.sleep(1)
        if not name in self.calenderName(browser) :
            raise Exception('캘린더 생성 확인 필요')

    def sc_createSharedCalendar (self, browser) :
        browser_click(browser, varname.createCalendar)
        browser.implicitly_wait(5)
        #동일 캘린더 명으로 생성가능하여 수정x
        browser_sendKey(browser, varname.calendarName, '공유캘린더 생성1')
        browser_sendKey(browser, varname.calendarExplan, 'GUITAR는 이미지 기반의 자동화 툴이며 selenium Webdriver도 지원합니다.chrome 브라우저가 실행 되었을때 주소창의 위치가 이미지로 저장되어 있어야 합니다.')
        inputUser(browser, varname.calendarParticipant)
        btn_click(browser, WSC_LUXButton, save)
        time.sleep(1)
        if not '공유캘린더 생성1\n공유' in self.calenderName(browser) :
            raise Exception('캘린더 생성 확인 필요')

    def sc_dragCalender(self, browser) :
        cal = browser.find_element(By.XPATH, varname.calendarList)
        action = ActionChains(browser)
        action.click_and_hold(cal).drag_and_drop_by_offset(cal, 0, 50).perform()
        time.sleep(1)
        if not '공유' in context(browser, varname.calendarList) :
            raise Exception('캘린더 이동 확인 필요')

    def sc_modifyCalendar (self, browser) :
        time.sleep(1)
        browser_click(browser, varname.calendarList)
        time.sleep(1)
        browser_click(browser, varname.calendarEditBtn)
        time.sleep(1)
        browser_click(browser, varname.calendarModifyBtn)
        time.sleep(1)
        action = ActionChains(browser)
        action.send_keys(Keys.BACKSPACE).pause(0.5).send_keys('수정~').perform()
        action.reset_actions()
        btn_click(browser, WSC_LUXButton, save)
        time.sleep(1)
        if not '캘린더 생성수정~' in self.calenderName(browser) :
            raise Exception('캘린더 수정 확인 필요')

    def sc_deleteCalendar(self, browser) :
        calender = browser.find_elements(By.CLASS_NAME, 'ellipsis')
        calenderList = []
        for c in calender :
            if c.text :
                calenderList.append(c.text)
        for i in range(len(calenderList), 0, -1):
            calender = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[2]/div/div[1]/div[3]/div[2]/div[1]/div/div['
            calender = calender + str(i) + ']'
            canlenderName = browser.find_element(By.XPATH, calender).text
            if '캘린더 생성' in canlenderName :
                browser_click(browser, calender)
                time.sleep(1)
                option = calender + '/div[2]/div/div[1]/button'
                browser_click(browser, option)
                time.sleep(1)
                browser_click(browser, varname.calendarDeleteBtn)
                time.sleep(1)
                browser_click(browser, varname.confirm)
                time.sleep(3)
        time.sleep(1)
        if len(Schedule().calenderName(browser)) != 2 :
            raise Exception('캘린더 삭제 확인 필요')

    def sc_registerSchedule (self, browser) :
        browser_click(browser, varname.registerSchedule)
        time.sleep(3)
        #동일 일정 명으로 생성가능하여 수정x
        browser_sendKey(browser, varname.scheduleName, str(currentTime())[5:16])
        # 장소입력
        enter(browser, varname.sc_place, '에버랜드')
        time.sleep(1)
        self.sc_scheduleDetail(browser)

        btn_click(browser, WSC_LUXButton, save)
        progress(browser)
        if not (hasxpath(browser, 'rbc-addons-dnd-resizable', CLASS_NAME) or hasxpath(browser, 'schedule_info.day.color_type1', CLASS_NAME)):
            raise Exception('일정 등록 확인 필요')

    def sc_scheduleDetail(self, browser) :
        # 참석자 추가
        schedule = browser.find_elements(By.CLASS_NAME, 'WSC_LUXSpriteIcon')
        schedule[3].click()
        time.sleep(0.5)
        btn_click(browser, WSC_LUXButton, '사람 찾기')
        progress(browser)
        btn_click(browser, WSC_LUXButton, '조직도')
        inputUser(browser, '//*[@id="inputSearch-TK"]')
        # 사용자 추가 안된 경우
        if hasxpath(browser, 'point_color', CLASS_NAME) :
            browser_click(browser, 'point_color', CLASS_NAME)
            btn_click(browser, WSC_LUXButton, '추가')
            btn_click(browser, WSC_LUXButton, '확인')
        else : 
            action = ActionChains(browser)
            action.send_keys(Keys.ENTER).perform()
            browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[4]/div[2]/div/div/div[1]/div/div[2]/div/button[1]')
            time.sleep(1)
        # 알림 추가
        schedule[4].click()
        time.sleep(0.5)
        btn_click(browser, 'WSC_LUXCheckBox', '웹')

        # 설명추가
        schedule[7].click()
        time.sleep(0.5)
        enter(browser, varname.descriptionInput, '설명입니다')

    def sc_searchSchedule(self, browser) :
        enter(browser, varname.sc_searchInput, str(currentTime())[5:11])
        if context(browser, varname.sc_searchResult) == '0건' :
            raise Exception('일정 검색 확인 필요') 

    def sc_addComment(self, browser) :
        Common().close(browser)
        if hasxpath(browser, 'rbc-addons-dnd-resizable', CLASS_NAME) :
            browser_click(browser, 'rbc-addons-dnd-resizable', CLASS_NAME)
            btn_click(browser, WSC_LUXButton, '상세')
            time.sleep(1)
            browser_click(browser, varname.sc_comment)
            browser_sendKey(browser, varname.sc_commentInput, '일정에서 쓰는 댓글입니다.')
            time.sleep(0.5)
            browser_click(browser, varname.sc_registComment)
            time.sleep(3)
            count = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[3]/div[1]/div[9]/div[2]/div/div/div[1]/div/div/div[1]/ul/li[2]/a/span/span'
            if context(browser, count) == '0' :
                Common().close(browser)
                raise Exception('일정 댓글 확인 필요')
            Common().close(browser)
        else :
            raise Exception('일정 미등록 상태')

    def sc_deleteSchedule(self, browser) :
        while True :
            if hasxpath(browser, 'rbc-addons-dnd-resizable', CLASS_NAME) :
                browser_click(browser, 'rbc-addons-dnd-resizable', CLASS_NAME)
                btn_click(browser, WSC_LUXButton, delete)
                time.sleep(0.5)
            else :
                break
        if hasxpath(browser, 'rbc-addons-dnd-resizable', CLASS_NAME) :
            raise Exception('일정 삭제 확인 필요')

    def sc_clickCalendar(self, browser) :
        Common().close(browser)
        browser_click(browser, varname.weekCalendar) 
        time.sleep(1)
        if not hasxpath(browser, 'chfont.rbc-time-view', CLASS_NAME) :
            raise Exception('일정 주간 클릭 확인 필요')
        
        browser_click(browser, varname.dayCalendar) 
        time.sleep(1)
        if not hasxpath(browser, 'chfont.rbc-time-view', CLASS_NAME) :
            raise Exception('일정 일간 클릭 확인 필요')
        
        browser_click(browser, varname.listCalendar) 
        time.sleep(1)
        if not hasxpath(browser, 'rbc-agenda-content.agenda-scroll', CLASS_NAME) :
            raise Exception('일정 목록 클릭 확인 필요')

class Mail :
    normal='일반'; reserve='예약'; security='보안'; reply='답장'; replyAll='전체답장'; forward='전달'
    
    def ma_settingUse(self, browser) :
        # 읽기 설정
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        btn = browser.find_elements(By.CLASS_NAME, 'WSC_LUXRadioButton')
        for i in btn[3::2] : 
            i.click()
            time.sleep(0.1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)
        # 쓰기설정
        browser.find_element(By.XPATH, '//li[contains(., "쓰기설정")]').click()
        btn_click(browser, 'WSC_LUXRadioButton', '사용함', False)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        self.ma_addSignature(browser, '서명')
        self.ma_addSignature(browser, '부재중')

    def ma_addSignature(self, browser, name) :
        action = ActionChains(browser)
        action.send_keys(Keys.HOME).perform()
        action.reset_actions()
        time.sleep(1)
        browser.find_element(By.XPATH, '//li[contains(., "기타 설정")]').click()
        if name == '부재중' : 
            name = '답장'; title = varname.ma_absence; saveBtn = varname.ma_absenceBtn
            browser.find_element(By.XPATH, '//li[contains(., "부재중 응답")]').click()
        elif name == '서명' : title = varname.ma_signature ; saveBtn = varname.ma_signatureBtn
        btn_click(browser, 'WSC_LUXRadioButton', '사용함')
        btn_click(browser, WSC_LUXButton, name)
        time.sleep(1)
        browser_sendKey(browser, title, '여기 '+name)
        self.ma_sendMailContent(browser)
        browser_click(browser, saveBtn)
        btn = browser.find_elements(By.CLASS_NAME, 'WSC_LUXRadioButton')
        btn[-1].click()
        btn_click(browser, WSC_LUXButton, save)
        time.sleep(1)

    def ma_settingUnuse(self, browser) :
        # 읽기설정
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        btn = browser.find_elements(By.CLASS_NAME, 'WSC_LUXRadioButton')
        for i in btn[4::2] : 
            i.click()
            time.sleep(0.1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)
        # 쓰기설정
        browser.find_element(By.XPATH, '//li[contains(., "쓰기설정")]').click()
        btn_click(browser, 'WSC_LUXRadioButton', '사용 안 함', False)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        self.ma_delSignature(self, browser, '서명')
        self.ma_delSignature(self, browser, '서명')

    def ma_delSignature(self, browser, name) :
        action = ActionChains(browser)
        action.send_keys(Keys.HOME).perform()
        action.reset_actions()
        time.sleep(1)
        browser.find_element(By.XPATH, '//li[contains(., "기타 설정")]').click()
        if name == '부재중' : 
            name = '답장'; title = varname.ma_absence; saveBtn = varname.ma_absenceBtn
            browser.find_element(By.XPATH, '//li[contains(., "부재중 응답")]').click()
        elif name == '서명' : title = varname.ma_signature ; saveBtn = varname.ma_signatureBtn
        btn_click(browser, WSC_LUXButton, '삭제')
        btn_click(browser, WSC_LUXButton, confirm)
        btn_click(browser, 'WSC_LUXRadioButton', '사용 안 함')
        btn_click(browser, WSC_LUXButton, save)
        time.sleep(1)

    def ma_checkUse(self, browser) : print('')

    def ma_mailboxClick(self, browser, title) :
        browser.find_element(By.XPATH, f'//li[contains(., "{title}")]').click()
        time.sleep(1)
        mailbox = '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]/div[1]/h2'
        name = browser.find_element(By.XPATH, mailbox).text
        if name != title :
            raise Exception('메일박스 확인필요')

    def ma_mailbox(self, browser) :
        time.sleep(1)
        self.ma_mailboxClick(browser, '전체메일함')
        self.ma_mailboxClick(browser, 'WEHAGO 메일')
        self.ma_mailboxClick(browser, '보낸메일함')
        self.ma_mailboxClick(browser, '임시보관함')

    def ma_recipient(self, browser) :
        btn_click(browser, 'LUX_basic_btn.Default.basic', '사람찾기')
        btn_click(browser, WSC_LUXButton, '조직도')
        time.sleep(1)
        # inputUser(browser, '//*[@id="inputSearch-TK"]')
        # browser_click(browser, 'point_color', CLASS_NAME)
        btn_click(browser, 'LUX_basic_btn.Default.basic', '추가')
        btn_click(browser, 'LUX_basic_btn.saobtn.basic2', confirm)
        self.ma_receivercc(browser)
        time.sleep(1)

    def ma_receivercc(self, browser) :
        browser_click(browser, 'LUX_basic_btn.Image.basic.btn_more', CLASS_NAME)
        time.sleep(1)
        if wehagoBrand == 3:
            enter(browser, varname.mailcc, 'ianswldudi@wehagov.com')
            enter(browser, varname.mailbcc, 'vqatest02@wehagov.com')
        else : 
            enter(browser, varname.mailcc, 'ctestjy_1030@wehago.com')
            enter(browser, varname.mailbcc, 'stestjy_1913@wehago.com')

    def ma_hasMailTitle(self, browser):
        #메일 제목 없는 경우
        if sameText(browser, '제목이 지정되지 않았습니다.') :
            browser_click(browser, varname.confirm)
            time.sleep(3)

    def ma_sendMailContent(self, browser) :
        browser.switch_to.frame(0)
        time.sleep(1)
        browser.find_element(By.XPATH, '//*[@id="dzeditor_0"]').click()
        action = ActionChains(browser)
        action.send_keys('대박드디어썼다ㅠㅠㅠ').perform()
        browser.switch_to.default_content()
        time.sleep(1)
        
    def ma_sendMailTitle(self, browser, name) :
        textClear(browser, varname.mailTitle)
        browser_sendKey(browser, varname.mailTitle, '메일제목입력하는부분--'+name)
        time.sleep(1)

    def ma_clickOption(self, browser, mail) :
        browser_click(browser, varname.mailOption)
        if mail == self.reserve :
            browser_click(browser, varname.reservationMail)
            self.ma_hasMailTitle(browser)
            time.sleep(1)
            #예약메일 보내기 위해 시간 세팅
            browser_sendKey(browser, varname.mailHour, currentTime().strftime('%I'))
            time.sleep(3)
            text = '예약 시간은 현재 이후부터 설정 가능합니다.'
            if sameText(browser, text) :
                browser_click(browser, varname.confirm)
                print('1분 뒤에 다시 보내기')
                time.sleep(60)
                browser_sendKey(browser, varname.mailHour, currentTime().strftime('%I'))
                time.sleep(0.5)
            browser_sendKey(browser, varname.mailMinute, currentTime().strftime('%M'))
            time.sleep(0.5)
            browser_sendKey(browser, varname.mailMinute, Keys.ENTER)
            time.sleep(1)
        elif mail == self.security :
            browser_click(browser, varname.secureMail)
            time.sleep(1)
            self.ma_hasMailTitle(browser)
            browser_sendKey(browser, varname.password, 'ckacl118*')
            browser_sendKey(browser, varname.passwordCheck, 'ckacl118*')

    def ma_clickSendButton(self, browser, mail) :
        if mail == self.reserve or mail == self.security:
            self.ma_clickOption(browser, mail)
            btn_click(browser, WSC_LUXButton, confirm)
        else : 
            btn_click(browser, 'LS_btn', '보내기')
            self.ma_hasMailTitle(browser)
        progress(browser)
        if sameText(browser, '메일 전송에 실패하였습니다.') :
            browser_click(browser, varname.confirm)
        if mail != '임시저장' :
            if not hasxpath(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div/h3') :
                raise Exception(mail + ' 전송 확인 필요')
        else :
            browser_click(varname.drafts)
            time.sleep(1)
            count = browser.find_element(By.CLASS_NAME, 'sub_info.sub_info2').text
            if count[4:] != '1' :
                raise Exception('임시저장 확인 필요')
        self.ma_mailbox(browser)
        time.sleep(5)

    def ma_wedriveUpload(self, browser) :
        btn_click(browser, 'LUX_basic_btn.Default.basic', '웹스토리지')
        time.sleep(1)
        if hasxpath(browser, varname.ma_wedriveSelect) :
            browser_click(browser, varname.ma_wedriveSelect)
            browser_click(browser, varname.ma_wedriveConfirm)
            time.sleep(3)
        else : 
            browser_click(browser, varname.ma_wedriveConfirm)
            raise Exception('웹스토리지 파일 없음')

    def ma_sendMailDetail(self, browser, name, local=True, wedrive=None) :
        Common().close(browser)
        browser_click(browser, varname.sendMail)
        try :
            browser.switch_to.alert.accept()
        except : pass
        time.sleep(3)
        self.ma_recipient(browser)
        self.ma_sendMailTitle(browser, name)
        if local :
            Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
            time.sleep(1)
        if wedrive :
            self.ma_wedriveUpload(browser)
        self.ma_sendMailContent(browser)

    def ma_sendMail(self, browser) :
        self.ma_sendMailDetail(browser, self.normal)
        self.ma_clickSendButton(browser, self.normal)

    def ma_sendMailWedrive(self, browser) :
        self.ma_sendMailDetail(browser, '웹스토리지 파일 첨부', local=False, wedrive=True)
        self.ma_clickSendButton(browser, self.normal)

    def ma_sendMailLocalWedrive(self, browser) :
        self.ma_sendMailDetail(browser, '웹스토리지 로컬 파일 첨부', wedrive=True)
        self.ma_clickSendButton(browser, self.normal)

    def ma_sendReservedMail(self, browser) :
        self.ma_sendMailDetail(browser, self.reserve)
        self.ma_clickSendButton(browser, self.reserve)
    
    def ma_sendSecureMail(self, browser) :
        self.ma_sendMailDetail(browser, self.security)
        self.ma_clickSendButton(browser, self.security)

    def ma_sendSharedMail(self, browser) :
        self.ma_sendMailDetail(browser, '공용메일')
        browser_click(browser, 'inputElement', ID)
        action = ActionChains(browser)
        action.send_keys(Keys.DOWN*2).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(3)
        self.ma_clickSendButton(browser, '공용메일')

    def ma_sendSpamMail(self, browser) :
        self.ma_sendMailDetail(browser, '스팸')
        self.ma_clickSendButton(browser, '스팸')

    def ma_sendMore(self, browser, mail) :
        browser.find_element(By.XPATH, '//li[contains(., "전체메일함")]').click()
        time.sleep(5)
        browser_click(browser, 'mail_list_item_0', ID)
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, mail)

    def ma_replyMail(self, browser) :
        self.ma_sendMore(browser, self.reply)
        self.ma_clickSendButton(browser, self.reply)

    def ma_replyMailAll(self, browser) :
        self.ma_sendMore(browser, self.replyAll)
        self.ma_clickSendButton(browser, self.replyAll)
    
    def ma_deliveryMail(self, browser) :
        self.ma_sendMore(browser, self.forward)
        self.ma_recipient(browser)
        self.ma_clickSendButton(browser, self.forward)

    def ma_temporarySave(self, browser) :
        self.ma_sendMailDetail(browser, '임시저장')
        browser_click(browser, varname.mailSave)
        browser_click(browser, varname.drafts)
        progress(browser)

    def ma_deleteMail(self, browser) :
        time.sleep(3)
        Common().close(browser)
        browser.find_element(By.XPATH, '//li[contains(., "전체메일함")]').click()
        time.sleep(5)
        browser_click(browser, varname.checkMail)
        if context(browser, varname.deleteMail) == delete :
            browser_click(browser, varname.deleteMail)
            time.sleep(1)
        else : 
            print('삭제할 메일 없음,,?!')

    def ma_emptyTrash(self, browser) :
        # 메일함 비우기 클릭
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        browser_click(browser, varname.mailBoxSetting)
        time.sleep(1)        
        pageDown(browser, 'content_flex_area', CLASS_NAME)
        btn = browser.find_elements(By.CLASS_NAME, 'LUX_basic_btn.Default.basic')
        btnlist = []
        for i in btn :
            if i.text == '비우기' : btnlist.append(i)

        for i in btnlist :
            i.click()
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(1)
    
    def ma_externalMailLink(self, browser) :
        time.sleep(3)
        Common().close(browser)
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, varname.externalMailSetting)
        browser_click(browser, varname.naverMail)
        browser_sendKey(browser, varname.naverid, 'smile_1896@naver.com')
        browser_sendKey(browser, varname.naverPass, 'ckacl118*')
        browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[7]/div[2]/span')
        browser_click(browser, 'fltrgt', CLASS_NAME)
        progress(browser)
        if sameText(browser, '동일한 계정이 이미 등록되어 있습니다.') :
            browser_click(browser, varname.confirm)
            browser_click(browser, varname.closeExternalMail)

        if hasxpath(browser, varname.deleteExternalMail) :
            browser_click(browser, varname.deleteExternalMail)
            browser_click(browser, varname.confirm)
            time.sleep(1)
        else :
            raise Exception('외부메일 연동 확인 필요')

    def ma_externalMailLinkEtc(self, browser) :
        time.sleep(3)
        Common().close(browser)
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, varname.externalMailSetting)
        browser_click(browser, varname.mailLinkEtc)
        time.sleep(1)
        browser_sendKey(browser, varname.externalAccount, 'smile_1896@naver.com')
        browser_sendKey(browser, varname.externalPassword, 'ckacl118*')
        browser_sendKey(browser, varname.popserver, 'pop.naver.com')
        browser_sendKey(browser, varname.smtpsetting, 'smtp.naver.com')
        browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[8]/div[2]/span/span')
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
        progress(browser)
        if sameText(browser, '동일한 계정이 이미 등록되어 있습니다.') :
            browser_click(browser, varname.confirm)
            browser_click(browser, varname.closeExternalMail)
        if hasxpath(browser, varname.deleteExternalMail) :
            browser_click(browser, varname.deleteExternalMail)
            browser_click(browser, varname.confirm)

    def ma_settingClick(self, browser) :
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        browser_click(browser, varname.mailSetDefault)
        mailSetting = '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/ul/li[1]'
        if context(browser, mailSetting) != '읽기설정' :
            raise Exception('메일 환경설정 확인')
        time.sleep(1)
        browser_click(browser, varname.manageMailbox)
        if context(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div[1]/dl/dt') != '사용가능 용량' :
            raise Exception('메일 환경설정 확인')
        time.sleep(1)
        browser_click(browser, varname.setMail)
        if context(browser, mailSetting) != '자동분류' :
            raise Exception('메일 환경설정 확인')
        time.sleep(1)
        browser_click(browser, varname.mailLink)
        if context(browser, mailSetting) != '외부메일추가' :
            raise Exception('메일 환경설정 확인')
        time.sleep(1)
        browser_click(browser, varname.mailOtherSetting)
        if context(browser, mailSetting) != '서명' :
            raise Exception('메일 환경설정 확인')
    
    def ma_addExternalMail(self, browser) :
        self.ma_settingClick(browser)
        self.ma_externalMailLink(browser)

    def ma_automaticClassification(self, browser) :
        time.sleep(3)
        Common().close(browser)
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        browser_click(browser, varname.setMail)
        browser_click(browser, varname.ma_category)
        time.sleep(3)
        enter(browser, varname.mailCategoryTitle, '메일제목')
        browser_click(browser, varname.ma_markAsRead)
        browser_click(browser, varname.ma_applyBtn)
        time.sleep(3)
        # browser_click(browser, 'rnb_info_item', CLASS_NAME)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
        time.sleep(5)
        browser.find_element(By.XPATH, '//li[contains(., "전체메일함")]').click()
        time.sleep(1)
        # count = '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[2]/div[2]/div[1]/div[1]/p/em'
        # if context(browser, count) != '0' :
        #     raise Exception('자동분류 확인 필요')

    def ma_deleteAutomatic(self, browser) :
        time.sleep(3)
        Common().close(browser)
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        browser_click(browser, varname.setMail)
        time.sleep(3)
        btn = browser.find_elements(By.CLASS_NAME, 'LUX_basic_btn.Default.basic')
        btnList = []
        for i in btn :
            if i.text == '삭제' : btnList.append(i)
        del btnList[0]
        for i in btnList[::-1] :
            i.click()
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(1)

    def ma_spamSetting(self, browser) :
        time.sleep(3)
        Common().close(browser)
        browser_click(browser, 'sp_snb.ico_settings', CLASS_NAME)
        browser_click(browser, varname.setMail)
        browser_click(browser, varname.spamSetting)

class Todo :
    def td_close(self, browser) :
        if hasxpath(browser, 'LUX_basic_btn.Default.basic.close_btn',CLASS_NAME) :
            browser_click(browser, 'LUX_basic_btn.Default.basic.close_btn',CLASS_NAME)
            time.sleep(1)

    def td_createProject(self, browser) :
        self.td_createPersonalProject(browser)
        self.td_createSharedProject(browser)

        if not hasxpath(browser, varname.projectList) :
            raise Exception('할일 프로젝트 생성 확인 필요')

    def td_createPersonalProject(self, browser) :
        # 개인
        browser_click(browser, varname.createTodoProject)
        browser_sendKey(browser, varname.todoProjectName, '개인프로젝트생성')
        browser_click(browser, varname.saveTodoProject)
        progress(browser)

    def td_createSharedProject(self, browser) :
        # 공유
        browser_click(browser, varname.createTodoProject)
        browser_click(browser, '//*[@id="root"]/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/ul/li[8]/span')
        browser_sendKey(browser, varname.todoProjectName, '공유프로젝트생성')
        inputUser(browser, varname.TodoParticipant)
        self.td_undistribute(browser)
        browser_click(browser, varname.saveTodoProject)
        progress(browser)

    def td_undistribute(self, browser) :
        time.sleep(1)
        # 서비스 미배포인 경우
        if '서비스 권한 미보유' in context(browser, varname.td_duplicatePopup) :
            browser_click(browser, varname.confirm)
            Common().undistribute(browser)
            self.td_createSharedProject(browser)

    def td_modifyProject(self, browser) :
        self.td_modifyPersonalProject(browser)
        self.td_modifySharedProject(browser)

        if not '수정~!' in context(browser, varname.projectList2) :
            raise Exception('할일 프로젝트 수정 확인 필요')

    def td_modifyPersonalProject(self, browser) :
        # 개인프로젝트 수정하여 공유멤버 추가
        browser_click(browser, varname.projectList2)
        browser_click(browser, varname.todoOption2)
        time.sleep(1)
        browser_click(browser, varname.todoModifyBtn)
        time.sleep(1)
        browser_sendKey(browser, varname.todoProjectName, '수정~!')
        inputUser(browser, varname.TodoParticipant)
        browser_click(browser, varname.saveTodoProject)
        progress(browser)

    def td_modifySharedProject(self, browser) :
        # 공유프로젝트 수정하여 공유멤버 제외
        browser_click(browser, varname.projectList)
        browser_click(browser, varname.todoOption)
        time.sleep(1)
        browser_click(browser, varname.todoModifyBtn)
        time.sleep(1)
        browser_click(browser, varname.todoUserList)
        browser_click(browser, varname.td_excludeShared)
        browser_click(browser, varname.saveTodoProject2)
        progress(browser)

    def td_createBoard(self, browser) :
        browser_click(browser, varname.projectList)
        for i in range(0,20) :
            browser_click(browser, varname.addTodoBoard)
            time.sleep(1)

        time.sleep(1)
        title = browser.find_element(By.XPATH, '//*[@id="boardWidth"]/div/div[20]/div[1]/p').text
        if title != 'Board(19)' :
            raise Exception('할일 보드 생성 확인 필요')

    def td_deleteBoard(self, browser) :
        browser_click(browser, varname.projectList)
        while True :
            board = browser.find_elements(By.CLASS_NAME, 'sp_td.op')
            time.sleep(1)
            if len(board) != 1 :
                browser_click(browser, 'sp_td.op', CLASS_NAME)
                time.sleep(1)
                browser_click(browser, varname.boardDelete)
                time.sleep(0.5)
                browser_click(browser, varname.confirm)
                time.sleep(1)
            else :
                break

        browser.refresh()
        progress(browser)
        self.td_close(browser)

        time.sleep(1)
        title = browser.find_element(By.XPATH, '//*[@id="boardWidth"]/div/div/div[1]/p').text
        if title != 'Board(19)' :
            raise Exception('할일 보드 삭제 확인 필요')

    def td_createChildTodo(self, browser) :
        browser_click(browser, varname.addTodo)
        # 할일명 입력
        browser_sendKey(browser, '//*[@id="todo_name_"]', '하위할일')
        browser_click(browser, varname.saveTodo)
        progress(browser)

    def td_createTodo(self, browser) :
        browser_click(browser, varname.projectList)
        self.td_createChildTodo(browser)
        browser_click(browser, varname.addTodo)
        # 할일명 입력
        browser_sendKey(browser, '//*[@id="todo_name_"]', '할일22')
        # 우선순위 선택
        browser_click(browser, varname.td_priority)
        time.sleep(0.5)
        browser_click(browser, '/html/body/div[4]/div/div/div[2]/div/ul/li[2]')
        # 기한 선택
        browser_click(browser, varname.td_datePicker)
        time.sleep(0.5)
        browser_click(browser, 'btn_group', CLASS_NAME)
        time.sleep(0.5)

        todo = browser.find_elements(By.CLASS_NAME, 'accodion_lst')
        for s in todo :
            s.click()
            time.sleep(0.1)
        time.sleep(1)

        # 체크리스트 입력
        for i in range(1, 11) :
            enter(browser, varname.td_checklist, '할일체크크'+str(i))
        # 태그 입력
        browser_sendKey(browser, varname.td_tag, '할일x태그')
        time.sleep(2)
        action = ActionChains(browser)
        action.send_keys(Keys.ENTER).perform()
        action.reset_actions()
        # 설명 입력
        enter(browser, varname.td_description, '할일설명이라네')
        # 알림 클릭
        browser_click(browser, varname.td_notice)
        # 하위할일 추가
        enter(browser, varname.td_childTodo, '하위할일')

        browser_click(browser, varname.saveTodo)
        progress(browser)
        browser_click(browser, 'content_bx', CLASS_NAME)
        progress(browser)
        if not hasxpath(browser, 'LUX_basic_tabs.bdline_cnt', CLASS_NAME) :
            raise Exception('할일 클릭 확인 필요')

    def td_addComment(self, browser) :
        Common().close(browser)
        browser_click(browser, varname.projectList)
        time.sleep(1)
        browser_click(browser, 'content_bx', CLASS_NAME)
        progress(browser)
        time.sleep(1)
        browser_click(browser, varname.td_comment)
        time.sleep(1)
        browser_sendKey(browser, varname.td_commentInput, '할일 댓글입니다')
        browser_click(browser, varname.td_registComment)
        time.sleep(1)
        count = '//*[@id="root"]/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div[2]/div[3]/div/div[1]/div[1]/ul/li[2]/a/span/span'
        if context(browser, count) == '0' :
            raise Exception('할일 댓글 확인 필요')

    def td_completeTodo(self, browser) :
        browser_click(browser, varname.projectList)
        time.sleep(1)
        browser_click(browser, 'chk_form', CLASS_NAME)
        time.sleep(1)

    def td_searchTodo(self, browser) :
        browser_click(browser, 'btn.btn_search', CLASS_NAME)
        time.sleep(1)
        enter(browser, varname.td_search, '할일22')
        if context(browser, 'point_color.nm', CLASS_NAME) == '0' :
            raise Exception('할일 검색 확인 필요')

    def td_deleteTodo(self, browser) :
        browser_click(browser, 'content_bx', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.td_deleteTodoBtn)
        browser_click(browser, varname.confirm)

    def td_deleteProject (self, browser) :
        self.td_close(browser)
        self.td_deleteProjectDetail(browser, '개인')
        self.td_deleteProjectDetail(browser, '공유')

        # 프로젝트 리스트가 2개이상이면 프로젝트 삭제 제대로 안된것
        browser_click(browser, varname.addTodo)
        browser_click(browser, varname.selectTodoProject)
        time.sleep(1)
        if hasxpath(browser, '//*[@id="listBoxElement"]/div/ul/li[2]') :
            browser_click(browser, '//*[@id="listBoxElement"]/div/ul/li[1]')
            browser_click(browser, varname.close_td)
            raise Exception('할일 프로젝트 삭제 확인 필요')
        else :
            browser_click(browser, '//*[@id="listBoxElement"]/div/ul/li[1]')
            browser_click(browser, varname.close_td)

    def td_deleteProjectDetail(self, browser, member) :
        if member == '개인' :
            projectList = varname.projectList2
            todoOption = varname.todoOption2
        else :
            projectList = varname.projectList
            todoOption = varname.todoOption
        while hasxpath(browser, projectList) :
            browser_click(browser, projectList)
            time.sleep(1)
            browser_click(browser, todoOption)
            time.sleep(1)
            browser_click(browser, varname.todoDeleteBtn)
            browser_click(browser, varname.confirm)
            browser_click(browser, varname.checkTodo)
            progress(browser)

class Wecrm :
    opportunity='영업기회'; product='판매상품'
    def crm_basicNext(self, browser) :
        browser_click(browser, varname.crmTopms)
        time.sleep(1)
        browser_click(browser, varname.crmBasicsetNext2)
        time.sleep(5)
        browser_click(browser, varname.crmStart)
        time.sleep(5)

    def crm_basicset(self, browser) :
        time.sleep(5)
        if hasxpath(browser, 'pms_basicset_tit_btn', CLASS_NAME) :
            browser_click(browser, 'pms_basicset_tit_btn', CLASS_NAME)
            Company().cs_setAdministor(browser)
        else :
            if hasxpath(browser, 'pms_basicset_tit', CLASS_NAME) :
                browser_click(browser, varname.crmBasicsetNext1)
                browser_click(browser, varname.crmBasicsetNext2)
                time.sleep(0.5)
                if hasxpath(browser, varname.crmTopms) :
                    self.crm_basicNext(browser)
                else :
                    browser_click(browser, '//*[@id="conbox"]')
                    action = ActionChains(browser)
                    action.send_keys('테스트2').send_keys(Keys.ENTER).perform()
                    time.sleep(1)
                    browser_click(browser, varname.crmBasicsetNext2)
                    self.crm_basicNext(browser)

    def crm_settingUse(self, browser) :
        li_click(browser, setting)
        btn_click(browser, 'WSC_LUXCheckBox', '사용')
        btn_click(browser, WSC_LUXButton, confirm)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(3)
        browser_click(browser, varname.crmAccountManagemet)
        time.sleep(1)
        Common().canvasClick(browser, '//*[@id="salesListGrid"]/div/canvas', 100, 45)
        progress(browser)
        if not hasxpath(browser, 'sp_crm.pms2', CLASS_NAME) : raise Exception('pms 연동 사용 확인 필요')
        
    def crm_settingUnuse(self, browser) :
        li_click(browser, setting)
        btn_click(browser, 'WSC_LUXCheckBox', '사용안함')
        btn_click(browser, WSC_LUXButton, confirm)
        btn_click(browser, WSC_LUXButton, confirm)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(3)
        browser_click(browser, varname.crmAccountManagemet)
        time.sleep(1)
        Common().canvasClick(browser, '//*[@id="salesListGrid"]/div/canvas', 100, 45)
        progress(browser)
        if hasxpath(browser, 'sp_crm.pms2', CLASS_NAME) : raise Exception('pms 연동 사용안함 확인 필요')

    def crm_businessDetails(self, browser, name) :
        browser_sendKey(browser, varname.salesName, name)
        textClear(browser, varname.orderAmount)
        browser_sendKey(browser, varname.orderAmount, '1056000')
        browser_click(browser, varname.registerCrm)
        progress(browser)

    def crm_searchAccount(self, browser) :
        time.sleep(1)
        enter(browser, varname.crmAccountName, 'CRM 테스트')
        progress(browser)
        browser_click(browser, varname.selectCrmAccount)
        browser_click(browser, varname.crmNext)
        progress(browser)

    def crm_duplicateSales(self, browser) :
        text = '영업 이름이 중복되었습니다.'
        if sameText(browser, text) :
            browser_click(browser, varname.confirm)
            self.crm_businessDetails(browser, currentTime().strftime('%m%d %H:%M'))

    def crm_registerSales(self, browser, sales) :
        if sales == self.opportunity : addSalesBtn = 'items.type1'
        elif sales == self.product : addSalesBtn = 'items.type8'
        browser_click(browser, varname.businessRegistration)
        time.sleep(1)
        browser_click(browser, addSalesBtn, CLASS_NAME)
        progress(browser)
        self.crm_searchAccount(browser)
        self.crm_businessDetails(browser, sales)
        time.sleep(1)
        self.crm_duplicateSales(browser)
        time.sleep(1)

    def crm_registerOpportunity(self, browser) :
        self.crm_registerSales(browser, self.opportunity)
        if context(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td/div') != '영업기회' :
            raise Exception('영업기회 추가 확인 필요')
        
    def crm_registerGoods(self, browser) :
        self.crm_registerSales(browser, self.product)
        if context(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td/div') != '판매상품' :
            raise Exception('판매상품 추가 확인 필요')

    def crm_opportunity(self, browser) :
        browser_click(browser, 'btn.btn_search', CLASS_NAME)
        time.sleep(1)
        enter(browser, varname.searchCrm, self.opportunity)
        time.sleep(3)
        browser_click(browser, varname.searchCrmList)
        progress(browser)
        
        # 요구사항 분석 단계
        textClear(browser, varname.crmAmount1)
        enter(browser, varname.crmAmount1, '105000')
        enter(browser, varname.crmItem, '품목이란')
        enter(browser, varname.crmRequest, '여기에는 요청사항을 써주세요')
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2.next', CLASS_NAME)
        progress(browser)
        
        # 제안 및 검토 단계
        textClear(browser, varname.crmAmount2)
        enter(browser, varname.crmAmount2, '100000')
        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2.next', CLASS_NAME)
        progress(browser)

        # 수주여부 선택 (실패 > 재개 > 성공)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2.next', CLASS_NAME)
        browser_click(browser, varname.orderFail)
        progress(browser)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2.next', CLASS_NAME)
        browser_click(browser, varname.confirm)
        progress(browser)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2.next', CLASS_NAME)
        browser_click(browser, varname.orderSuccess)
        progress(browser)

    def crm_addContactPerson(self, browser) :
        browser_click(browser, varname.crmAccountManagemet)
        progress(browser)
        browser_click(browser, varname.contactPerson)
        browser_click(browser, varname.addContactPerson)
        time.sleep(1)
        browser_sendKey(browser, varname.contactPersonName, '이사장')
        browser_sendKey(browser, varname.contactPersonDepartment, '더존')
        browser_sendKey(browser, varname.contactPersonNumber, '01012341234')
        browser_click(browser, varname.register)
        progress(browser)
        if not hasxpath(browser, 'manager_cardlist_item', CLASS_NAME) :
            raise Exception('crm 담당자 등록 확인 필요')

    def crm_deleteContactPerson(self, browser) :
        browser_click(browser, varname.crmAccountManagemet)
        progress(browser)
        browser_click(browser, varname.contactPerson)
        browser_click(browser, varname.contactPersonOption)
        time.sleep(1)
        browser_click(browser, varname.contactPersonDelete)
        browser_click(browser, varname.confirm)
        progress(browser)
        if hasxpath(browser, 'manager_cardlist_item', CLASS_NAME) :
            raise Exception('crm 담당자 삭제 확인 필요')

    def crm_issueManagement(self, browser) :
        browser_click(browser, varname.crmAccountManagemet)
        progress(browser)
        browser_click(browser, varname.crmIssueManagement)
        browser_click(browser, 'LUX_basic_btn.Default.basic', CLASS_NAME)
        progress(browser)
        # 제목, 내용 입력
        browser_sendKey(browser, varname.crm_issueName, 'CRM 이슈 제목입력')
        browser_sendKey(browser, varname.crm_issueContent, 'CRM 이슈 본문입력')
        # 지도 내용 추가
        browser_click(browser, 'LUX_basic_btn.Image.btn_map', CLASS_NAME)
        time.sleep(3)
        enter(browser, '//*[@id="keyword"]', '에버랜드')
        browser_click(browser, 'placesList', ID)
        browser_click(browser, varname.crm_issueConfirm)
        # 할일 추가
        browser_click(browser, 'chk_todo', CLASS_NAME)
        browser_click(browser, varname.crm_registerIssue)
        time.sleep(1)

        # 할일 완료까지
        if hasxpath(browser, 'btn_prog', CLASS_NAME) :
            browser_click(browser, 'btn_prog', CLASS_NAME)
        else :
            raise Exception('crm 이슈등록 확인 필요')

    def crm_salesInformation(self, browser) :
        browser_click(browser, varname.crmAccountManagemet)
        progress(browser)
        browser_click(browser, varname.salesInformation)
        browser_click(browser, varname.directInputSales)
        time.sleep(3)
        browser_sendKey(browser, varname.inputSupplyValue, '70000')
        browser_sendKey(browser, varname.inputTaxAmount, '7000')
        browser_click(browser, 'inputElement', ID)
        time.sleep(0.5)
        browser_click(browser, varname.salesInformationList)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
        progress(browser)
        if not '70,000' in context(browser, 'summary_bx', CLASS_NAME) :
            raise Exception('CRM 매출정보 등록 확인 필요')

    def crm_deleteSalesInformation(self, browser) :
        browser_click(browser, varname.crmAccountManagemet)
        progress(browser)
        browser_click(browser, varname.salesInformation)
        time.sleep(3)
        Common().canvasClick(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]', 10, 160)
        browser_click(browser, varname.deleteSalesInformation)

    def crm_deleteSales(self, browser) :
        self.crm_basicset(browser)
        time.sleep(1)
        li_click(browser, '대시보드')
        time.sleep(3)
        Common().canvasClick(browser, '//*[@id="salesListGrid"]/div/canvas', 16, 16)
        time.sleep(1)
        #캔버스에서 요소가 없으면 클릭되어도 액션바가 미노출 됨
        if checkText(browser, WSC_LUXButton, delete) :
            btn_click(browser, WSC_LUXButton, delete)
            progress(browser)
            browser_click(browser, varname.confirm)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        Common().close(browser)

    def crm_account(self, browser, bname, blicense) :
        browser_click(browser, varname.crmAccountManagemet)
        progress(browser)
        browser_click(browser, varname.registerCrmAccount)
        progress(browser)
        browser_sendKey(browser, varname.registerCrmName, bname)
        browser_sendKey(browser, varname.registerCrmBusiness, blicense)
        browser_sendKey(browser, varname.registerCrmRepresent, '김대표')
        browser_click(browser, varname.register)
        progress(browser)
        text = '이미 등록된 거래처입니다.'
        if sameText(browser, text) :
            browser_click(browser, varname.confirm)
            browser_click(browser, varname.crmCancel)
            time.sleep(3)

    def crm_registerAccounts (self, browser) :
        self.crm_account(browser, 'CRM 테스트', '0980980983')
        textClear(browser, varname.searchCrmAccount)
        enter(browser, varname.searchCrmAccount, 'CRM 테스트')
        time.sleep(1)
        if hasxpath(browser, 'nodata_area.nodata_area_v3', CLASS_NAME) :
            raise Exception('crm 거래처 추가 확인 필요')

    def crm_deleteAccounts (self, browser) :
        browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[1]/div/div/div/div/div[1]/div[2]/ul/li[2]')
        time.sleep(1)
        enter(browser, varname.searchCrmAccount, 'CRM 테스트')
        progress(browser)
        if hasxpath(browser, 'nodata_area.nodata_area_v3', CLASS_NAME) :
            print('삭제할 crm 거래처 없음')
        else :
            browser_click(browser, varname.crmList)
            browser_click(browser, varname.crmOption)
            time.sleep(1)
            browser_click(browser, varname.deleteCrm)
            browser_click(browser, varname.confirm)
            progress(browser)
            if context(browser, varname.duplicatePopup) == '영업이 있는 거래처는 삭제할 수 없습니다.' :
                browser_click(browser, varname.confirm)

        textClear(browser, varname.searchCrmAccount)
        enter(browser, varname.searchCrmAccount, 'CRM 테스트')
        if not hasxpath(browser, 'nodata_area.nodata_area_v3', CLASS_NAME) :
            raise Exception('crm 거래처 삭제 확인 필요')
    
    def crm_addSalesInforDetail(self, browser, sales) :
        browser_click(browser, varname.crmAccountManagemet)
        time.sleep(3)
        li_click(browser, '매출정보')
        btn_click(browser, WSC_LUXButton, '매출정보')
        if sameText(browser, '거래처에 수주된 영업이 없습니다.') :
            Common().close(browser)
            raise Exception('영업 등록 확인 필요')
        else :
            time.sleep(3)
            browser.find_element(By.XPATH, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/table/tbody/tr[3]/td/div/div/div/input').send_keys('1056000')
            browser_click(browser, 'inputElement', ID)
            time.sleep(1)
            li_click(browser, sales)
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '등록')

    def crm_addSalesInfor(self, browser) :
        self.crm_addSalesInforDetail(browser, self.opportunity)
        self.crm_addSalesInforDetail(browser, self.product)

    def crm_delSalesInfor(self, browser) : 
        browser_click(browser, varname.crmAccountManagemet)
        time.sleep(3)
        li_click(browser, '매출정보')
        time.sleep(1)
        Common().canvasClick(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/object', 5, 5)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '매출정보 삭제')
        btn_click(browser, WSC_LUXButton, confirm)
        progress(browser)

    def crm_addGoals(self, browser) :
        li_click(browser, '목표설정')
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.Default.basic', '신규사업 목표')
        browser_sendKey(browser, varname.crm_goal, '12345678900')
        btn_click(browser, WSC_LUXButton, confirm)
        Common().close(browser)
        time.sleep(3)
        if not hasxpath(browser, 'card_selected_0', ID) : raise Exception('신규사업 목표 추가 확인 필요')

    def crm_copyGoals(self, browser) : 
        browser_click(browser, 'sp_crm', CLASS_NAME)
        time.sleep(0.1)
        li_click(browser, '복사')
        time.sleep(0.1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        if not hasxpath(browser, 'card_selected_1', ID) : raise Exception('신규사업 목표 복사 확인 필요')

    def crm_delGoals(self, browser) :
        browser.get(getUrl('wecrm/goalSetting'))
        time.sleep(5)
        while True : 
            time.sleep(1)
            if hasxpath(browser, 'sp_crm', CLASS_NAME) :
                browser_click(browser, 'sp_crm', CLASS_NAME)
                time.sleep(1)
                li_click(browser, '삭제')
                btn_click(browser, WSC_LUXButton, confirm)
                time.sleep(3)
            else : break
        if hasxpath(browser, 'card_selected_0', ID) : raise Exception('신규사업 목표 삭제 확인 필요')

class Wepms :
    internalPj='사내'; externalPj='외부'; crmPj='CRM수주'; nneeww='NNEEWW'
    def pms_basicset(self, browser) :
        if hasxpath(browser, 'pms_basicset_tit_btn', CLASS_NAME) :
            browser_click(browser, 'pms_basicset_tit_btn', CLASS_NAME)
            Company().cs_setAdministor(browser)
        else :
            if hasxpath(browser, 'pms_basicset_tit', CLASS_NAME) :
                browser_click(browser, varname.pmsBasicsetNext1)
                browser_click(browser, varname.pmsBasicsetNext2)
                time.sleep(0.5)
                for i in range(1,4) :
                    basicset = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[8]/div/div[2]/div/div/div[1]/div/div[3]/div/div[2]/div/div/div[1]/button['
                    basicset = basicset + str(i) + ']'
                    browser_click(browser, basicset)
                    time.sleep(0.5)
                    browser_sendKey(browser, varname.pmsBasicsetContent, '테스트')
                    browser_sendKey(browser, varname.pmsBasicsetContent, Keys.ENTER)
                    time.sleep(1)
                browser_click(browser, varname.pmsBasicsetNext3)
                browser_click(browser, varname.pmsToCrm)
                browser_click(browser, varname.confirm)
                browser_click(browser, varname.pmsBasicSave)
                browser_click(browser, varname.pmsStart)
                time.sleep(5)

    def pms_settingUse(self, browser) :
        li_click(browser, setting)
        # 예산수립, crm연동, 전자결재연동 사용
        btn = browser.find_elements(By.CLASS_NAME, 'LUX_basic_switch')
        for i in btn[0::2] :
            i.click()
            time.sleep(0.1)
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(0.1)
        btn = browser.find_elements(By.CLASS_NAME, 'WSC_LUXRadioButton')
        for i in btn[0::2] :
            i.click()
            time.sleep(0.1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)

    def pms_settingUnuse(self, browser) :
        li_click(browser, setting)
        # 예산수립, crm연동, 전자결재연동 사용
        btn = browser.find_elements(By.CLASS_NAME, 'LUX_basic_switch')
        for i in btn[1::2] :
            i.click()
            time.sleep(0.1)
            btn_click(browser, WSC_LUXButton, confirm)
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(0.1)
        btn = browser.find_elements(By.CLASS_NAME, 'WSC_LUXRadioButton')
        for i in btn[1:4:2] :
            i.click()
            time.sleep(0.1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)

    def pms_addProjectTypeDetail(self, browser, name) :
        li_click(browser, setting)
        time.sleep(1)
        browser_click(browser, '//*[@id="pms_admin_tab"]/div/ul/li[2]')
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.Default.basic', '유형추가')
        time.sleep(3)
        if name == self.externalPj :
            btn_click(browser, 'WSC_LUXRadioButton', '외부')
        elif name == self.crmPj :
            btn_click(browser, 'WSC_LUXRadioButton', '외부')
            time.sleep(0.5)
            btn_click(browser, 'WSC_LUXRadioButton', 'WE CRM')

        browser_sendKey(browser, varname.addProjectType, self.nneeww+name)
        btn_click(browser, 'LUX_basic_btn.Default.basic', '찾기')
        browser_click(browser, 'WSC_LUXCheckBox', CLASS_NAME)
        btn_click(browser, 'LUX_basic_btn.Confirm.basic2', save)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '등록')
        time.sleep(3)

    def pms_addProjectType(self, browser) :
        self.pms_addProjectTypeDetail(browser, self.internalPj)
        self.pms_addProjectTypeDetail(browser, self.externalPj)
        self.pms_addProjectTypeDetail(browser, self.crmPj)

    def pms_deleteProjectType(self, browser) :
        li_click(browser, setting)
        time.sleep(1)
        browser_click(browser, '//*[@id="pms_admin_tab"]/div/ul/li[2]')
        time.sleep(1)
        btn = browser.find_elements(By.CLASS_NAME, 'LS_form')
        for i in btn[-1:2:-1] : 
            i.click()
            time.sleep(0.1)
        btn_click(browser, WSC_LUXButton, delete)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)

    def pms_addUse(self, browser) :
        li_click(browser, setting)
        time.sleep(1)
        browser_click(browser, '//*[@id="pms_admin_tab"]/div/ul/li[4]')
        time.sleep(1)
        browser_click(browser, 'pms_adminset_btn', CLASS_NAME)
        time.sleep(1)
        browser_sendKey(browser, varname.pms_addUse, 'pms용도도')
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '추가')
        time.sleep(1)
        if sameText(browser, '동일한 용도명이 존재합니다.') : 
            btn_click(browser, WSC_LUXButton, confirm)
            browser_sendKey(browser, varname.pms_addUse, currentTime().strftime('%H:%M'))
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '추가')
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        progress(browser)

    def pms_delUse(self, browser) :
        li_click(browser, setting)
        time.sleep(1)
        browser_click(browser, '//*[@id="pms_admin_tab"]/div/ul/li[4]')
        time.sleep(3)
        if hasxpath(browser, 'btn_func', CLASS_NAME) :
            browser_click(browser, 'btn_func', CLASS_NAME)
            time.sleep(1)
            browser_click(browser, varname.pms_delUse)
            btn_click(browser, WSC_LUXButton, confirm)
        else : print('삭제할 용도 없음')
        time.sleep(3)

    def pms_searchProject(self, browser, name) :
        enter(browser, '//*[@id="project_search_input"]', name)
        time.sleep(1)
        count = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[3]/div[1]/div[3]/div[1]/div/em'
        if context(browser, count) == '00' :
            return False
        else :
            return True

    def pms_clickProjectType(self, browser, name) :
        self.pms_basicset(browser)
        browser_click(browser, varname.projectManagement)
        time.sleep(3)
        browser_click(browser, 'register_btn', CLASS_NAME)
        time.sleep(5)
        browser.find_element(By.XPATH, f'//div[1]/li[contains(., "{name}")]').click()
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '다음')
        progress(browser)

    def pms_inputProject(self, browser, name, pm=True) :
        browser_sendKey(browser, varname.pmsProjectName, name)
        browser_sendKey(browser, varname.estimatedRevenue, '1056000')
        if not pm :
            textClear(browser, varname.projectManager)
            inputUser(browser, varname.projectManager)
            time.sleep(0.5)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '등록')
        progress(browser)
        text = '동일한 이름의 프로젝트가 존재합니다.'
        if sameText(browser, text) :
            browser_click(browser, varname.confirm)
            time.sleep(0.5)
            browser_sendKey(browser, varname.pmsProjectName, currentTime().strftime('%m%d %H:%M'))
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '등록')
            progress(browser)

        time.sleep(1)
        if not self.pms_searchProject(browser, name) :
            raise Exception(name +' 프로젝트 등록 확인 필요')

    def pms_registerProject(self, browser, name) :
        self.pms_clickProjectType(browser, name)
        text1 = '영업 정보가 없습니다.'; text2 = '거래처 정보가 없습니다.'
        if sameText(browser, text1) or sameText(browser, text2) :
            browser_click(browser, varname.confirm)
            browser_click(browser, varname.pmsPrevios)
            time.sleep(1)
            browser_click(browser, varname.pmsCancel)
        else :
            if self.internalPj in name : 
                self.pms_inputProject(browser, name)
            elif self.externalPj in name :
                enter(browser, '//*[@id="search_crm_value"]', 'CRM 테스트')
                progress(browser)
                browser_click(browser, varname.pmsAccountList)
                browser_click(browser, varname.next)
                progress(browser)
                self.pms_inputProject(browser, name)
            elif self.crmPj in name :
                browser_click(browser, varname.pmsCrmList)
                browser_click(browser, varname.next)
                btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '등록')
                progress(browser)

    def pms_registerCrmProject(self, browser) :
        self.pms_registerProject(browser, self.crmPj)

    def pms_registerExternalProject(self, browser) :
        self.pms_registerProject(browser, self.externalPj)

    def pms_registerInternalProject(self, browser) :
        self.pms_registerProject(browser, self.internalPj)

    def pms_registerCrmProject_new(self, browser) :
        self.pms_registerProject(browser, self.nneeww+self.crmPj)

    def pms_registerExternalProject_new(self, browser) :
        self.pms_registerProject(browser, self.nneeww+self.externalPj)

    def pms_registerInternalProject_new(self, browser) :
        self.pms_registerProject(browser, self.nneeww+self.internalPj)

    def pms_manpower(self, browser) :
        browser_click(browser, varname.projectManagement)
        progress(browser)
        browser_click(browser, varname.manpower)
        browser_click(browser, varname.addUser)
        progress(browser)
        inputUser(browser, '//*[@id="inputSearch-TK"]')
        if sameText(browser, '검색결과가 없습니다.') :
            browser_click(browser, varname.confirm)
            Common().close(browser)
        else : 
            browser_click(browser, varname.pmsUserList)
            time.sleep(1)
            browser_click(browser, varname.addButton)
            browser_click(browser, varname.registUser)
            progress(browser)

        count = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/strong/em'
        if context(browser, count) != '2' :
            raise Exception('참여인력 확인 필요')

    def pms_schedulePlan(self, browser) :
        browser_click(browser, varname.projectManagement)
        progress(browser)
        browser_click(browser, varname.schedulePlan)
        time.sleep(3)
        browser_click(browser, '//*[@id="gantt_task"]/div/div[1]/div[1]/div/div/div[2]/div[1]/div[2]/div[3]')
        action = ActionChains(browser)
        action.send_keys(' 테스트11').pause(1).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(1)
    
    def pms_budget(self, browser) :
        browser_click(browser, varname.projectManagement)
        progress(browser)
        li_click(browser, '예산수립')
        time.sleep(1)
        browser_click(browser, 'newbtn.sp_pms_before', CLASS_NAME)
        time.sleep(3)
        browser_sendKey(browser, varname.budgetName, '예산서1번')
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', confirm)
        progress(browser)
        # 예산상세 입력
        browser_click(browser, 'prj_budget_item', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'additem.sp_pms_before', CLASS_NAME)
        time.sleep(3)
        browser_sendKey(browser, varname.budgetDetail, '예산11')
        browser_sendKey(browser, varname.budgetAmount, '10000')
        time.sleep(1)
        if sameText(browser, '프로젝트 매출액을 초과했습니다.') :
            browser_click(browser, varname.confirm)
        else :
            browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
            time.sleep(3)
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[1])
            Approval().ap_pms(browser)

        time.sleep(3)

        if not hasxpath(browser, 'stat_label.sp_pms_before.complete', CLASS_NAME) :
            raise Exception('예산서 등록 확인 필요')

    def pms_budgetExecution(self, browser) :
        li_click(browser, '프로젝트 관리')
        if self.pms_searchProject(browser, self.internalPj) :
            li_click(browser, '예산집행정보')
            btn_click(browser, 'LUX_basic_btn.Default.basic', '현금지출 등록')
            if sameText(browser, '등록된 용도가 없습니다.') : 
                btn_click(browser, WSC_LUXButton, confirm)
                self.pms_addUse(browser)
                browser.back()
                time.sleep(3)
                btn_click(browser, 'LUX_basic_btn.Default.basic', '현금지출 등록')
            enter(browser, varname.budgetExecutionName, '엄마손김밥')
            browser_sendKey(browser, varname.budgetExecutioniAmount, '10000')
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '집행등록')
            time.sleep(5)
            pageDown(browser, 'prjmgmt_section_top.v2', CLASS_NAME)
            Common().canvasClick(browser, '//*[@id="mainGrid"]', 5,5)
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, '전자결재')
            time.sleep(3)
            browser.switch_to.window(browser.window_handles[1])
            Approval().ap_pms(browser, True)
            # btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '최종결산')

    def pms_delBudgetExecution(self, browser) :
        li_click(browser, '프로젝트 관리')
        time.sleep(1)
        if self.pms_searchProject(browser, self.internalPj) :
            li_click(browser, '예산집행정보')
            time.sleep(1)
            pageDown(browser, 'prjmgmt_section_top.v2', CLASS_NAME)
            Common().canvasClick(browser, '//*[@id="mainGrid"]', 5,5)
            btn_click(browser, WSC_LUXButton, delete)
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', delete)
        else : print('프로젝트 없음')
        
    def pms_createIssue(self, browser) :
        browser_click(browser, varname.projectManagement)
        progress(browser)
        li_click(browser, '이슈관리')
        progress(browser)
        browser_click(browser, varname.addIssue)
        progress(browser)
        browser_sendKey(browser, varname.issueName, '이슈제목입력')
        browser_sendKey(browser, varname.issueContent, '이슈상세내용')
        time.sleep(1)
        browser_click(browser, varname.saveIssue)
        progress(browser)

        if not hasxpath(browser, 'itemlist', CLASS_NAME) :
            raise Exception('이슈 생성 확인 필요')
    
    def pms_deleteProject(self, browser) :
        browser.get(getUrl('wepms'))
        time.sleep(5)
        browser_click(browser, varname.projectManagement)
        time.sleep(1)
        while hasxpath(browser, varname.projectOption) :
            browser_click(browser, varname.projectOption)
            time.sleep(1)
            browser_click(browser, varname.deleteProject)
            progress(browser)
            browser_click(browser, varname.confirm)
            progress(browser)

        if hasxpath(browser, 'projectitem', CLASS_NAME) :
            raise Exception('프로젝트 삭제 확인 필요')

    def pms_usercreateIssue(self, browser) :
        self.pms_clickProjectType(browser, self.internalPj)
        self.pms_inputProject(browser, varname.name_addUser)
        self.pms_manpower(browser)

        user = browser.find_elements(By.XPATH, '//*[contains(@id, "join_worker")]/div/div/div[3]/div/button[2]')
        for i in user :
            i.click()
            if context(browser, varname.confirm) == '확인' :
                browser_click(browser, varname.confirm)
            time.sleep(0.1)
        browser_click(browser, '//*[@id="app"]/div/div[2]/div[2]/div[1]/div/button[2]')
        time.sleep(1)

    def pms_userProjectManamger(self, browser) :
        self.pms_clickProjectType(browser, self.internalPj)
        self.pms_inputProject(browser, varname.name_userManager, pm=False)
        
class Note :
    def nt_createSharedSpace (self, browser) :
        browser_click(browser, varname.sharedNote)
        browser_sendKey(browser, varname.sharedNoteName, '공유지식공간명' + currentTime().strftime('%H%M'))
        inputUser(browser, '//*[@id="inputSearch"]')
        browser_click(browser, varname.createShared_ntBtn)
        time.sleep(1)
        if not hasxpath(browser, varname.shardNoteList) :
            raise Exception('공유지식공간 생성 확인 필요')

    def nt_deleteSharedSpace (self, browser) :
        while hasxpath(browser, varname.shardNoteList) :
            self.nt_administor(browser)
            browser_click(browser, varname.shardNoteList)
            time.sleep(1)
            browser_click(browser, 'btn_edit', CLASS_NAME)
            browser_click(browser, varname.deleteSharedNote)
            browser_click(browser, varname.confirm)
            time.sleep(1)

        if hasxpath(browser, varname.shardNoteList) :
            raise Exception('공유지식공간 삭제 확인 필요')

    def nt_administor (self, browser) :
        time.sleep(3)
        browser_click(browser, varname.shardNoteList)
        browser_click(browser, 'LUX_basic_btn.nt_share_btn', CLASS_NAME)
        progress(browser)
        if hasxpath(browser, varname.sharedUserList) :
            browser_click(browser, varname.sharedUserList)
            browser_click(browser, '/html/body/div[4]/div/div/div[2]/div/ul/li[3]')
            browser_click(browser, varname.confirm)
        Common().close(browser)
        time.sleep(3)
        
    def nt_createNote (self, browser) :
        time.sleep(3)
        browser_click(browser, varname.createNote)
        browser_sendKey(browser, varname.noteTitle, '노트제목')
        time.sleep(1)
        browser_click(browser, 'LUX_basic_btn.Small.basic.btn_change', CLASS_NAME)
        browser_click(browser, 'note_list_item_all', ID)
        browser_click(browser, varname.confirm_nt)
        time.sleep(3)
        browser.switch_to.frame(0)
        time.sleep(1)
        browser.find_element(By.XPATH, '//*[@id="dzeditor_0"]').click()
        action = ActionChains(browser)
        action.send_keys('대박드디어썼다ㅠㅠㅠ').perform()
        browser.switch_to.default_content()
        time.sleep(1)
        browser_click(browser, varname.createNoteBtn)
        progress(browser)

        if not hasxpath(browser, varname.noteList) :
            raise Exception('노트 생성 확인 필요')

    def nt_deleteNote (self, browser) :
        browser_click(browser, varname.noteList)
        progress(browser)
        browser_click(browser, varname.noteSelectAll)
        time.sleep(1)
        browser_click(browser, varname.deleteNote)
        browser_click(browser, varname.confirm)
        progress(browser)

        if not hasxpath(browser, 'nodata_area', CLASS_NAME) :
            raise Exception('노트 삭제 확인 필요')

    def nt_emptyTrash (self, browser) :
        time.sleep(10)
        browser_click(browser, 'is_trash', CLASS_NAME)
        browser_click(browser, varname.noteSelectAll)
        browser_click(browser, varname.notePermanentDelete)
        browser_click(browser, varname.confirm)
        progress(browser)

        count = '//*[@id="root"]/div/div[1]/div[1]/div/div/div/div/div/div/div[3]/div[1]'
        if not '휴지통0' in context(browser, count) :
            raise Exception('노트 휴지통 비우기 확인 필요')

class Attendance :
    distribute='배포'; undistribute='배포해제'; attendanceItem='전자결재연동외근'
    setWorkingGroup='근로제그룹설정'; setWorkingPlace='근무지그룹설정'; atPolicy='근태정책'; setVacation='휴가설정'
    setHoliday='휴일지정'; setAuthorization='권한부여'
    def at_assign(self, browser, assign) :
        time.sleep(3)
        if assign == self.undistribute :
            browser_click(browser, varname.assignedUser)
            time.sleep(1)

        Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div/canvas', 16, 16)
        time.sleep(3)
        text = browser.find_element(By.XPATH, varname.attendanceButton).text
        # 근로그룹배포, 근로그룹제외, 근무지배포, 근무지제외 버튼이 있으면 클릭
        if text :
            browser_click(browser, varname.attendanceButton)
            browser_click(browser, varname.confirm)
        time.sleep(1)

    def at_unassignmet(self, browser) :
        time.sleep(1)
        # browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div[1]/ul/li[2]')
        attendanceList = browser.find_elements(By.CLASS_NAME, 'WSC_LUXTooltip')
        if attendanceList :
            for a in attendanceList :
                a.click()
                self.at_assign(browser, self.undistribute)
                time.sleep(1)

    def at_settingWorkingGroup(self, browser) :
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setWorkingGroup)
        browser_click(browser, 'LUX_basic_btn.list_top_btn', CLASS_NAME)
        time.sleep(0.5)
        browser_sendKey(browser, varname.workingGroupName, '일반근로제')
        browser_click(browser, varname.breaktime)
        btn_click(browser, WSC_LUXButton, save)
        time.sleep(1)
        if hasxpath(browser,'//*[@id="BODY_CLASS"]/div[3]/div[4]/div[2]/div/div/div[1]/h1') :
            browser_click(browser, varname.confirmAttendance)

        if context(browser, varname.at_count) == '0개' :
            raise Exception('근로 그룹 추가 확인 필요')

    def at_assignmentWorkingGroup(self, browser) :
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setWorkingGroup)
        browser_click(browser, varname.assignmentWorkingGroup)
        self.at_assign(browser, self.distribute)

    def at_unassignmentWorkingGroup(self, browser) :
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setWorkingGroup)
        browser_click(browser, varname.assignmentWorkingGroup)
        self.at_unassignmet(browser)

    def at_deleteWorkingGroup(self, browser) :
        self.at_unassignmentWorkingGroup(browser)
        time.sleep(1)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setWorkingGroup)
        browser_click(browser, varname.workingGroupList)
        attendanceList = browser.find_elements(By.CLASS_NAME, 'WSC_LUXPopover')
        if attendanceList :
            for a in attendanceList :
                browser_click(browser, varname.attendanceOption)
                time.sleep(1)
                browser_click(browser, varname.deleteWorkingGroup)
                time.sleep(1)

        if context(browser, varname.at_count) != '0개' :
            raise Exception('근로 그룹 삭제 확인 필요')

    def at_settingWorkingPlace(self, browser) :
        time.sleep(1)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setWorkingPlace)
        browser_click(browser, 'LUX_basic_btn.list_top_btn', CLASS_NAME)
        time.sleep(1)
        browser_sendKey(browser, varname.workingPlaceName, '서비스QA팀')
        time.sleep(3)
        action = ActionChains(browser)
        action.send_keys(Keys.TAB).send_keys(Keys.ENTER).pause(1).send_keys(' 버들1길130').pause(0.5).send_keys(Keys.ENTER).pause(1)
        action.send_keys(Keys.TAB*3).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(1)
        browser_click(browser, varname.searchWifi)
        btn_click(browser, WSC_LUXButton, '등록')
        time.sleep(1)

        if context(browser, varname.at_count) == '0개' :
            raise Exception('근무지 그룹 추가 확인 필요')
        
    def at_assignmentWorkingPlace(self, browser) :
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setWorkingPlace)
        browser_click(browser, varname.assignmentWorkingPlace)
        time.sleep(1)
        self.at_assign(browser, self.distribute)
    
    def at_unassignmentWorkingPlace(self, browser) :
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setWorkingPlace)
        browser_click(browser, varname.assignmentWorkingPlace)
        time.sleep(1)
        self.at_unassignmet(browser)             

    def at_deleteWorkingPlace(self, browser) :
        self.at_unassignmentWorkingPlace(browser)
        time.sleep(1)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setWorkingPlace)
        browser_click(browser, varname.workingPlaceList)
        attendanceList = browser.find_elements(By.CLASS_NAME, 'row_lnk')
        if attendanceList :
            for a in attendanceList :
                browser_click(browser, 'LUX_basic_btn.Image.basic', CLASS_NAME)
                browser_click(browser, varname.deleteWorkingPlace)
                if sameText(browser, '선택한 근무지에 배포된 직원이 존재합니다.') : 
                    browser_click(browser, varname.confirm)
                    break
                else :
                    browser_click(browser, varname.confirm)
                time.sleep(1)

        if context(browser, varname.at_count) != '0개' :
            raise Exception('근무지 그룹 삭제 확인 필요')

    def at_attendacneClassification(self, browser) :
        browser_click(browser, varname.attendanceMypage)
        time.sleep(1)
        Common().close(browser)
        browser_click(browser, 'btn_apply', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.outsideWork)
        self.at_undistributeWork(browser)
        time.sleep(10)
        browser.switch_to.window(browser.window_handles[1])

        for i in range(0,30) :
            if not hasxpath(browser, varname.approvalName) :
                time.sleep(1)
            else : break

        atlist = browser.find_elements(By.ID, 'inputElement')
        if self.attendanceItem == atlist[-1].text :
            return True
        else :
            return False

    def at_addAttendanceItem(self, browser) : 
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.atPolicy)
        browser_click(browser, varname.attendanceItem)
        browser_click(browser, 'LUX_basic_btn.list_top_btn', CLASS_NAME)
        browser.find_element(By.XPATH, varname.attendacneClassification).send_keys(self.attendanceItem)
        browser_click(browser, 'WSC_LUXRadioButton', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
        time.sleep(3)
        # 근태구분에 추가한 항목 없는 경우 실패
        try :
            if not self.at_attendacneClassification(browser) :
                raise Exception('전자결재에 연동 확인')
        finally :
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(3)

    def at_deleteAttendanceItem(self, browser) :
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.atPolicy)
        browser_click(browser, varname.attendanceItem)
        time.sleep(1)
        attendanceItem = browser.find_elements(By.CLASS_NAME, 'LUX_basic_btn.Image.basic')
        if attendanceItem :
            for a in attendanceItem :
                browser_click(browser, 'LUX_basic_btn.Image.basic', CLASS_NAME)
                browser_click(browser, varname.deleteAttendanceItem)
                browser_click(browser, varname.confirm)
                time.sleep(1)

        # 근태구분에 추가한 항목 없는 경우 실패
        try :
            if self.at_attendacneClassification(browser) :
                raise Exception('전자결재에 연동 확인')
        finally :
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            time.sleep(3)

    def at_settingVacation(self, browser) :
        # Common().close(browser)
        # li_click(browser, '서비스관리')
        # btn_click(browser, 'group_box.is_num', self.setVacation)
        browser_click(browser, varname.settingEmployeeVacation)
        browser_click(browser, varname.serviceYear)
        time.sleep(1)
        enter(browser, varname.searchAttendance, usersName(browser))
        vacation = '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div[3]/div[1]/ul[2]/li/div/div[5]'
        if browser.find_element(By.XPATH, vacation).text == '' :
            browser_click(browser, varname.selectEmployee)
            btn_click(browser, WSC_LUXButton, '기본부여')
            browser_sendKey(browser, varname.dayOfVacation, '10')
            btn_click(browser, WSC_LUXButton, save)
            time.sleep(1)
    
    def at_vacation(self, browser, assign) :
        Common().close(browser)
        time.sleep(1)
        if not hasxpath(browser, 'apply_bx.on', CLASS_NAME) :
            browser_click(browser, 'btn_apply', CLASS_NAME)
        time.sleep(1)
        if assign == '취소' :
            browser_click(browser, 'slick-next.slick-arrow', CLASS_NAME)
            time.sleep(1)
            browser_click(browser, varname.vacationApplicationCancel)
        else :
            browser_click(browser, varname.vacationApplication)
        self.at_undistributeWork(browser)
        time.sleep(5)

    def at_vacationApplication(self, browser) :
        self.at_vacation(browser, '신청')
        browser.switch_to.window(browser.window_handles[1])
        Approval().ap_attendanceVacation(browser)
        time.sleep(1)
        Common().close(browser)
        num = browser.find_element(By.CLASS_NAME, 'btn_state').text
        # 잔여 휴가일수가 9개가 아니면 에러
        if '9개' not in num :
            raise Exception('휴가 신청 확인 필요')

    def at_vacationApplicationCancel(self, browser) :
        self.at_vacation(browser, '취소')
        browser.switch_to.window(browser.window_handles[1])
        Approval().ap_attendanceVacationCancel(browser)
        time.sleep(1)
        Common().close(browser)
        num = browser.find_element(By.CLASS_NAME, 'btn_state').text
        # 잔여 휴가일수가 10개가 아니면 에러
        if '10개' not in num :
            raise Exception('휴가 신청 취소 확인 필요')

    def at_undistributeWork(self, browser) :
        if sameText(browser, '근로제가 배포되어있지 않습니다.') :
            browser_click(browser, varname.confirm)
            raise Exception('근로제 미배포 상태??')

    def at_registerholiday(self, browser) :
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setHoliday)
        browser_click(browser, 'LUX_basic_btn.list_top_btn', CLASS_NAME)
        time.sleep(1)
        browser_sendKey(browser, varname.holidayName, '오늘은 휴일입니다.')
        browser_click(browser, varname.registerHolidayBtn)
        time.sleep(1)
        if not hasxpath(browser, 'card_ico01', CLASS_NAME) :
            raise Exception('휴일 등록 확인 필요')

    def at_deleteHoliday(self, browser) :
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setHoliday)
        attendance = browser.find_elements(By.CLASS_NAME, 'card_ico01')
        for at in attendance :
            at.click()
            if checkText(browser, WSC_LUXButton, delete) :
                btn_click(browser, WSC_LUXButton, delete)
                btn_click(browser, WSC_LUXButton, confirm)
                time.sleep(1)
            else :
                Common().close(browser)
                time.sleep(1)

    def at_authorization(self, browser) :
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setAuthorization)
        browser_click(browser, 'LUX_basic_btn.list_top_btn', CLASS_NAME)
        time.sleep(1)
        enter(browser, '//*[@id="inputSearch-TK2"]', usersName(browser))
        browser_click(browser, 'point_color', CLASS_NAME)
        browser_click(browser, 'sp_rnb.btn_add', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, '전체부서 관리')
        time.sleep(3)
        num = '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div[2]/div/div/div/div/div[2]/div[1]/div[2]/h4/span'
        if '0명' in context(browser, num) :
            raise Exception('근태관리 권한부여 확인 필요')

    def at_deauthorization(self, browser) :
        Common().close(browser)
        li_click(browser, '서비스관리')
        btn_click(browser, 'group_box.is_num', self.setAuthorization)
        Common().canvasClick(browser, '//*[@id="gridBase"]/div/canvas', 16, 16)
        btn_click(browser, WSC_LUXButton, '조직권한자 제외')
        time.sleep(3)
        num = '//*[@id="BODY_CLASS"]/div[3]/div[1]/div/div/div/div[2]/div/div/div/div/div[2]/div[1]/div[2]/h4/span'
        if not '0명' in context(browser, num) :
            raise Exception('근태관리 권한해제 확인 필요')

class Expense :
    approval='승인['; refusal='승인거절['; wait='승인대기['
    def expenseInformation(self, browser, card) :
        # 경비정보입력
        progress(browser)
        time.sleep(1)
        if hasxpath(browser, varname.cCardExpenseContent) :
            browser_click(browser, varname.cCardExpenseContent)
            textClear(browser, varname.cCardExpenseContent)
        else : 
            browser_click(browser, varname.pCardExpenseContents)
            textClear(browser, varname.pCardExpenseContents)
        time.sleep(0.3)
        # Common().fileUpload(browser, 'btn_webot.png')
        action = ActionChains(browser)
        action.send_keys(card + '내용').send_keys(Keys.TAB).send_keys(card + '목적').send_keys(Keys.TAB).perform()
        action.reset_actions()
        time.sleep(3)
        browser_click(browser, varname.expenseMeal)
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.saobtn.basic2', '경비청구')
        progress(browser)
        
        if '필수정보 누락' in context(browser, varname.duplicatePopup) :
            browser_click(browser, varname.confirm)
            Common().fileUpload(browser, 'btn_webot.png')
            time.sleep(1)
            btn_click(browser, 'LUX_basic_btn.saobtn.basic2', '경비청구')
            progress(browser)

    def scraping(self, browser, card) :
        time.sleep(1)
        if card == '법인카드' :
            li_click(browser, '지출관리')
        else :
            browser.get(getUrl('expensepersonalcard/cardusagestatement'))
        time.sleep(10)
        browser_click(browser, 'sp_cr.ico_update', CLASS_NAME)
        time.sleep(3)
        Common().close(browser)
        if hasxpath(browser, varname.scrapingNotice) :
            browser_click(browser, varname.scrapingNotice)
        progress(browser)
        err = browser.find_elements(By.CLASS_NAME, 'LUX_basic_btn.SAOverConfirm.basic2')
        for i in err :
            if i.text == '자세히보기' :
                i.click()
                raise Exception('스크래핑 오류?')
        self.scraping_hasHistory(browser)

    def scraping_hasHistory(self, browser) :
        if sameText(browser, '최근 사용내역 업데이트 이력이 존재합니다.') :
            time.sleep(1)
            # 방금전에 사용내역 업데이트 한 경우라면 3분 대기
            browser_click(browser, varname.confirm)
            print('3분 대기 후 재스크래핑')
            waitseconds(180)
            browser_click(browser, 'sp_cr.ico_update', CLASS_NAME)

    def scrapingErr(self, browser):
        path = os.getcwd()
        filename = '/' + currentTime().strftime('%m%d') + '사용내역 업데이트 실패.png'
        if hasxpath(browser, 'dialog_data.dialog_data_icon', CLASS_NAME) :
            browser_click(browser, varname.scrapingErr)
            browser.save_screenshot(path + filename)
            Login().logout(browser)
            Login().login(browser, 'hancho1')
            browser.get('https://www.wehago.com/#/communication2/talk/VapzR3cBqq7xHM_q0h6e')
            time.sleep(5)
            if "자동화 리포트용" in browser.title :
                browser.find_element_by_css_selector("input[type='file']").send_keys(filename)
        time.sleep(3)

    def ex_selectField(self, browser, text) :
        # 미진행건만 클릭
        browser_click(browser, 'WSC_LUXSelectField', CLASS_NAME)
        time.sleep(1)
        for i in range(1,8) : 
            selectField = '//*[@id="scrollElement"]/div/ul/div['
            selectField = selectField + str(i) + ']'
            if hasxpath(browser, selectField) :
                selectFieldText = browser.find_element(By.XPATH, selectField).text
                if text in selectFieldText :
                    browser_click(browser, selectField)
                    break
            else :
                break
        time.sleep(1)

    def ex_statusTabClick(self, browser, status) :
        time.sleep(1)
        if status == '수정요청' :
            browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[8]/div[5]/div[2]/div/div[1]/ul/li[4]')
        else :
            browser.find_element(By.XPATH, f'//li[contains(., "{status}")]').click()
        time.sleep(1)
        action = ActionChains(browser)
        expense = browser.find_element(By.XPATH, '//*[@id="gridRequestApprovalList"]/div/canvas')
        width = expense.size['width']*0.9
        action.move_to_element_with_offset(expense,width,45).click().perform()
        action.reset_actions()
        time.sleep(0.5)

    def ex_statusCancel(self, browser, status) :
        browser.find_element(By.XPATH, '//li[contains(., "경비관리")]').click()
        time.sleep(5)

        while not '[0건]' in context(browser, f'//li[contains(., "{status}")]'):
            self.ex_statusTabClick(browser, status)
            btn = browser.find_elements(By.CLASS_NAME, 'LUX_basic_btn.saobtn.basic')
            btn[1].click()
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, confirm)
            progress(browser)

    def ex_statusWait(self, browser, status) :
        browser.find_element(By.XPATH, '//li[contains(., "경비관리")]').click()
        time.sleep(5)
        self.ex_statusTabClick(browser, self.wait)
        if status == self.approval :
            browser_click(browser, 'LUX_basic_btn.saobtn.basic2', CLASS_NAME)
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(3)
        elif status == self.refusal :
            btn_click(browser, 'LUX_basic_btn.saobtn.basic', '거절')
            action = ActionChains(browser)
            btn = browser.find_elements(By.CLASS_NAME, 'WSC_LUXTextArea')
            btn[1].click()
            action.send_keys('거절거절').perform()
            action.reset_actions()
            btn_click(browser, 'LUX_basic_btn.saobtn.basic', '거절')
            time.sleep(3)
        elif status == '수정요청' :
            time.sleep(1)
            btn_click(browser, 'LUX_basic_btn.saobtn.basic', '수정요청')
            action = ActionChains(browser)
            action.send_keys(Keys.ENTER).perform()
            action.reset_actions()
            btn = browser.find_elements(By.CLASS_NAME, 'WSC_LUXTextArea')
            btn[1].click()
            action = ActionChains(browser)
            action.send_keys('쑤정').perform()
            action.reset_actions()
            btn_click(browser, 'LUX_basic_btn.saobtn.basic', '수정요청')

    def ex_request(self, browser) :
        # 승인대기 > 수정요청
        browser.find_element(By.XPATH, '//li[contains(., "경비관리")]').click()
        time.sleep(5)
        if not '[0건]' in context(browser, f'//li[contains(., "{self.wait}")]'):
            self.ex_statusWait(browser, '수정요청')
        else :
            print('경비관리 승인대기 건 없음')

    def ex_approve(self, browser) :
        # 승인대기 > 승인
        browser.find_element(By.XPATH, '//li[contains(., "경비관리")]').click()
        time.sleep(5)
        if not '[0건]' in context(browser, f'//li[contains(., "{self.wait}")]'):
            self.ex_statusWait(browser, self.approval)
        else :
            print('경비관리 승인대기 건 없음')

    def ex_reject(self, browser) :
        # 승인대기 > 승인거절
        browser.find_element(By.XPATH, '//li[contains(., "경비관리")]').click()
        time.sleep(5)
        if not '[0건]' in context(browser, f'//li[contains(., "{self.wait}")]'):
            self.ex_statusWait(browser, self.refusal)
        else :
            print('경비관리 승인대기 건 없음')

    def ex_approveCancel(self, browser) :
        # 승인 > 승인대기
        self.ex_statusCancel(browser, self.approval)

    def ex_rejectCancel(self, browser) :
        # 승인거절 > 승인대기
        self.ex_statusCancel(browser, self.refusal)

class CorporateCard(Expense) :
    returnCard='카드반납'
    def cca_clause(self, browser) :
        if hasxpath(browser, varname.cCardStart) :
            browser_click(browser, varname.cCardStart)

    def cca_cardRegist(self, browser) :
        time.sleep(3)
        # 서비스관리 탭으로 이동하여 법인카드 홈페이지로 이동
        li_click(browser, '카드관리')
        time.sleep(3)
        if hasxpath(browser, varname.cCardRegist) :
            browser_click(browser, varname.cCardRegist)
            time.sleep(1)
            browser_click(browser, varname.cCardKB)
            browser_click(browser, 'LUX_basic_text', CLASS_NAME)
            action = ActionChains(browser)
            # 용민주임님꺼 국민카드
            action.send_keys('6258').send_keys(Keys.TAB).send_keys('0405').send_keys(Keys.TAB).send_keys('0739').send_keys(Keys.TAB).send_keys('9006')
            action.send_keys(Keys.TAB*3).send_keys('PYM3362').send_keys(Keys.TAB).send_keys('dydalsqa@1').perform()
            action.reset_actions()
            browser_click(browser, varname.expensNext)
            while True :
                time.sleep(3)
                if context(browser, varname.registComplete) == '등록완료' :
                    browser_sendKey(browser, varname.cardName, '국민카드')
                    browser_click(browser, varname.registComplete)
                    time.sleep(5)
                    break
        else : 
            print('카드등록되어있음')

    def cca_returnCard(self, browser) :
        browser.find_element(By.XPATH, '//li[contains(., "카드관리")]').click()
        time.sleep(3)
        if checkText(browser, 'LUX_basic_btn.SAOverConfirm.basic2', self.returnCard) :
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', self.returnCard)
            time.sleep(1)
            if hasxpath(browser, 'WSC_LUXLinearChart', CLASS_NAME) :
                if checkText(browser, 'WSC_LUXLinearChart', '상태오류') :
                    Common().close(browser)
                    browser.find_element(By.XPATH, '//li[contains(., "지출관리")]').click()
                    time.sleep(3)
                    self.cca_statusError(browser)
                    self.cca_returnCard(browser)
                elif checkText(browser, 'WSC_LUXLinearChart', '결재필요') :
                    Common().close(browser)
                    browser.find_element(By.XPATH, '//li[contains(., "지출관리")]').click()
                    time.sleep(3)
                    self.cca_requestApproval(browser)
                    self.cca_returnCard(browser)
            if hasxpath(browser, varname.returnCardReason) :
                browser_sendKey(browser, varname.returnCardReason, '법인카드 반납 진행')
        
            btn_click(browser,WSC_LUXButton, self.returnCard)
            time.sleep(1)
        else : 
            raise Exception('법인카드 미지급되었는지 확인 필요')

        if checkText(browser, 'LUX_basic_btn.SAOverConfirm.basic2', self.returnCard) :
            raise Exception('법인카드 반납 확인 필요')

    def cca_setAdminstor(self, browser) :
        li_click(browser, setting)
        time.sleep(3)
        inputUser(browser, varname.ccaAdminstor)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)
        browser.find_element(By.XPATH, '//li[contains(., "카드관리")]').click()
        time.sleep(3)
        if not hasxpath(browser, 'tag_name', CLASS_NAME) :
            raise Exception('법인카드 경비관리자 설정 확인 필요')

    def cca_unsetAdminstor(self, browser) :
        li_click(browser, setting)
        time.sleep(3)
        browser_click(browser, varname.cca_delAdminstor)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)
        browser.find_element(By.XPATH, '//li[contains(., "카드관리")]').click()
        time.sleep(3)
        if hasxpath(browser, 'tag_name', CLASS_NAME) :
            raise Exception('법인카드 경비관리자 설정 확인 필요')

    def cca_settingUse(self, browser) :
        li_click(browser, setting)
        time.sleep(3)
        btn = browser.find_elements(By.CLASS_NAME, 'LUXrabx')
        for i in btn[0::2] :
            i.click()
            time.sleep(0.1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)

    def cca_settingUnuse(self, browser) :
        li_click(browser, setting)
        time.sleep(3)
        btn = browser.find_elements(By.CLASS_NAME, 'LUXrabx')
        btn[1].click()
        time.sleep(0.5)
        btn_click(browser, WSC_LUXButton, confirm)
        for i in btn[4:] :
            i.click()
            time.sleep(0.1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)

    def cca_changeStatus(self, browser) :
        action = ActionChains(browser)
        expense = browser.find_element(By.XPATH, '//*[@id="gridCheckBox"]/div')
        # 상태 클릭하여 정렬
        action.move_to_element_with_offset(expense,45,16).click()
        action.move_to_element_with_offset(expense,16,45).click().perform()
        action.reset_actions()
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, '미진행상태 변경')
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        progress(browser)

    def cca_cardProvision(self, browser) :
        time.sleep(3)
        if checkText(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '카드지급') :
            browser_click(browser, varname.longTermUse)
            textClear(browser, varname.usagePurpose)
            browser_sendKey(browser, varname.usagePurpose, '법인카드지급')
            browser_sendKey(browser, varname.approveAmount, '100000')
            enter(browser, varname.cardUser, usersName(browser))
            enter(browser, varname.cardManager, usersName(browser))
            time.sleep(1)
            browser_click(browser, varname.paymentDay)
            time.sleep(3)
            btn_click(browser, WSC_LUXButton, '오늘')
            time.sleep(1)
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '카드지급')
            time.sleep(1)
            browser.refresh()
            time.sleep(3)
        elif checkText(browser, 'LUX_basic_btn.SAOverConfirm.basic2', self.returnCard) :
            print('카드 미반납 상태')
        else : 
            self.cca_cardRegist(browser)
            self.cca_cardProvision(browser)

        if not hasxpath(browser, varname.returnCard) :
            raise Exception('법인카드 지급 확인 필요')

    def cca_scraping(self, browser) :
        self.cca_cardProvision(browser)
        self.scraping(browser, '법인카드')

    def cca_statusError (self, browser) :
        self.ex_selectField(browser, '상태오류')
        time.sleep(1)
        Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div', 45, 45)
        time.sleep(1)
        Common().canvasClick(browser, '//*[@id="gridCancelList"]/div/canvas', 16, 16)
        time.sleep(0.5)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '취소분변경')
        btn_click(browser, WSC_LUXButton, confirm)
        progress(browser)
        browser.refresh()
        time.sleep(5)

    def cca_expensClaimDetail(self, browser) :
        self.ex_selectField(browser, '미진행')
        Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div', 45, 45)
        time.sleep(10)
        # 결재필요 상태 클릭한 경우
        if context(browser, 'LUX_basic_btn.saobtn.basic2', CLASS_NAME) == '전자결재하기' :
            btn_click(browser, 'LUX_basic_btn.saobtn.basic', '미진행상태 변경')
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(0.5)
        else :
            time.sleep(1)
            self.expenseInformation(browser, '법인카드')

    def cca_countScraping(self, browser) :
        browser.find_element(By.XPATH, '//li[contains(., "지출관리")]').click()
        progress(browser)
        # 미진행건
        none = '//*[@id="BODY_CLASS"]/div[3]/div[3]/div/div/div/div/div/div[7]/div[2]/div[1]/div[2]/ul/li[4]/span[2]'
        noneCount = browser.find_element(By.XPATH, none).text
        # 상태오류건
        labels = '//*[@id="BODY_CLASS"]/div[3]/div[3]/div/div/div/div/div/div[7]/div[2]/div[1]/div[2]/ul/li[5]/span[1]'
        err = '//*[@id="BODY_CLASS"]/div[3]/div[3]/div/div/div/div/div/div[7]/div[2]/div[1]/div[2]/ul/li[5]/span[2]'
        if hasxpath(browser, err) :
            if context(browser, labels) == '상태오류' :
                errCount = browser.find_element(By.XPATH, err).text
            else : 
                errCount = '0건'
        else :
            errCount = '0건'

        return noneCount, errCount
    
    def cca_expenseClaim(self, browser) :
        noneCount, errCount = self.cca_countScraping(browser)

        # 상태오류건이 있을때
        if errCount != '0건' :
            # 상태오류 n건 취소분상태로 변경
            self.cca_statusError(browser)

        # 미진행건 n건 > 경비청구 진행
        if noneCount != '0건' :
            self.cca_expensClaimDetail(browser)

    def cca_requestApproval(self, browser) :
        Common().close(browser)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)
        noneCount, errCount = self.cca_countScraping(browser)
        if noneCount != '0건' :
            self.ex_selectField(browser, '미진행')
            action = ActionChains(browser)
            expense = browser.find_element(By.XPATH, '//*[@id="gridCheckBox"]/div')
            # 상태 클릭하여 정렬
            action.move_to_element_with_offset(expense,45,16).click()
            action.move_to_element_with_offset(expense,45,45).click().perform()
            action.reset_actions()
            if wehagoBrand == 3 : time.sleep(15)
            else : time.sleep(5)
            progress(browser)
            time.sleep(1)
            if checkText(browser, 'LUX_basic_btn.saobtn.basic2', '전자결재하기') :
                btn_click(browser, 'LUX_basic_btn.saobtn.basic2', '전자결재하기')
                if wehagoBrand == 3 : time.sleep(30)
                else : time.sleep(5)
                browser.switch_to.window(browser.window_handles[1])
                # 전자결재 승인 진행
                Approval().ap_expense(browser, '법인카드')
            else : 
                Common().close(browser)
                btn_click(browser, WSC_LUXButton, confirm)
                raise Exception('법인카드 전자결재 확인 필요')
        else : print('전자결재 할 경비청구 없음')

    def cca_expenseClaimRequest(self, browser) :
        li_click(browser, '경비관리')
        progress(browser)
        while True :
            time.sleep(1)
            if not '[0건]' in context(browser, '//*[@id="BODY_CLASS"]/div[3]/div[3]/div/div/div/div/div/div[13]/div[2]/div/div[1]/ul/li[4]'):
                time.sleep(1)
                browser.find_element(By.XPATH, '//*[@id="BODY_CLASS"]/div[3]/div[3]/div/div/div/div/div/div[13]/div[2]/div/div[1]/ul/li[4]/button').click()
                time.sleep(1)
                action = ActionChains(browser)
                expense = browser.find_element(By.XPATH, '//*[@id="gridRequestApprovalList"]/div/canvas')
                width = expense.size['width']*0.9
                action.move_to_element_with_offset(expense,width,45).click().perform()
                action.reset_actions()
                time.sleep(0.5)
                time.sleep(3)
                browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div[3]/div/div/div/div/div/div[4]/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[2]/button[2]')
                btn_click(browser, WSC_LUXButton, confirm)
                time.sleep(1)
            else : break
        # li_click(browser, '수정요청')
        time.sleep(3)
        
    def cca_expenseClaimRequest222(self, browser) :
        li_click(browser, '경비관리')
        progress(browser)
        btn_click(browser, 'LUX_basic_btn.Default.basic', '상세')
        time.sleep(3)
        browser_click(browser, 'WSC_LUXSelectField', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, '//*[@id="scrollElement"]/div/ul/div[4]/li/a/div')
        time.sleep(3)
        action = ActionChains(browser)
        btn_click(browser, 'item_tit', '지출일자')
        action.send_keys(Keys.TAB).perform()
        # browser_click(browser, 'WSC_LUXDatePicker', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '당월')
        btn_click(browser, WSC_LUXButton, confirm)
        btn_click(browser, 'LUX_basic_btn.Default.basic', '상세검색')
        time.sleep(1)
        action = ActionChains(browser)
        expense = browser.find_element(By.XPATH, '//*[@id="gridCheckBox"]/div')
        action.move_to_element_with_offset(expense,45,45).click().perform()
        action.reset_actions()
        time.sleep(3)
        try :
            if hasxpath(browser, 'text_red', CLASS_NAME) :
                pageDown(browser, 'text_red', CLASS_NAME)
                btn_click(browser, 'LUX_basic_btn.saobtn.basic2', '수정완료')
                progress(browser)
            else : raise Exception('법인카드 수정요청 확인 필요')
        finally : 
            Common().close(browser)
            btn_click(browser, WSC_LUXButton, confirm)

    def cca_statusRequest(self, browser) :
        self.ex_statusTabClick(browser, self.wait)
        btn_click(browser, 'LUX_basic_btn.saobtn.basic', '수정요청')
        browser_sendKey(browser, varname.cCardReason, '쑤정')
        btn_click(browser, 'LUX_basic_btn.saobtn.basic', '수정요청')

    def cca_request(self, browser) :
        browser.find_element(By.XPATH, '//li[contains(., "경비관리")]').click()
        time.sleep(5)
        if not '[0건]' in context(browser, f'//li[contains(., "{self.wait}")]'):
            self.ex_statusWait(browser, '수정요청')
        else :
            print('경비관리 승인대기 건 없음')

    def cca_approve(self, browser) :
        browser.find_element(By.XPATH, '//li[contains(., "경비관리")]').click()
        time.sleep(5)
        # 승인대기 > 승인
        if not '[0건]' in context(browser, f'//li[contains(., "{self.wait}")]'):
            self.ex_statusWait(browser, self.approval)
        else :
            print('경비관리 승인대기 건 없음')

    def cca_reject(self, browser) :
        # 승인대기 > 승인거절
        if not '[0건]' in context(browser, f'//li[contains(., "{self.wait}")]'):
            self.ex_statusWait(browser, self.refusal)
        else :
            print('경비관리 승인대기 건 없음')

    def cca_approveCancel(self, browser) :
        # 승인 > 승인대기
        self.ex_statusCancel(browser, self.approval)

    def cca_rejectCancel(self, browser) :
        # 승인거절 > 승인대기
        self.ex_statusCancel(browser, self.refusal)

class PersonalCard(Expense) :
    def pca_clause(self, browser) :
        if hasxpath(browser, 'LS_form', CLASS_NAME) :
            browser_click(browser, 'LS_form', CLASS_NAME)
            browser_click(browser, varname.pCardAggree)
            time.sleep(1)
            browser_click(browser, varname.pCardStart)
            time.sleep(3)

    def pca_addManager(self, browser) :
        btn_click(browser, WSC_LUXButton, '경비관리자 추가')
        if usersName(browser) == '한초희' :
            browser_click(browser, '//*[@id= "memberbx_1"]')
        else :
            browser_click(browser, '//*[@id= "memberbx_0"]')
        time.sleep(1)
        browser_click(browser, 'sp_rnb.btn_add', CLASS_NAME)
        if sameText(browser, '이미 경비관리자로 지정된 직원입니다.') :
            btn_click(browser, WSC_LUXButton, confirm)
            Common().close(browser)
        else :
            btn_click(browser, WSC_LUXButton, '관리부서 지정')
            time.sleep(1)
            browser_click(browser, 'LUX_basic_btn.Image.basic.btn_next', CLASS_NAME)
            time.sleep(1)
            browser_click(browser, varname.pCardSaveManagement)
            time.sleep(1)
            if sameText(browser, '지정된 관리부서가 없습니다.') :
                browser_click(browser, varname.confirm)
                Common().close(browser)

    def pca_expenseManager(self, browser) :
        expense = '//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div/div[1]/div/h1'
        if hasxpath(browser, expense) :
            if context(browser, expense) == '지정된 경비관리자 없음' :
                browser_click(browser, varname.confirm)
                self.pca_addManager(browser)

    def pca_settingUse(self, browser) :
        li_click(browser, setting)
        time.sleep(3)
        btn = browser.find_elements(By.CLASS_NAME, 'LUXrabx')
        btn[0].click()
        time.sleep(0.5)
        btn_click(browser, WSC_LUXButton, confirm)
        for i in btn[2:9:2] :
            i.click()
            time.sleep(0.1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)

    def pca_checkUse(self, browser) :
        browser.get(getUrl('expensepersonalcard/expendituremanagement'))
        time.sleep(5)
        if not hasxpath(browser, 'sec_date.txt_red', CLASS_NAME) : raise Exception('경비마감일자 사용설정 확인 필요')
        btn_click(browser, 'LUX_basic_btn.Default.basic.fltlft', '경비지출 직접입력')
        try :
            time.sleep(0.5)
            if '귀속월' not in context(browser, varname.pca_checkUse1) : raise Exception('귀속월 사용설정 확인 필요')
            pageDown(browser, varname.pca_checkUse1)
            browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[5]/div[1]/div/div[2]/div[3]/div[2]/table/tbody/tr[4]/td/div/div/div/div[1]/div[1]/div')
            time.sleep(0.5)
            if not hasxpath(browser, '//li[contains(., "주유비(자동계산)")]') : raise Exception('주유비 사용설정 확인 필요')
        finally : Common().close(browser)
    
    def pca_settingUnuse(self, browser) :
        li_click(browser, setting)
        time.sleep(3)
        btn = browser.find_elements(By.CLASS_NAME, 'LUXrabx')
        btn[1].click()
        btn[3].click()
        time.sleep(0.5)
        btn_click(browser, WSC_LUXButton, confirm)
        for i in btn[5:10:2] :
            i.click()
            time.sleep(0.1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', save)
        time.sleep(1)

    def pca_clickExpenseClaim(self, browser) :
        self.pca_expenseManager(browser)
        browser.find_element(By.XPATH, '//div[2]/ul/li[contains(., "경비청구")]').click()
        time.sleep(5)

    def pca_cardRegist(self, browser) :
        self.pca_clickExpenseClaim(browser)
        if hasxpath(browser, varname.personalCardRegist) :
            browser_click(browser, varname.personalCardRegist)
            time.sleep(1)
            card = browser.find_element(By.CLASS_NAME, 'card_name')
            if card.text == '신한카드' :
                card.click()
            browser_click(browser, 'LUX_basic_text', CLASS_NAME)
            action = ActionChains(browser)
            action.send_keys('5594').send_keys(Keys.TAB).send_keys('1000').send_keys(Keys.TAB).send_keys('0563').send_keys(Keys.TAB).send_keys('5916')
            action.send_keys(Keys.TAB*2).send_keys('ianswldudi').send_keys(Keys.TAB).send_keys('ckacl118*').send_keys(Keys.TAB).send_keys('신한카드').perform()
            action.reset_actions()
            browser_click(browser, varname.pCardRegistButton)
            while True :
                time.sleep(3)
                if context(browser, varname.pcardRegistPopup) == '카드 등록완료' :
                    browser_click(browser, varname.confirm_pCard)
                    break
                elif hasxpath(browser, 'title_desc.txtcnt', CLASS_NAME) :
                    browser_click(browser, varname.scrapingErr)
                    time.sleep(0.5)
                    text = browser.find_element(By.XPATH, varname.scrapingErrMessage).text
                    if text == '이미 등록된 카드입니다.' :
                        browser_click(browser, varname.confirm_scraping)
                        browser_click(browser, varname.cancelPcard)
                        break
            time.sleep(3)
        else : print('카드 등록되어있음??')

    def pca_scraping (self, browser) :
        self.pca_expenseManager(browser)
        self.scraping(browser, '개인카드')
        if sameText(browser, '업데이트할 카드를 등록해주세요.') :
            time.sleep(1)
            print('카드 등록 필요')
            browser_click(browser, varname.confirm)
            self.pca_cardRegist(browser)
            self.scraping(browser, '개인카드')

    def pca_transmitExpenseClaim(self, browser) :
        self.pca_clickExpenseClaim(browser)
        action = ActionChains(browser)
        expense = browser.find_element(By.XPATH, '//*[@id="gridCheckBox"]/div')
        # 상태정보 클릭 후 가장 상단 내역 경비청구 진행
        width = expense.size['width']*0.7
        action.move_to_element_with_offset(expense,width,20).click().pause(1)
        action.move_to_element_with_offset(expense,16,45).click().perform()
        action.reset_actions()
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, '경비청구관리 전송')
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, '경비청구관리 이동')

    def pca_expenseManagement(self, browser) :
        # 경비청구 관리 클릭
        browser.get(getUrl('expensepersonalcard/expendituremanagement'))
        time.sleep(5)
        Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div', 16, 45)
    
    def pca_excludeDetails(self, browser) :
        browser.get(getUrl('expensepersonalcard/expendituremanagement'))
        time.sleep(3)
        self.ex_selectField(browser, '미진행')
        action = ActionChains(browser)
        expense = browser.find_element(By.XPATH, '//*[@id="gridCheckBox"]/div')
        action.move_to_element_with_offset(expense,45,45).click().perform()
        action.reset_actions()
        while True :
            time.sleep(1)
            Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div', 16, 45)
            if hasxpath(browser, varname.pCardActionLeft) :
                text = browser.find_element(By.XPATH, varname.pCardActionLeft).text
                if text == '경비 정보입력' or text == '전자결재' :
                    browser_click(browser, varname.excludeDetails)
                    browser_click(browser, varname.confirm)
                else : 
                    print('미진행건 아님')
                    break
            else :
                print('경비청구 없음')
                break

    def pca_expenseClaim(self, browser) :
        self.pca_expenseManagement(browser)
        time.sleep(1)
        # 경비 정보입력
        browser_click(browser, varname.pCardActionLeft)
        time.sleep(3)
        progress(browser)
        if not hasxpath(browser, varname.pCardApproval) :
            # 스크래핑 된 내역 경비정보입력
            self.expenseInformation(browser, '개인카드')
            time.sleep(3)
        else : 
            # 직접입력한 내역 경비정보입력X
            browser_click(browser, varname.pCardApproval)
            time.sleep(5)

    def pca_expenseClaimRequestDetail(self, browser, type) :
        browser.get(getUrl('expensepersonalcard/expendituremanagement'))
        time.sleep(5)
        btn_click(browser, 'LUX_basic_btn.Default.basic.fltlft', '상세')
        time.sleep(1)
        browser_click(browser, 'LUX_basic_select', CLASS_NAME)
        time.sleep(3)
        if type == '식대' : browser_click(browser, '//*[@id="scrollElement"]/div/ul/div[4]/li')
        elif type == '도서인쇄비' : browser_click(browser, '//*[@id="scrollElement"]/div/ul/div[3]/li')
        # btn = browser.find_elements(By.CLASS_NAME, 'LUX_basic_btn.Default.basic')
        # btn[-1].send_keys(Keys.ENTER)
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.Default.basic', '상세검색')
        progress(browser)
        while True :
            time.sleep(1)
            Common().canvasClick(browser, '//*[@id="gridCheckBox"]/div/canvas', 150, 45)
            progress(browser)
            select = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[3]/div[3]/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[1]/td/div/div/div/div[1]/div[1]/div'
            if hasxpath(browser, select) : 
                browser_click(browser, select)
                time.sleep(0.5)
                browser_click(browser, '//*[@id="scrollElement"]/div/ul/div[2]/li')
                pageDown(browser, 'text_red', CLASS_NAME)
                btn_click(browser, 'LUX_basic_btn.saobtn.basic2', '수정완료')
                progress(browser)
            else : 
                action = ActionChains(browser)
                action.send_keys(Keys.ESCAPE).pause(0.5).send_keys(Keys.ENTER).perform()
                time.sleep(1)
                break
        time.sleep(1)

    def pca_expenseClaimRequest(self, browser) :
        self.pca_expenseClaimRequestDetail(browser, '식대')
        self.pca_expenseClaimRequestDetail(browser, '도서인쇄비')

    def pca_requestApproval (self, browser) :
        self.ex_selectField(browser, '미진행')
        action = ActionChains(browser)
        expense = browser.find_element(By.XPATH, '//*[@id="gridCheckBox"]/div')
        # 상태 클릭하여 정렬
        action.move_to_element_with_offset(expense,45,16).click().pause(1)
        action.move_to_element_with_offset(expense,200,45).click().perform()
        action.reset_actions()
        time.sleep(3)

        btn_click(browser, 'LUX_basic_btn.saobtn.basic2', '전자결재하기')
        time.sleep(3)
        if len(browser.window_handles) == 2 :
            browser.switch_to.window(browser.window_handles[1])
            Approval().ap_expense(browser, '개인카드')
        else :
            print('전자결재건 아님')

    def pca_approve(self, browser) :
        # 승인대기 > 승인
        self.ex_statusWait(browser, self.approval)

    def pca_reject(self, browser) :
        # 승인대기 > 승인거절
        self.ex_statusWait(browser, self.refusal)

    def pca_approveCancel(self, browser) :
        # 승인 > 승인대기
        self.ex_statusCancel(browser, self.approval)

    def pca_rejectCancel(self, browser) :
        # 승인거절 > 승인대기
        self.ex_statusCancel(browser, self.refusal)

    def pca_request(self, browser) :
        browser.find_element(By.XPATH, '//li[contains(., "경비관리")]').click()
        time.sleep(5)
        if not '[0건]' in context(browser, f'//li[contains(., "{self.wait}")]'):
            self.ex_statusWait(browser, '수정요청')
        else :
            print('경비관리 승인대기 건 없음')
       
    def pca_directInput(self, browser, account=None) :
        if not account : account='엄마손김밥'
        browser.get(getUrl('expensepersonalcard/expendituremanagement'))
        time.sleep(5)
        btn_click(browser, 'LUX_basic_btn.Default.basic.fltlft', '경비지출 직접입력')
        time.sleep(1)
        Common().fileUpload(browser, 'btn_webot.png')
        browser_click(browser, 'WSC_LUXDatePicker', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '오늘')
        if hasxpath(browser, varname.directInputAccountName) : 
            accountInput = varname.directInputAccountName; cost = varname.directInputCost
        else : 
            accountInput = varname.directInputAccountName2; cost = varname.directInputCost2
        enter(browser, accountInput, account)
        browser_sendKey(browser, cost, '16000')
        time.sleep(0.5)
        action = ActionChains(browser)
        action.send_keys(Keys.TAB * 4).send_keys('지출내용').send_keys(Keys.TAB).send_keys('지출목적').pause(0.5).send_keys(Keys.TAB).pause(1).send_keys(Keys.DOWN*2).send_keys(Keys.ENTER).perform()
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '등록')
        browser_click(browser, varname.confirm)
        progress(browser)
        time.sleep(3)

        if hasxpath(browser, accountInput) :
            Common().close(browser)
            raise Exception('개인카드 직접입력 확인 필요')

    def pca_transferSlipDetail(self, browser, account=None) :
        print('전표전송')
        # 직접입력하고 > 결재승인하고 > 경비승인 > 전표전송처리 
        self.pca_directInput(browser, account)
        self.pca_expenseClaim(browser)
        self.pca_approve(browser)
        li_click(browser, '전체')
        Common().canvasClick(browser, '//*[@id="gridRequestApprovalList"]/div/canvas', 16, 45)
        browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div[8]/div[4]/div/div[1]/div/div[1]/div[1]/div/span')
        time.sleep(1)
        browser_click(browser, '//*[@id="scrollElement"]/div/ul/div[1]/li')
        progress(browser)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', '전표 전송')
        btn_click(browser, WSC_LUXButton, '취소')
        btn_click(browser, WSC_LUXButton, confirm)
        progress(browser)
        Common().close(browser)
        Common().canvasClick(browser, '//*[@id="gridRequestApprovalList"]/div/canvas', 830, 45)

    def pca_transferSlip(self, browser) :
        # 거래처 30글자 이하
        self.pca_transferSlipDetail(browser)
        self.pca_transferSlipDetail(browser, '가나다라마바사아자차카타파하가나다라마바사아자차카타파하가나다라마바사아자차카타파하')

class Pay :
    kb='국민카드'; shinhan='신한카드'
    def pay_shinhan(self, browser) :
        browser.switch_to.window(browser.window_handles[2])
        browser_click(browser, 'card-btn', CLASS_NAME)
        # 결제할 때까지 15초 대기 후 확인
        time.sleep(0.5)
        while True :
            waitseconds(15)
            browser_click(browser, 'btn.btn-primary', CLASS_NAME)
            time.sleep(1)
            if hasxpath(browser, 'btn.btn-default', CLASS_NAME) :
                browser_click(browser, 'btn.btn-default', CLASS_NAME)
            else :
                break
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[1])
        browser_click(browser, 'confirminfo', ID)
        browser_click(browser, 'btn_confirm', CLASS_NAME)
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[0])
        # elif hasxpath(browser, '//button[text()="1"]') :
        #     Common().setPassword(browser)

    def pay_kb(self, browser) :
        time.sleep(1)
        while True :
            time.sleep(1)
            if hasxpath(browser, 'confirminfo', ID) :
                browser_click(browser, 'confirminfo', ID)
                browser_click(browser, 'btn_confirm', CLASS_NAME)
                time.sleep(5)
                browser.switch_to.window(browser.window_handles[0])
                break
            else : waitseconds(15)
        time.sleep(5)

    def pay_card(self, browser, bank) : 
        if len(browser.window_handles) == 2 :
            browser.switch_to.window(browser.window_handles[1])
            browser_click(browser, varname.payAgree)
            browser_click(browser, varname.payNext)
            browser.find_element(By.XPATH, '//span[.="' + bank + '"]').click()
            browser_click(browser, 'btn_confirm', CLASS_NAME)
            time.sleep(3)
            if bank == self.kb : self.pay_kb(browser)
            elif bank == self.shinhan : self.pay_shinhan(browser)
            else : raise Exception('작업중')
        else : 
            print('0원결제?')

    def payment(self, browser, name) :
        time.sleep(3)
        Common().canvasClick(browser, 'dialog_content.mmd', 300, 200, CLASS_NAME)
        btn = browser.find_elements(By.CLASS_NAME, WSC_LUXButton)
        btnlist = []
        for i in btn :
            if i.text == '결제하기' :
                btnlist.append(i)
        btnlist[-1].click()

        time.sleep(3)
        if name == '박용민' : self.pay_card(browser, self.kb)
        else : self.pay_card(browser, self.shinhan)
        
class Market(Pay) :
    def market(self, browser, pay, name, service: dict, count=None) :
        if pay != 3 :
            # browser.get('https://www.wehago.com/#/market')
            if pay == 4 :
                browser.get('https://www.wehagot.com/#/market')
            else :
                browser.get('https://www.wehago.com/#/market')
            time.sleep(5)
            self.mk_purchaseService(browser, service, count)
            time.sleep(3)
            self.mk_payment(browser, name)
        else :
            print('마켓 구매 X')

    def mk_purchaseService (self, browser, service: dict, count=None) :
        for key, value in service.items() :
            if value == '구매O' :
                self.mk_addCart(browser, key, count)

    def mk_addCart (self, browser, name, count=None) :
        if not count : count = '3'
        li_click(browser, name)
        time.sleep(3)
        market = browser.find_element(By.XPATH, varname.buyButton).text
        if market == '바로구매' or market == '서비스사용':
            browser_click(browser, varname.buyButton)
            time.sleep(1)
            # if name == '회계관리' :
            #     browser_click(browser, 'sp_sm.plus', CLASS_NAME)
                
            if not (name == '전자결재' or name == '회사게시판' or name == 'WE빌더' or name == '내 PC 원격접속') :
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, varname.changedQuantity))).send_keys(count)
            if hasxpath(browser, varname.purchaseAgree) :
                browser_click(browser, 'LS_form', CLASS_NAME)
                # browser_click(browser, varname.purchaseAgree)
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, '장바구니 담기')
            browser_click(browser, varname.cancel)
        
        browser.back()
        time.sleep(1)

    def mk_payment (self, browser, name) :
        Common().close(browser)
        browser_click(browser, 'btn.btn_spcart', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.Confirm.basic', '결제')
        time.sleep(3)
        self.payment(browser, name)
        
        browser_click(browser, 'LUX_basic_btn.link', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, 'LUX_basic_btn.Small.basic', CLASS_NAME)
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, '결제')
        time.sleep(3)
        self.payment(browser, name)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)

class Join :
    def conditionAgree (self, browser) :
        #약관동의
        browser_click(browser, 'LS_form', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, '다음')
        time.sleep(1)
    
    def companyInformation(self, browser, pay, businessName=None, businessNum=None) :
        # 기업정보입력
        if not businessName : businessName = '테스트_테스트' + currentTime().strftime('%m%d')
        if not businessNum : businessNum = '1111111119'
        if pay == 4 or pay == 7 or pay == 8:
            browser.find_element(By.XPATH, '//*[@id="contnt"]/div[2]/div[2]/div[2]/div[2]/div/div/div/div/div/div/input').send_keys(businessNum)
            btn_click(browser, 'LUX_basic_btn.Confirm.basic', '중복확인')
            time.sleep(1)
            btn = '//*[@id="contnt"]/div[2]/div[2]/div[6]/div[2]/div/div/div[1]/div/div[1]/div[2]/div[2]/ul/li[1]'
            
            if hasxpath(browser, btn) :
                # 동일 사업자번호 있는 경우
                browser_click(browser, btn)
                time.sleep(3)
                textClear(browser, '//input[@type="text"]')
                browser_sendKey(browser, '//input[@type="text"]', businessName)
                
                if pay == 4 :
                    # T일 때 관리단위 입력 필요
                    action = ActionChains(browser)
                    action.send_keys(Keys.TAB*3).pause(1).send_keys(currentTime().strftime('%M')).send_keys(Keys.TAB).send_keys('김대표').send_keys(Keys.TAB*2).perform()
                    action.reset_actions()
                    time.sleep(1)
            else :
                # 동일 사업자번호 없는 경우
                browser_sendKey(browser, '//input[@type="text"]', businessName)
            btn_click(browser, WSC_LUXButton, '다음')
            progress(browser)
        else :
            # 사업자번호 미입력
            browser_sendKey(browser, '//input[@type="text"]', businessName)
            btn_click(browser, WSC_LUXButton, '다음')
            progress(browser)

    def certification (self, browser, name) :
        #본인 인증 단계
        self.cellNum(browser, name)
        time.sleep(1)
        # 초기화 안돌때는 플폼가서 초기화 할 시간 줌 
        if hasxpath(browser, varname.duplicateUser) :
            browser_click(browser, varname.cancel)
            waitseconds(15)
            self.cellNum(browser, name)

    def authentication(self, browser, brand) :
        if brand == 'sk' :
            brand = varname.sk
        elif brand == 'kt' :
            brand = varname.kt
        elif brand == 'lg' :
            brand = varname.lg 

        #본인인증
        if hasxpath(browser, varname.certification) :
            browser_click(browser, varname.certification)
        else : 
            browser_click(browser, varname.dt_certification)
        time.sleep(1)
        #창전환
        browser.switch_to.window(browser.window_handles[1])
        browser_click(browser, brand)

        agree = '//*[@id="ct"]/fieldset/ul[2]/li/span/label[1]'
        browser_click(browser, agree)
        if hasxpath(browser, 'btnSubmit', ID) :
            browser_click(browser, 'btnSubmit', ID)
        elif hasxpath(browser, 'btn_r.btn_type6.btn_r.btn_skip2', CLASS_NAME) :
            browser_click(browser, 'btn_r.btn_type6.btn_r.btn_skip2', CLASS_NAME)

    def cellNum (self, browser, name) :
        #사용자가 몇번째에 있는지
        num = userNumber(name)

        #사용자의 통신사 선택
        self.authentication(browser, userList[num][1])

        #핸드폰번호입력 // 이름/생년월일/성별(1,2)/핸드폰번호 순서로 입력 
        browser_sendKey(browser, 'username', userList[num][0], ID)
        browser_sendKey(browser, 'mynum1', userList[num][2], ID)
        browser_sendKey(browser, 'mynum2', userList[num][3], ID)
        browser_sendKey(browser, 'mobileno', userList[num][4], ID)

        browser_click(browser, 'answer', ID)

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        print('보안문자 입력')
        # 보안문자 입력할 때까지 10초 대기 후 확인
        while True :
            waitseconds(10)
            browser_click(browser, 'btnSubmit', ID)
            try :
                browser.switch_to.alert.accept()
                browser_click(browser, 'answer', ID)
            except :
                time.sleep(0.1)
                if context(browser, 'pop-tit', CLASS_NAME) == '인증 실패 안내' :
                    browser_click(browser, 'lastChild.defaultBtn.DefaultBtn', CLASS_NAME)
                else :
                    break

        time.sleep(1)
        print('인증번호 입력')
        # 인증번호 입력할 때까지 10초 대기 후 확인
        browser_click(browser, 'authnumber', ID)
        while True :
            waitseconds(10)
            browser_click(browser, 'btnSubmit', ID)
            time.sleep(1)
            try :
                browser.switch_to.alert.accept()
            except :
                break
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[0])

    def successSetId(self, browser, id) :        
        time.sleep(1)
        if hasxpath(browser, varname.duplicateUser) : 
            btn_click(browser, WSC_LUXButton, confirm)
        else : 
            id = id + '7'
            textClear(browser, '//input[@type="text"]')
            action = ActionChains(browser)
            action.send_keys(id).send_keys(Keys.TAB).perform()
            action.reset_actions()
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, '다음')
            time.sleep(5)
            self.successSetId(browser, id)
            
        print(id)
        # 파일에 id 쓰기
        path = os.getcwd()
        f = open(path+'/id.txt', 'w')
        f.write(id+'\n')
        f.close()

    def setId(self, browser, id, pay) :
        if pay  == 7 :
            mail = 'aaa'+currentTime().strftime('%M%H')+'@bbb.com'
        else : 
            mail = 'aaa@bbb.com' 
        time.sleep(0.5)
        if pay == 4 :
            btnInput = browser.find_elements(By.XPATH, '//input[@type="text"]')
            btnInput[2].click()
        else :
            browser_click(browser, '//input[@type="text"]')
        action = ActionChains(browser)
        action.send_keys(id).send_keys(Keys.TAB).send_keys('1q2w3e4r').send_keys(Keys.TAB).send_keys('1q2w3e4r').send_keys(Keys.TAB).send_keys(mail).perform()
        action.reset_actions()
        time.sleep(3)
        
        btn_click(browser, WSC_LUXButton, '다음')
        progress(browser)

        self.successSetId(browser, id)

    def wehagoJoin(self, browser, id, name, pay, businessName=None, businessNum=None) :
        if pay == 5 or pay == 6 :
            # 운영기 홈피스
            browser.get('https://www.wehago.com/#/join/allinone')
            time.sleep(5)
        elif pay == 4 : 
            # 운영기 티
            browser.get('https://www.wehagot.com/#/join/easyt/wehagot')
            time.sleep(5)
        elif pay == 7 :
            browser.get('https://www.wehago.com/#/join/easy/newbill')
            time.sleep(5)
            btn_click(browser, WSC_LUXButton, '회원가입')
        elif pay == 8 :
            browser.get('https://rnd.wehago.com/#/join/easy/rnd')
            time.sleep(5)
        else : 
            # 운영기 클럽, 프로, 싱글
            browser.get('https://www.wehago.com/#/join/choice')
            time.sleep(5)
            browser_click(browser, varname.planselect)
        #약관동의
        self.conditionAgree(browser)
        #본인인증
        self.certification(browser, name)
        #아이디생성
        self.setId(browser, id, pay)
        #회사정보입력
        self.companyInformation(browser, pay, businessName, businessNum)
        time.sleep(1)
        if pay == 7 : browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2.big_login_btn', CLASS_NAME)

    def employeeJoin(self, wehago) :
        path = os.getcwd()
        if platform.system() == 'Windows' :
            browser2 = webdriver.Chrome(path + '\\chromedriver.exe')
        elif platform.system() == 'Darwin' :
            browser2 = webdriver.Chrome(path + '/chromedriver')
        browser2.maximize_window()

        Login().naver_login(browser2)
        if len(browser2.window_handles) == 2 :
            browser2.switch_to.window(browser2.window_handles[1])
            time.sleep(3)
            browser_click(browser2, varname.employeeJoin)
            if wehago == 4 :
                Login().login(browser2, 'tqatest123')
            else :
                Login().login(browser2, 'qatest123')
                time.sleep(3)
            browser2.quit()
        else :
            print('qatest123 계정으로 가입 필요')

    def joinID(self, browser, id) :
        browser_sendKey(browser, varname.dt_id, id)
        browser_sendKey(browser, varname.dt_id, Keys.TAB)

        time.sleep(1)
        browser_click(browser, varname.dt_pw)
        mail = id+'@bill36524.com'
        action = ActionChains(browser)
        action.send_keys('bizon#720').send_keys(Keys.TAB).send_keys('bizon#720').send_keys(Keys.TAB).send_keys(mail).perform()
        action.reset_actions()
        time.sleep(3)
        browser_click(browser, varname.dt_nextButtonUser)
        time.sleep(5)
        browser_click(browser, varname.confirm)

class Plan(Pay) :
    club='club'; pro='pro';single='single';wehago='wehagot';dt='allinone'
    def plan_payment(self, browser, plan, name) :
        time.sleep(1)
        pageDown(browser, 'contents_top_wrap', CLASS_NAME)
        if plan == self.wehagot :
            browser_click(browser, varname.tPay)
            time.sleep(1)
        else :
            btn_click(browser, 'LUX_basic_btn.txtcnt', '연단위')
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, '결제하기')
        self.payment(browser, name)

    def plan_payment2222(self, browser, plan, name) :
        time.sleep(1)
        pageDown(browser, 'contents_top_wrap', CLASS_NAME)
        if plan == self.wehagot :
            browser_click(browser, varname.tPay)
            time.sleep(1)
        else :
            if plan == self.single :
                browser_click(browser, varname.annualSinglePayment)
            elif plan != self.dt :
                browser_click(browser, varname.annualPayment)
            time.sleep(1)
            browser_click(browser, 'section.mt.nopd', CLASS_NAME)
        time.sleep(1)
        self.payment(browser, name)

    def userCount(self, browser, xpath, count=None) :
        textClear(browser, xpath)
        if not count : count = '3'
        browser_sendKey(browser, xpath, count)
        time.sleep(0.5)

    def init_cardClick(self, browser) :
        card = browser.find_element(By.XPATH, '//*[@id="BODY_CLASS"]/div[2]/div/div/div[3]/div/div[1]/div[1]/div[2]/div[2]/ul/li[3]')
        action = ActionChains(browser)
        action.move_to_element_with_offset(card, 30, 240).click().move_by_offset(0, 200).click().perform()
        action.reset_actions()
        time.sleep(0.5)
        
    def buycard(self, browser) :
        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        card = browser.find_element(By.XPATH, '//*[@id="BODY_CLASS"]/div[2]/div/div/div[3]/div/div[1]/div[1]/div[2]/div[2]/ul/li[3]')
        action = ActionChains(browser)
        action.move_to_element_with_offset(card, 30, 240).click().move_by_offset(0, 200).click().perform()
        action.reset_actions()
        time.sleep(0.5)
        for i in range(3,5) :
            service = '//*[@id="BODY_CLASS"]/div[2]/div/div/div[3]/div/div[1]/div[1]/div[2]/div[2]/ul/li[3]/div/div['
            service = service + str(i) + ']/div/div[2]/div/div/input'
            textClear(browser, service)
            browser.find_element(By.XPATH, service).send_keys('3')
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def single_click(self, browser, count=None) :
        #서비스 클릭
        for i in range(1,13) :
            service = '//*[@id="BODY_CLASS"]/div[2]/div/div/div[3]/div/div[1]/div[2]/div[1]/div[2]/div/ul/li['
            service = service + str(i) + ']'
            browser_click(browser, service)
            time.sleep(0.1)
            #전자결재, 근태관리는 이미 체크되어 있어 제외
            if i == 7:
                continue
            else :
                countXpath = service + '/div/div[1]/dl/dd[2]/div/div[1]/input'
                self.userCount(browser, countXpath, count)

    def club(self, browser, name, count=None) :
        time.sleep(3)
        browser_click(browser, varname.club)
        self.userCount(browser, varname.user, count)
        self.buycard(browser)
        self.plan_payment(browser, self.club, name)

    def pro(self, browser, name, count=None) :
        time.sleep(3)
        browser_click(browser, varname.pro)
        self.userCount(browser, varname.user, count)
        self.buycard(browser)
        self.plan_payment(browser, self.pro, name)

    def single(self, browser, name, count=None) :
        time.sleep(3)
        browser_click(browser, varname.single)
        self.userCount(browser, varname.singleUser, count)
        self.single_click(browser, count)
        self.plan_payment(browser, self.single, name)

    def wehagot(self, browser, name, count=None) :
        time.sleep(3)
        self.userCount(browser, varname.tuser, count)
        self.plan_payment(browser, self.wehagot, name)
    
    def allinone(self, browser, pay, name) :
        if pay == 5 :
            browser_click(browser, 'plan_select_bx.club', CLASS_NAME)
        elif pay == 6 :
            browser_click(browser, 'plan_select_bx.pro.v2', CLASS_NAME)
        time.sleep(1)
        self.plan_payment(browser, self.dt, name)

    def plan(self, browser, pay, name, count=None) :
        if pay == 1 :
            self.club(browser, name, count)
        elif pay == 2 :
            self.pro(browser, name, count)
        elif pay == 3 :
            self.single(browser, name, count)
        elif pay == 4 :
            self.wehagot(browser, name, count)
        elif pay == 5 or pay == 6 :
            self.allinone(browser, pay, name)

class WehagoSetting :
    def addEmpolyee(self, browser) :
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(5)
        browser.get('https://www.wehago.com/#/company/management/')
        time.sleep(3)
        Company().cs_addEmpolyee(browser)

    def purchaseService(self, browser, wehago, pay) :
        if wehago == 1 :
            browser.get('http://dev.wehago.com/#/market')
        else : 
            browser.get('https://www.wehago.com/#/market')
        time.sleep(1)
        if pay == 1 or pay == 2 :
            Market().mk_purchaseService(browser)
            Market().mk_payment(browser)

class Personal :
    def pe_setMail(self, browser, id) :
        browser.get(getUrl('personal/detailpersoninfo'))
        time.sleep(5)
        browser_click(browser, varname.modifyPersonal)
        time.sleep(1)
        textClear(browser, varname.mailAddress)
        mail = id + '@wehago.com'
        browser_sendKey(browser, varname.mailAddress, mail)
        browser_click(browser, varname.savePersonal)
        browser_click(browser, varname.confirm)

class Approval :
    def ap_basicset(self, browser) :
        browser_click(browser, varname.createApproval)
        browser_click(browser, varname.setFrequentlyApproval)
        enter(browser, varname.serachFormname, '명함')
        browser_click(browser, varname.approvalForm)
        browser_click(browser, varname.saveApproval)
        text = '자주쓰는 결재를 등록하지 않은 경우'
        if sameText(browser, text) :
            browser_click(browser, varname.cancel)
            browser_click(browser, varname.cancelApproval)
        progress(browser)

    def ap_settingType(self, browser) :
        browser_click(browser, varname.approvalSetting)
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[1])
        while not hasxpath(browser, varname.approvalManagement) :
            time.sleep(1)
        browser_click(browser, varname.approvalManagement)
        time.sleep(1)
        if not browser.find_element(By.ID, 'chkbox_defer').is_selected() :
            browser_click(browser, varname.postApproval)
            browser_click(browser, varname.preApproval)
        browser_click(browser, varname.approvalSaveButton)
        time.sleep(1)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(1)

    def ap_unsavedInformation(self, browser) :
        text = '결재문서에 입력된 정보가 존재합니다.'
        if sameText(browser, text) :
            browser_click(browser, varname.confirm)

    def ap_addFile(self, browser) :
        browser.switch_to.frame(0)
        time.sleep(1)
        browser.find_element(By.XPATH, '//*[@id="dzeditor_0"]').click()
        browser_click(browser, 'TB_INSERT_IMAGE_0', ID)
        time.sleep(3)
        browser.switch_to.default_content()
        upload = browser.find_elements_by_css_selector('input[type="file"]')
        upload[1].send_keys(path+'/btn_webot.png')
        time.sleep(1)
        browser_click(browser,'duzon_dialog_btn_ok_normal',CLASS_NAME)
        progress(browser)

    def ap_createApproval(self, browser, type, archive=None) :
        self.ap_unsavedInformation(browser)
        browser_click(browser, varname.createApproval)
        progress(browser)
        if not hasxpath(browser, varname.createApprovalForm) :
            self.ap_basicset(browser)
        browser_click(browser, varname.createApprovalForm)
        progress(browser)
        time.sleep(1)
        approveTitle = currentTime().strftime('%m%d %H:%M')+'전자결재' + type
        if archive :
            self.ap_archive(browser)
            approveTitle = approveTitle + archive
        browser_sendKey(browser, varname.approvalName, approveTitle)
        self.ap_addFile(browser)
        self.ap_approver(browser, type)
        time.sleep(1)
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        progress(browser)
    
    def ap_approver(self, browser, type) :
        browser_click(browser, varname.approvalUser)
        progress(browser)
        if type == '일반' :
            enter(browser, '//*[@id="inputSearch-TK"]', usersName(browser))
            browser_click(browser, 'point_color', CLASS_NAME)
            browser_click(browser, varname.approvalAddUser)
            time.sleep(1)
            if '중복 지정' in context(browser, varname.ap_duplicatePopup) :
                browser_click(browser, varname.ap_duplicateConfirm)
        else :
            if type == '후결' :
                browser_click(browser, varname.postApprovalButton)
            elif type == '전결' :
                browser_click(browser, varname.preApprovalButton)
            time.sleep(1)
            if '프로세스 변경 시' in context(browser, varname.duplicatePopup) :
                browser_click(browser, varname.confirm)
                time.sleep(1)
            enter(browser, '//*[@id="inputSearch-TK"]', usersName(browser))
            browser_click(browser, 'point_color', CLASS_NAME)
            browser_click(browser, varname.approvalAddUser1)
            textClear(browser, '//*[@id="inputSearch-TK"]')
            inputUser(browser, '//*[@id="inputSearch-TK"]')
            browser_click(browser, 'point_color', CLASS_NAME)
            browser_click(browser, varname.approvalAddUser2)
        browser_click(browser, varname.registApprover)
        time.sleep(3)
        # if '후결 일 경우' in context(browser, varname.duplicatePopup) :
        #     browser_click(browser, varname.confirm)
        #     Common().close(browser)
        
    def ap_approval(self, browser) :
        self.ap_createApproval(browser, '일반')

    def ap_clickApproval(self, browser) :
        browser_click(browser, varname.approvalHome)
        progress(browser)
        browser_click(browser, varname.receiptApproval)
        progress(browser)
        browser_click(browser, varname.approveList)
        progress(browser)

    def ap_reApproval(self, browser) :
        self.ap_clickApproval(browser)
        btn_click(browser, 'LUX_basic_btn.Default.basic', '재기안')
        btn_click(browser, WSC_LUXButton, confirm)
        browser_sendKey(browser, varname.approvalName, '재기안 상신')
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        progress(browser)

    def ap_modifyApproval(self, browser) :
        self.ap_clickApproval(browser)
        browser_click(browser, varname.modifyApproval)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        browser_click(browser, varname.ap_findUser)
        enter(browser, '//*[@id="inputSearch-TK"]', usersName(browser))
        browser_click(browser, 'point_color', CLASS_NAME)
        browser_click(browser, varname.ap_userCheck)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, confirm)
        browser_sendKey(browser, varname.modifyReason, '수정')
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', confirm)
        progress(browser)

        # 수정이 된 경우 시행자 정상입력되어있음, 시행자 없는경우
        modify = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div[3]/div[3]/div/div[3]/div[3]/div[1]/table/tbody/tr[7]/td'
        if not browser.find_element(By.XPATH, modify).text :
            raise Exception('전자결재 수정 확인 필요')
        
    def ap_approve(self, browser) :
        self.ap_clickApproval(browser)
        browser_click(browser, varname.approve)
        browser_click(browser, varname.checkApproval)
        progress(browser)

        browser_click(browser, varname.approvalHome)
        progress(browser)
        browser_click(browser, 'tabbtn.color4', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, '//*[@id="document_listbox_history"]/ul[1]/li[2]')
        time.sleep(1)
        if not hasxpath(browser, 'status.color_green', CLASS_NAME) :
            raise Exception('전자결재 승인 확인 필요')

    def ap_reject(self, browser) :
        self.ap_clickApproval(browser)
        browser_click(browser, varname.reject)
        if hasxpath(browser, varname.rejectReason) :
            browser_sendKey(browser, varname.rejectReason, '반려입니다')
            browser_click(browser, varname.rejectButton)
        else :
            browser_click(browser, varname.checkApproval)
        progress(browser)

        # browser_click(browser, varname.approvalHome)
        # progress(browser)
        # browser_click(browser, 'tabbtn.color4', CLASS_NAME)
        # time.sleep(3)
        # browser_click(browser, '//*[@id="document_listbox_history"]/ul[1]/li[2]')
        # time.sleep(1)
        # if not hasxpath(browser, 'status.color_red', CLASS_NAME) :
        #     raise Exception('전자결재 반려 확인 필요')

    def ap_enforcement(self, browser) :
        browser_click(browser, varname.enforcement)
        progress(browser)
        if not hasxpath(browser, varname.enforcementList) :
            raise Exception('시행처리 확인필요')
        else :
            browser_click(browser, varname.enforcementList)
            progress(browser)
            browser_click(browser, varname.enforcementButton)
            browser.find_element(By.XPATH, varname.enforcementInfor).send_keys('시행완료')
            browser_click(browser, varname.enforcementCompleted)
        progress(browser)

        if not hasxpath(browser, 'label.enfo', CLASS_NAME) :
            raise Exception('시행처리 확인 필요')
    
    def ap_deleteApprove(self, browser) :
        time.sleep(3)
        self.clickApproalSetting(browser)
        enter(browser, varname.serachApproval, '전자결재')
        progress(browser)
        while True :
            Common().canvasClick(browser, '//*[@id="gridAdminCheckBox"]/div/canvas', 45, 170)
            if context(browser, varname.deleteApprove) == delete :
                browser_click(browser, varname.deleteApprove)
                browser_click(browser, varname.confirm)
            else :
                break
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(3)

    def ap_searchApproval(self, browser, text) :
        browser_click(browser, 'btn.btn_search', CLASS_NAME)
        enter(browser, varname.btn_searchApproval, text)
        progress(browser)
        if hasxpath(browser, '//*[@id="document_listbox_search"]/li[2]') :
            browser_click(browser, '//*[@id="document_listbox_search"]/li[2]')
            time.sleep(3)
        else :
            raise Exception(text+'문서 없음')

    def ap_postApproval(self, browser) :
        self.ap_createApproval(browser, '후결') 
        self.ap_approve(browser)

    def ap_preApproval(self, browser) :
        self.ap_createApproval(browser, '전결')
        self.ap_approve(browser)

    def ap_serviceApprove(self, browser) :
        enter(browser, varname.approver, usersName(browser))
        if '중복 지정' in context(browser, varname.ap_duplicatePopup) :
            browser_click(browser, varname.ap_duplicateConfirm)
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        progress(browser)
        # 근태관리 중복휴일 지정 불가 있는경우 
        try :
            time.sleep(1)
            if '중복신청건' in context(browser, varname.ap_duplicatePopup) :
                browser_click(browser, varname.ap_duplicateConfirm)
                browser.get(getUrl('eapprovals'))
                time.sleep(5)
                self.ap_searchApproval(browser, '휴가')
                browser_click(browser, varname.approve)
                browser_click(browser, varname.checkApproval)
                progress(browser)
                raise Exception('휴가신청 확인필요')
            elif '휴가신청서' in context(browser, varname.ap_duplicatePopup) :
                browser_click(browser, varname.ap_duplicateConfirm)
                raise Exception('휴가신청취소 확인필요')
            elif '휴가신청이 불가합니다.' in context(browser, varname.ap_duplicatePopup) :
                browser_click(browser, varname.ap_duplicateConfirm)
                print('오늘이 휴일인가요,')
                self.ap_attendanceHoliday(browser)
                browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
                progress(browser)
                self.ap_approve(browser)
            else :
                self.ap_approve(browser)
        finally:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            browser.refresh()
            time.sleep(5)

    def ap_attendanceHoliday(self, browser) :
        Common().close(browser)
        date = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div[3]/div[3]/div/div[3]/div[1]/div[1]/table/tbody/tr[6]/td/div/div/div/div[1]/div[2]/div/div[1]/div/button'
        browser_click(browser, date)
        time.sleep(1)
        browser_click(browser, 'btn.btn_next_mon', CLASS_NAME)
        time.sleep(3)
        day = (currentTime() + datetime.timedelta(days=3)).strftime('%#d')
        print(day)
        btn_click(browser, WSC_LUXButton, day)
        time.sleep(1)
        browser_click(browser, '/html/body/div[3]/div/div/div[4]/div/button[2]')
        time.sleep(1)

    def ap_expense(self, browser, card) :
        for i in range(0,60) :
            if hasxpath(browser, varname.cardTitle) : break
            else : time.sleep(1)
        browser_sendKey(browser, varname.cardTitle, card + '지출')
        self.ap_serviceApprove(browser)

    def ap_attendanceVacation(self, browser) :
        for i in range(0,60) :
            if hasxpath(browser, varname.approvalName) : break
            else : time.sleep(1)
        browser_sendKey(browser, varname.approvalName, currentTime().strftime('%m%d %H:%M')+'휴가신청')
        self.ap_serviceApprove(browser)
    
    def ap_attendanceVacationCancel(self, browser) :
        for i in range(0,60) :
            if hasxpath(browser, varname.approvalName) : break
            else : time.sleep(1)
        browser_sendKey(browser, varname.approvalName, currentTime().strftime('%m%d %H:%M')+'휴가취소신청')
        browser_click(browser, varname.referenceDocument)
        time.sleep(1)
        Common().canvasClick(browser, '//*[@id="참조문서 지정"]/div/canvas', 16, 75)
        time.sleep(1)
        browser_click(browser, varname.confirmReferenceButton)
        time.sleep(1)
        browser_sendKey(browser, varname.cancellationReason, '휴가취소')
        self.ap_serviceApprove(browser)

    def ap_pms(self, browser, name=None) :
        try:
            for i in range(0,60) :
                if hasxpath(browser, varname.approvalName) : break
                else : time.sleep(1)
            if name : browser_sendKey(browser, varname.approvalName, '집행정보')
            time.sleep(3)
            browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
            progress(browser)
            self.ap_approve(browser)
        finally:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

    def ap_createArchive(self, browser) :
        browser_click(browser, 'add_group', CLASS_NAME)
        time.sleep(1)
        action = ActionChains(browser)
        action.send_keys('보관함 하나~').send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(1)
        if context(browser, varname.archiveCount) == '0' :
            raise Exception('보관함 추가 확인 필요')

    def ap_deleteArchive(self, browser): 
        while hasxpath(browser, varname.archiveList) :
            browser_click(browser, varname.archiveList)
            time.sleep(1)
            browser_click(browser, varname.archiveOption)
            browser_click(browser, varname.archiveDelete)
            if '보관함을 삭제' in context(browser, varname.archivePopup) :
                browser_click(browser, varname.archiveConfirm)
            time.sleep(1)
        if context(browser, varname.archiveCount) != '0' :
            raise Exception('보관함 삭제 확인 필요')

    def ap_moveDocumentArchive(self, browser) :
        self.ap_clickApproval(browser)
        browser_click(browser, varname.archive)
        browser_click(browser, 'storegebtn', CLASS_NAME)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', CLASS_NAME)
        progress(browser)
        browser_click(browser, varname.archiveList)
        progress(browser)
        if not hasxpath(browser, varname.archiaveApprovalList) :
            raise Exception('상신된 문서 보관함 이동 확인 필요')
        self.ap_deleteDocumentArchive(browser)

    def ap_approveDocumentArchive(self, browser) :
        self.ap_createApproval(browser, '일반', '상신하면서 보관함 이동')
        self.ap_approve(browser)
        browser_click(browser, varname.archiveList)
        progress(browser)
        if not hasxpath(browser, varname.archiaveApprovalList) :
            raise Exception('결재 작성하면서 보관함 이동 확인 필요')
        self.ap_deleteDocumentArchive(browser)

    def ap_deleteDocumentArchive(self, browser) :
        browser_click(browser, varname.archiveList)
        progress(browser)
        browser_click(browser, '//*[@id="document_listbox_history"]/ul/li[2]/div[1]/label/span')
        browser_click(browser, varname.deleteDocumentArchive)
        browser_click(browser, varname.deleteArchiveConfim)
        time.sleep(3)
        if context(browser, varname.archiveDocumentCount) != '0' :
            raise Exception('보관함 문서 삭제 확인 필요')

    def ap_archive(self, browser) :
        browser_click(browser, varname.setArchive)
        time.sleep(1)
        browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div[3]/div[3]/div/div[4]/div[2]/div/div/div[1]/div[1]/div/div[2]/div/div/div/table/tbody/tr/td/div/div/div/div[1]/button')
        time.sleep(1)
        browser_click(browser, '//*[@id="scrollElement"]/div/ul/div[2]/li')
        browser_click(browser, varname.saveApproval)
        time.sleep(1)

    def clickApproalSetting(self, browser) :
        browser_click(browser, varname.approvalSetting)
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[1])
        while not hasxpath(browser, varname.documentForm) :
            time.sleep(1)

    def testaddDocForm(self, browser) :
        enter(browser, varname.searchCategory, '사용자생성')
        time.sleep(1)
        # 양식 추가
        browser_click(browser, varname.addDocument)
        browser_click(browser, 'LUX_basic_select', CLASS_NAME)
        time.sleep(1)
        for i in range(1,10) :
            category = '//*[@id="scrollElement"]/div/ul/div[' + str(i) + ']'
            if not hasxpath(browser, category) :
                break
            else :
                categoryText = browser.find_element(By.XPATH, category).text
                if categoryText == '사용자생성' :
                    browser_click(browser, category)

    def ap_addDocumentForm(self, browser) :
        self.clickApproalSetting(browser)
        browser_click(browser, varname.documentForm)
        # 카테고리 추가
        browser_click(browser, 'add_category', CLASS_NAME)
        browser_sendKey(browser, varname.categoryName, '사용자생성')
        browser_sendKey(browser, varname.categoryDescription, '카테고리설명명')
        browser_click(browser, varname.addCategoryBtn)
        time.sleep(1)

        # 양식 추가
        enter(browser, varname.searchCategory, '사용자생성')
        browser_click(browser, varname.addDocument)
        time.sleep(3)
        browser_click(browser, varname.toggle1)
        browser_click(browser, varname.toggle2)
        browser_click(browser, varname.toggle3)
        browser_sendKey(browser, varname.formName, '만든양식')
        browser_sendKey(browser, varname.formdescription, '만든 양식 설명')
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        time.sleep(3)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(3)

    def ap_deleteDocumentForm(self, browser) :
        self.clickApproalSetting(browser)
        browser_click(browser, varname.documentForm)
        time.sleep(1)
        # 양식 삭제
        enter(browser, varname.searchCategory, '사용자생성')
        self.ap_deleteform(browser)
        browser.refresh()
        time.sleep(3)
        # 카테고리 삭제
        self.ap_deleteCategory(browser)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        time.sleep(3)

    def ap_deleteform(self, browser) :
        # 양식 삭제
        while True :
            time.sleep(1)
            if hasxpath(browser, 'favorite_approval_item.type2', CLASS_NAME) :
                browser_click(browser, 'favorite_approval_item.type2', CLASS_NAME)
                time.sleep(1)
                btn_click(browser, 'LUX_basic_btn.Confirm.basic', delete)
                btn_click(browser, WSC_LUXButton, confirm)
                time.sleep(3)
            else :
                break

    def ap_deleteCategory(self, browser) :
        count = 1
        while True :
            setbtn = '//*[@id="CategoryList"]/li[' + str(count) + ']/button'
            if hasxpath(browser, setbtn) :
                browser_click(browser, setbtn)
                time.sleep(0.1)
                name = browser.find_element(By.XPATH, varname.categoryName).get_attribute('value')
                if name == '사용자생성' :
                    browser_click(browser, varname.deleteCategory)
                    time.sleep(0.1)
                    if sameText(browser, '등록된 양식') :
                        browser_click(browser, varname.confirm)
                        Common().close(browser)
                        category = re.sub('/button','',setbtn)
                        browser_click(browser, category)
                        self.ap_deleteform(browser)
                        count += 1
                    else :
                        browser_click(browser, varname.confirm)
                        time.sleep(0.5)
                else :
                    Common().close(browser)
                    count += 1
            else :
                break
        enter(browser, varname.searchCategory, '사용자생성')
        if context(browser, varname.confirm) != '확인' :
            raise Exception('전자결재 카테고리 삭제 확인')
        else : 
            browser_click(browser, varname.confirm)

    def ap_createApprovalbyUser(self, browser) :
        browser_click(browser, varname.createApproval)
        progress(browser)
        enter(browser, varname.searchApproval, '만든양식')
        browser_click(browser, 'favorite_approval_list', CLASS_NAME)
        progress(browser)
        time.sleep(1)
        browser_sendKey(browser, varname.approvalName, currentTime().strftime('%m%d %H:%M')+'전자결재 사용자생성')
        self.ap_addFile(browser)
        self.ap_approver(browser, '일반')
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        progress(browser)

    def ap_approvebyUser(self, browser) :
        self.ap_createApprovalbyUser(browser)
        self.ap_approve(browser)

    def ap_rejectbyUser(self, browser) :
        self.ap_createApprovalbyUser(browser)
        self.ap_reject(browser)

class Webuilder :
    def wb_webuilder(self, browser) :
        browser.get(getUrl('main'))
        time.sleep(5)
        
        Common().close(browser)
        close = '//*[@id="BODY_CLASS"]/div[4]/div[11]/div[1]/div[2]/div/div/div[1]/div/div/div[1]/button/span'
        close2 = '//*[@id="BODY_CLASS"]/div[4]/div[10]/div[1]/div[2]/div/div/div[1]/div/div/div[1]/button/span'
        close3 = '//*[@id="BODY_CLASS"]/div[4]/div[9]/div[1]/div[2]/div/div/div[1]/div/div/div[1]/button/span'
        if hasxpath(browser, close) :
            browser_click(browser, close)
        elif hasxpath(browser, close2) :
            browser_click(browser, close2)
        elif hasxpath(browser, close3) :
            browser_click(browser, close3)
        time.sleep(1)
        browser_click(browser, 'MAIN-SVC_webuilder', ID)
        time.sleep(3)
        browser.switch_to.window(browser.window_handles[1])
        if not browser.title == 'DOUZONE :: 더존 위빌더' :
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            raise Exception('WE빌더 확인 필요')
        else :
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

class Invoice :
    tax='전자세금계산서'; trading='거래명세서'; deposit='입금표'; receipt='영수증'
    taxation='과세'; taxSmall='영세'; taxFree='면세'; right='정방향'; reverse='역방향'
    businessNumber='0012312376'; publish='발행'
    # 전자세금계산서
    def tax_checkPublish(self, browser, invoice=None) :
        self.tax_hasPoint(browser)
        # 발행이 완료되었는지 확인 
        time.sleep(1)
        try :
            if invoice == self.receipt or invoice == self.deposit :
                if sameText(browser, '발행에 성공하였습니다.') :
                    browser_click(browser, varname.confirm)
                    time.sleep(0.5)
                else :
                    if '잔여포인트가 부족합니다.' in context(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div[1]/div/div/div/div[3]/div[2]/div[2]/div[3]/div/div[2]/div[2]/div/div/div[1]/div') :
                        print('포인트 충전 필요!')
                    else :
                        raise Exception('입금표 발행 확인필요')
            else :
                if hasxpath(browser, 'sp_lux.sp_dialog2', CLASS_NAME) :
                    Common().close(browser)
                    time.sleep(1)
                else :
                    raise Exception('전자세금계산서 발행 확인필요')
        finally :
            Common().close(browser)
            time.sleep(1)

    def tax_hasPoint(self, browser) :
        if sameText(browser, '포인트가 부족합니다.') :
            browser_click(browser, varname.confrim)
            Common().close(browser)
            raise Exception('포인트 부족')

    def inputBusiness(self, browser, direction) :
        business = browser.find_elements(By.CLASS_NAME, 'WSC_LUXSmartComplete')
        if direction == self.reverse : business[0].click()
        else : business[1].click()
        action = ActionChains(browser)
        action.send_keys(self.businessNumber).pause(5).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(1)

    def formText(self, browser, invoice, direction) :
        self.inputBusiness(browser, direction)
        if invoice == self.deposit or invoice == self.receipt :
            if invoice == self.deposit :
                browser_sendKey(browser, varname.re_price, '10000')
                time.sleep(1)
                browser_click(browser, 'in_content', CLASS_NAME)
                time.sleep(3)
            else :
                browser_sendKey(browser, varname.re_taxRemarks, '비고입니다')
                action = ActionChains(browser)
                action.pause(1).send_keys(Keys.TAB*2).pause(1).send_keys(' 품목테스트').pause(1).send_keys(Keys.TAB).send_keys('10').send_keys(Keys.TAB).send_keys('10000').send_keys(Keys.TAB).perform()
                action.reset_actions()
                time.sleep(1)   
        else: 
            remarks = browser.find_elements(By.CLASS_NAME, 'WSC_LUXTextField')
            remarks[-2].click()
            time.sleep(1)
            action = ActionChains(browser)
            action.send_keys('비고입니다').send_keys(Keys.TAB*4).pause(1).send_keys(' 품목테스트').pause(1).send_keys(Keys.TAB).pause(1).send_keys('ea').pause(1).send_keys(Keys.TAB).pause(1).send_keys('10').pause(1).send_keys(Keys.TAB).pause(1).send_keys('1000').pause(1).send_keys(Keys.ENTER).perform()
            action.reset_actions()
            time.sleep(1)

    def tax_form(self, browser, invoice, taxType, direction) :
        Common().close(browser)
        # 목록 클릭
        if invoice == self.tax : browser_click(browser, varname.invoiceIssuance)
        elif invoice == self.trading : browser_click(browser, varname.tradingIssued)
        else : raise Exception('양식발행 입력 확인 필요')
        time.sleep(3)
        Common().close(browser)
        # 과세유형 클릭
        if taxType == self.taxation or taxType == self.taxSmall or taxType == self.taxFree :
            btn_click(browser, 'WSC_LUXRadioButton', taxType)
        else : 
            raise Exception('과세 유형 입력 확인 필요')
        time.sleep(1)
        if direction == self.reverse :
            btn_click(browser, 'WSC_LUXCheckBox', self.reverse)
            time.sleep(1)
        self.formText(browser, invoice, direction)

    def tax_formPublishBtn(self, browser, invoice=None) :
        Common().close(browser)
        pageDown(browser, 'tax_table_box', CLASS_NAME)
        if checkText(browser, WSC_LUXButton, self.publish) : btn_click(browser, WSC_LUXButton, self.publish)
        elif checkText(browser, WSC_LUXButton, '발행요청') : btn_click(browser, WSC_LUXButton, '발행요청')
        time.sleep(3)
        if sameText(browser, '서비스코드가 없습니다.') or sameText(browser, '필수 입력사항을'):
            browser_click(browser, varname.confirm)
            raise Exception('전자세금계산서 발행 확인필요')
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(5)
        self.tax_checkPublish(browser, invoice)

    def tax_saveBtn(self, browser) :
        Common().close(browser)
        btn_click(browser, WSC_LUXButton, save)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        Common().close(browser)
        time.sleep(1)

    def tax_saveList(self, browser, direction) :
        browser_click(browser, varname.invoiceLookup)
        time.sleep(3)
        if direction == self.reverse :
            browser_click(browser, varname.taxPurchase)
            time.sleep(1)
        btn_click(browser, WSC_LUXButton, '상세검색')
        browser_click(browser, varname.issuanceStatus)
        time.sleep(1)
        browser_click(browser, varname.statusSave)
        browser_click(browser, varname.taxDetailSearchBtn)
        time.sleep(5)

    def tax_listPublishDetail(self, browser) :
        Common().canvasClick(browser, '//*[@id="gridMain"]/div/canvas', 60, 45)
        time.sleep(1)
        if checkText(browser, WSC_LUXButton, self.publish) :
            btn_click(browser, WSC_LUXButton, self.publish)
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(5)
            if sameText(browser, '발행이 완료되었습니다.') :
                btn_click(browser, WSC_LUXButton, confirm)
            else :
                raise Exception('전자세금계산서 발행 확인필요')
        else :
            raise Exception('저장 상태 확인 필요')
 
    def tax_listPublishBtn(self, browser, direction) :
        Common().close(browser)
        self.tax_saveList(browser, direction)
        self.tax_listPublishDetail(browser)

    def tax_detailPublishBtn(self, browser, invoice, direction) :
        Common().close(browser)
        if invoice == self.tax : self.tax_saveList(browser, direction)
        elif invoice == self.trading : self.tr_saveList(browser, direction)
        elif invoice == self.receipt or invoice == self.deposit: self.re_saveBtn(browser, invoice)
        Common().canvasClick(browser, '//*[@id="gridMain"]/div/canvas', 100, 45)
        time.sleep(3)
        Common().close(browser)
        if hasxpath(browser, 'tax_table_box', CLASS_NAME) :
            self.tax_formPublishBtn(browser, invoice)
        else :
            raise Exception('저장 상태 확인 필요')

    def simpleText(self, browser, invoice) :
        if sameText(browser, '서비스코드가 없습니다.'):
            browser_click(browser, varname.confirm)
            raise Exception('전자세금계산서 발행 확인필요')
        enter(browser, 'in_input_ph', self.businessNumber, CLASS_NAME, 3)
        if invoice == self.tax :
            browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[2]/div[3]/div/div[4]/div[4]/div[3]')
        elif invoice == self.trading :
            browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[4]/div[3]')
        elif invoice == self.receipt :
            browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]')
        time.sleep(1)
        action = ActionChains(browser)
        action.pause(1).send_keys(Keys.TAB*2).pause(0.5).send_keys(' 품목테스트').pause(1).send_keys(Keys.TAB).pause(1).send_keys('ea').pause(1).send_keys(Keys.TAB).pause(1).send_keys('10').pause(1).send_keys(Keys.TAB).pause(1).send_keys('1000').pause(1).send_keys(Keys.ENTER).pause(1).perform()
        action.reset_actions()
        time.sleep(1)

    def tax_simple(self, browser, invoice, taxType, direction) :
        Common().close(browser)
        if invoice == self.tax : 
            browser_click(browser, varname.invoiceIssuance)
            reverseBtn = varname.s_taxReverse
        elif invoice == self.trading : 
            browser_click(browser, varname.tradingIssued)
            reverseBtn = varname.ts_taxReverse
        time.sleep(3)
        Common().close(browser)
        time.sleep(1)
        # 간편발행 선택
        browser_click(browser, 'sp_in.showdetail', CLASS_NAME)
        time.sleep(3)
        Common().close(browser)
        if taxType == self.taxation or taxType == self.taxSmall or taxType == self.taxFree :
            btn_click(browser, 'WSC_LUXRadioButton', taxType)
        else : 
            raise Exception('과세 유형 확인 필요')

        self.simpleText(browser, invoice)
        if direction == self.reverse :
            browser_click(browser, reverseBtn)
            time.sleep(1)

    def tax_simplePublishBtn(self, browser, invoice=None) :
        pageDown(browser, 'in_content.simple_issue', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, self.publish)
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, '발행하기')
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(5)
        self.tax_checkPublish(browser, invoice)

    def tax_successfulClick(self, browser) :
        browser_click(browser, varname.invoiceLookup)
        time.sleep(3)
        enter(browser, varname.searchInvoice, '테스트_QA테스트전자')
        time.sleep(1)
        invoice = browser.find_element(By.XPATH, '//*[@id="gridMain"]/div/canvas')
        width = invoice.size['width']*0.9
        action = ActionChains(browser)
        action.move_to_element_with_offset(invoice,width,15).double_click().pause(1).move_by_offset(0,30).click().perform()
        action.reset_actions()
        progress(browser)
        if hasxpath(browser, varname.invoiceStatus) :
            if context(browser, varname.invoiceStatus) != '전송성공' :
                raise Exception('전송처리 필요')
        else :
            action = ActionChains(browser)
            action.move_to_element_with_offset(invoice,width,45).click().perform()
            progress(browser)
        time.sleep(1)
        pageDown(browser, 'tax_table_box', CLASS_NAME)

    def tax_modify(self, browser) :
        Common().close(browser)
        btn_click(browser, WSC_LUXButton, '다음')
        time.sleep(3)
        if sameText(browser, '수정세금계산서를 발행하시겠습니까') :
            browser_click(browser, varname.confirm)
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, '수정발행')
        progress(browser)
        btn_click(browser, WSC_LUXButton, '다음')
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)
        self.tax_formPublishBtn(browser)

    # 거래명세서
    def tr_saveList(self, browser, direction) :
        browser_click(browser, varname.tradingLookup)
        progress(browser)
        if direction == self.reverse :
            browser_click(browser, varname.trPurhase)
            time.sleep(1)
        browser_click(browser, varname.tradingSave)

    def tr_listPublishBtn(self, browser, direction) :
        self.tr_saveList(browser, direction)
        Common().canvasClick(browser, '//*[@id="gridMain"]/div/canvas', 60, 45)
        time.sleep(1)
        if hasxpath(browser, varname.listPublishBtn) :
            browser_click(browser, varname.listPublishBtn)
            time.sleep(1)
            if sameText(browser, '발행할 수 있는 상태의 데이터가 없습니다.') :
                browser_click(browser, varname.confirm)
                self.tax_deleteSaved(browser)
            else :
                browser_click(browser, varname.t_listPublishConfirm)
                progress(browser)
                self.tax_hasPoint(browser)
                if sameText(browser, '거래명세서 발행이 완료되었습니다.') :
                    browser_click(browser, varname.confirm)
                else :
                    raise Exception('전자세금계산서 발행 확인필요')
        else :
            raise Exception('저장 상태 확인 필요')

    def tr_attachmentPublishBtn(self, browser) :
        btn_click(browser, WSC_LUXButton, '첨부발행')
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        progress(browser)
        if sameText(browser, '첨부발행에 성공하였습니다.') :
            btn_click(browser, WSC_LUXButton, confirm)
            time.sleep(0.5)
            self.tax_formPublishBtn(browser)
        else :
            raise Exception('거래명세서 첨부발행 확인 필요')

    def tr_attachmentListPublishBtn(self, browser, direction) :
        self.tr_saveList(browser, direction)
        Common().canvasClick(browser, '//*[@id="gridMain"]/div/canvas', 60, 45)
        time.sleep(1)
        # 리스트에서 첨부발행
        if checkText(browser, WSC_LUXButton, self.publish) :
            btn_click(browser, WSC_LUXButton, '세금계산서 첨부발행')
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, '세금계산서 발행')
            time.sleep(1)
            try :
                if not hasxpath(browser, 'dialog_content.md', CLASS_NAME) :
                    raise Exception('리스트 첨부발행 확인 필요')
            finally : Common().close(browser)
        else :
            raise Exception('저장상태 확인 필요')

    def tr_attachmentDetailPublishBtn(self, browser, direction) :
        self.tr_saveList(browser, direction)
        Common().canvasClick(browser, '//*[@id="gridMain"]/div/canvas', 100, 45)
        time.sleep(3)
        # 발행 상태가 저장이 맞는지 확인 
        status = browser.find_element(By.CLASS_NAME, 'WSC_LUXLabel').text
        if status == save :
            # 첨부발행 클릭
            self.tr_attachmentPublishBtn(browser)
        else :
            self.tax_deleteSaved(browser)
            self.tax_deleteInvoice(browser)
            self.tr_deleteTrading(browser)
            raise Exception('거래명세서 상세발행 시 상태 이슈,, ')

    # 입금표/영수증
    def dr_formPublishBtn(self, browser, invoice) :
        if invoice == self.receipt : browser_click(browser, varname.receipt)
        elif invoice == self.deposit : browser_click(browser, varname.deposit)
        time.sleep(3)
        self.formText(browser, invoice, self.right)
        self.tax_formPublishBtn(browser, invoice)

    def dr_listPublishBtn(self, browser, invoice) :
        if invoice == self.receipt : browser_click(browser, varname.receipt)
        elif invoice == self.deposit : browser_click(browser, varname.deposit)
        time.sleep(3)
        self.formText(browser, invoice, self.right)
        self.re_saveBtn(browser, invoice)
        self.tax_listPublishDetail(browser)

    def dr_detailPublishBtn(self, browser, invoice) :
        if invoice == self.receipt : browser_click(browser, varname.receipt)
        elif invoice == self.deposit : browser_click(browser, varname.deposit)
        time.sleep(3)
        self.formText(browser, invoice, self.right)
        self.tax_detailPublishBtn(browser, invoice, self.right)

    def re_saveBtn(self, browser, invoice) :
        self.tax_saveBtn(browser)
        # 조회
        if invoice == self.deposit :
            browser_click(browser, varname.depositLookup)
        elif invoice == self.receipt :
            browser_click(browser, varname.receiptLookup)
        time.sleep(3)
        browser_click(browser, varname.re_save)
    
    def dr_simplePublishBtn(self, browser, invoice) :
        browser_click(browser, 'sp_in.showdetail', CLASS_NAME)
        progress(browser)
        enter(browser, 'in_input_ph', '테스트_QA테스트', CLASS_NAME, 3)

        if invoice == self.deposit :
            value = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]/div/table/tbody/tr/td[1]/div/div/input'
            browser_sendKey(browser, value, '100000')
            time.sleep(1)
        elif invoice == self.receipt :
            browser_click(browser, '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[3]/div[2]')
            time.sleep(1)
            action = ActionChains(browser)
            action.pause(1).send_keys(' 품목테스트').pause(1).send_keys(Keys.TAB).pause(1).send_keys('10').pause(1).send_keys(Keys.TAB).pause(1).send_keys('1000').pause(1).send_keys(Keys.ENTER).pause(1).perform()
            action.reset_actions()
            time.sleep(1)
        self.tax_simplePublishBtn(browser, invoice)

    def tax_deleteBtn(self, browser, text) :
        Common().canvasClick(browser, '//*[@id="gridMain"]/div/canvas', 60, 15)
        time.sleep(3)
        if checkText(browser, WSC_LUXButton, text) :
            btn_click(browser, WSC_LUXButton, text)
            time.sleep(3)
            btn_click(browser, WSC_LUXButton, confirm)
            progress(browser)
            Common().close(browser)
        else : print(text+'없음??????')
        time.sleep(1)
        

    # 삭제 1) 당일 발행분 지우기 2) 저장건 지우기
    def tax_todayDelete(self, browser, invoice) :
        if invoice == self.tax : browser_click(browser, varname.invoiceLookup)
        elif invoice == self.trading : browser_click(browser, varname.tradingLookup)
        elif invoice == self.receipt : browser_click(browser, varname.receiptLookup)
        elif invoice == self.deposit : browser_click(browser, varname.depositLookup)
        else : raise Exception('삭제 할 타입 입력 확인 필요')
        time.sleep(5)
        # 전체선택 후 취소 ,삭제
        self.tax_deleteBtn(browser, '취소')
        self.tax_deleteBtn(browser, '삭제')
        time.sleep(3)

    def tax_savedDelete(self, browser, invoice) :
        if invoice == self.tax : browser_click(browser, varname.invoiceLookup)
        elif invoice == self.trading : browser_click(browser, varname.tradingLookup)
        elif invoice == self.receipt : browser_click(browser, varname.receiptLookup)
        elif invoice == self.deposit : browser_click(browser, varname.depositLookup)
        else : raise Exception('삭제 할 타입 입력 확인 필요')
        time.sleep(3)
        if invoice == self.tax :
            btn_click(browser, WSC_LUXButton, '상세검색')
            browser_click(browser, varname.issuanceStatus)
            time.sleep(1)
            browser_click(browser, varname.statusSave)
            browser_click(browser, varname.taxDetailSearchBtn)
            time.sleep(5)
        else :
            browser_click(browser, 'btn_filter.nosend', CLASS_NAME)
            time.sleep(1)
            self.tax_deleteBtn(browser, '삭제')

    def eb_formText(self, browser) :
        browser_click(browser, varname.ebill)
        time.sleep(3)
        browser_click(browser, '//*[@id="BUY_NO_BIZ"]')
        action = ActionChains(browser)
        action.send_keys('테스트_QA테스트전자').pause(3).send_keys(Keys.ENTER).send_keys('박대표').send_keys(Keys.TAB*3).send_keys('smile_1896@naver.com').pause(1)
        action.send_keys(Keys.TAB*8).pause(1).send_keys('품목테스트').send_keys(Keys.TAB).send_keys('10').send_keys(Keys.TAB).send_keys('12000').send_keys(Keys.TAB).pause(1).perform()
        action.reset_actions()
        browser_click(browser,'//*[@id="BODY_CLASS"]/div[3]/div/div/div/div/div/div/div[3]/div[2]/div[2]')
        time.sleep(1)

    def eb_formPublish(self, browser) :
        self.eb_formText(browser)
        browser_click(browser, varname.eb_publishBtn)
        time.sleep(3)
        if sameText(browser, '전자청구서 발행 완료했습니다.') :
            browser_click(browser, varname.confirm)
        else :
            raise Exception('전자 청구서 발행 확인 필요')

    def eb_saved(self, browser) :
        browser_click(browser, varname.ebillLookup)
        time.sleep(3)
        check = browser.find_elements(By.CLASS_NAME, 'WSC_LUXCheckBox')
        for i in range(1,5) :
            check[i].click()
            time.sleep(0.1)
        time.sleep(1)

    def eb_detailPublish(self, browser) :
        browser.refresh()
        time.sleep(5)
        self.eb_formText(browser)
        browser_click(browser, varname.eb_saveBtn)
        browser_click(browser, varname.confirm)
        time.sleep(1)
        if sameText(browser, '전자청구서 저장 완료했습니다.') :
            browser_click(browser, varname.confirm)
            time.sleep(1)
            self.eb_saved(browser)
            Common().canvasClick(browser, '//*[@id="gridMain"]/div/canvas', 100, 45)
            time.sleep(1)
            browser_click(browser, varname.eb_detailPublishBtn)
            time.sleep(1)
            if sameText(browser, '전자청구서 발행 완료하였습니다.') :
                browser_click(browser, varname.confirm)
            else :
                raise Exception('전자 청구서 상세 발행 확인 필요')
        else : 
            raise Exception('전자 청구서 저장 확인 필요')

    def eb_simpleText(self, browser) :
        browser_click(browser, varname.ebill)
        time.sleep(3)
        browser_click(browser, 'sp_in.showlist', CLASS_NAME)
        browser_click(browser, varname.eb_confirm)
        time.sleep(1)
        enter(browser, '//*[@id="SELL_NO_BIZ"]', '테스트_QA테스트전자', sec=3)
        time.sleep(1)
        enter(browser, '//*[@id="BUY_DAM_NM"]', '박대표')
        browser_click(browser, 'LUX_basic_tbl.taxissue_info2', CLASS_NAME)
        action = ActionChains(browser)
        action.send_keys(Keys.TAB*2).send_keys('품목테스트').send_keys(Keys.TAB).send_keys('10').send_keys(Keys.TAB).send_keys('1500').send_keys(Keys.TAB).perform()
        action.reset_actions()
        time.sleep(1)

    def eb_simplePublishBtn(self, browser) :
        browser_click(browser, varname.eb_publishBtn)
        time.sleep(1)
        browser_click(browser, varname.eb_publishBtn2)
        time.sleep(3)

        if sameText(browser, '전자청구서 발행 완료했습니다.') :
            browser_click(browser, varname.confirm)
        else :
            raise Exception('전자 청구서 간편 발행 확인 필요')

    def eb_simpleSaveBtn(self, browser) :
        browser_click(browser, varname.eb_saveBtn)
        browser_click(browser, varname.confirm)
        time.sleep(1)
        if sameText(browser, '전자청구서 저장 완료했습니다.') :
            browser_click(browser, varname.confirm)
            time.sleep(1)
        else : 
            raise Exception('전자 청구서 저장 확인 필요')

    def eb_simplePublish(self, browser) :
        self.eb_simpleText(browser)
        self.eb_simplePublishBtn(browser)

    def eb_deleteEbill(self, browser) :
        for i in range(0,3) :
            # 첫번째 저장 상태 삭제
            # 두번째 나머지 선택하고 취소 처리
            # 세번째 삭제
            if i != 2 :
                self.eb_saved(browser)
            Common().canvasClick(browser, '//*[@id="gridMain"]/div/canvas', 60, 15)
            time.sleep(1)
            if hasxpath(browser, varname.taxDelete) :
                browser_click(browser, varname.taxDelete)
                browser_click(browser, varname.confirm)
                time.sleep(1)
                browser_click(browser, varname.confirm)

class InvoicePublish(Invoice) :
    def tax_formPublish(self, browser, invoice, taxType, direction) :
        self.tax_form(browser, invoice, taxType, direction)
        self.tax_formPublishBtn(browser, invoice)

    def tax_formListPublish(self, browser, invoice, taxType, direction) :
        self.tax_form(browser, invoice, taxType, direction)
        self.tax_saveBtn(browser)
        if invoice == self.tax : self.tax_listPublishBtn(browser, direction)
        elif invoice == self.trading : self.tr_listPublishBtn(browser, direction)

    def tax_formDetailPublish(self, browser, invoice, taxType, direction) :
        self.tax_form(browser, invoice, taxType, direction)
        self.tax_saveBtn(browser)
        self.tax_detailPublishBtn(browser, invoice, direction)

    def tax_simplePublish(self, browser, invoice, taxType, direction) :
        self.tax_simple(browser, invoice, taxType, direction)
        self.tax_simplePublishBtn(browser)

    def tax_simpleListPublish(self, browser, invoice, taxType, direction) :
        self.tax_simple(browser, invoice, taxType, direction)
        self.tax_saveBtn(browser)
        self.tax_listPublishBtn(browser, direction)

    def tax_simpleDetailPublish(self, browser, invoice, taxType, direction) :
        self.tax_simple(browser, invoice, taxType, direction)
        self.tax_saveBtn(browser)
        self.tax_detailPublishBtn(browser, invoice, direction)

    def tax_modifyInvoice_detail(self, browser) :
        self.tax_successfulClick(browser)
        btn_click(browser, WSC_LUXButton, '수정발행')
        browser_click(browser, varname.confirm)
        progress(browser)
        self.tax_modify(browser)

    def tax_modifyInvoice_list(self, browser) :
        browser_click(browser, varname.invoiceModifyTab)
        time.sleep(3)
        enter(browser, varname.modifySearchAccount, '테스트_QA테스트전자')
        progress(browser)
        self.tax_modify(browser)

    def tax_modifyInvoice_approval(self, browser) :
        self.tax_successfulClick(browser)
        number = context(browser, '//*[@id="in_container"]/div[3]/div/div[4]/div[5]/div[1]/div[2]/dl/dd[3]')
        browser_click(browser, varname.invoiceModifyTab)
        time.sleep(3)
        btn_click(browser, 'WSC_LUXRadioButton', '승인번호조회')
        enter(browser, varname.approvalNumInput, number)
        self.tax_modify(browser)

    def re_formPublish(self, browser) :
        self.dr_formPublishBtn(browser, self.receipt)
        time.sleep(3)
        
    def re_listPublish(self, browser) :
        self.dr_listPublishBtn(browser, self.receipt)
        time.sleep(3)

    def re_detailPublish(self, browser) :
        self.dr_detailPublishBtn(browser, self.receipt)
        time.sleep(3)

    def re_simplePublish(self, browser) :
        browser_click(browser, varname.receipt)
        time.sleep(3)
        self.dr_simplePublishBtn(browser, self.receipt)

    def de_formPublish(self, browser) :
        self.dr_formPublishBtn(browser, self.deposit)
        time.sleep(3)
    
    def de_listPublish(self, browser) :
        self.dr_listPublishBtn(browser, self.deposit)
        time.sleep(3)

    def de_detailPublish(self, browser) :
        self.dr_detailPublishBtn(browser, self.deposit)
        time.sleep(3)

    def de_simplePublish(self, browser) :
        browser_click(browser, varname.deposit)
        time.sleep(3)
        self.dr_simplePublishBtn(browser, self.deposit)

    # 거래명세서 첨부발행
    def tr_attachmentPublish(self, browser, invoice, taxType, direction) :
        self.tax_form(browser, invoice, taxType, direction)
        self.tr_attachmentPublishBtn(browser)

    # 거래명세서 리스트에서 첨부발행 
    def tr_attachmentListPublish(self, browser, invoice, taxType, direction) :
        self.tax_form(browser, invoice, taxType, direction)
        self.tax_saveBtn(browser)
        self.tr_attachmentListPublishBtn(browser, direction)

    # 거래명세서 상세에서 첨부발행
    def tr_attachmentDetailPublish(self, browser, invoice, taxType, direction) :
        self.tax_form(browser, invoice, taxType, direction)
        self.tax_saveBtn(browser)
        self.tr_attachmentDetailPublishBtn(browser, direction)
    
    # 양식발행
    def tax_formTaxation(self, browser) :
        self.tax_formPublish(browser, self.tax, self.taxation, self.right)
        time.sleep(3)
    
    def tax_formTaxationReverse(self, browser) :
        self.tax_formPublish(browser, self.tax, self.taxation, self.reverse)
        time.sleep(3)

    def tax_formTaxSmall(self, browser) :
        self.tax_formPublish(browser, self.tax, self.taxSmall, self.right)
        time.sleep(3)
    
    def tax_formTaxSmallReverse(self, browser) :
        self.tax_formPublish(browser, self.tax, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tax_formTaxFree(self, browser) :
        self.tax_formPublish(browser, self.tax, self.taxFree, self.right)
        time.sleep(3)
    
    def tax_formTaxFreeReverse(self, browser) :
        self.tax_formPublish(browser, self.tax, self.taxFree, self.reverse)
        time.sleep(3)

    # 양식 저장 > 리스트 발행
    def tax_formListTaxation(self, browser) :
        self.tax_formListPublish(browser, self.tax, self.taxation, self.right)
        time.sleep(3)
    
    def tax_formListTaxationReverse(self, browser) :
        self.tax_formListPublish(browser, self.tax, self.taxation, self.reverse)
        time.sleep(3)

    def tax_formListTaxSmall(self, browser) :
        self.tax_formListPublish(browser, self.tax, self.taxSmall, self.right)
        time.sleep(3)
    
    def tax_formListTaxSmallReverse(self, browser) :
        self.tax_formListPublish(browser, self.tax, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tax_formListTaxFree(self, browser) :
        self.tax_formListPublish(browser, self.tax, self.taxFree, self.right)
        time.sleep(3)
    
    def tax_formListTaxFreeReverse(self, browser) :
        self.tax_formListPublish(browser, self.tax, self.taxFree, self.reverse)
        time.sleep(3)

    # 양식 저장 > 상세 발행
    def tax_formDetailTaxation(self, browser) :
        self.tax_formDetailPublish(browser, self.tax, self.taxation, self.right)
        time.sleep(3)
    
    def tax_formDetailTaxationReverse(self, browser) :
        self.tax_formDetailPublish(browser, self.tax, self.taxation, self.reverse)
        time.sleep(3)

    def tax_formDetailTaxSmall(self, browser) :
        self.tax_formDetailPublish(browser, self.tax, self.taxSmall, self.right)
        time.sleep(3)
    
    def tax_formDetailTaxSmallReverse(self, browser) :
        self.tax_formDetailPublish(browser, self.tax, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tax_formDetailTaxFree(self, browser) :
        self.tax_formDetailPublish(browser, self.tax, self.taxFree, self.right)
        time.sleep(3)
    
    def tax_formDetailTaxFreeReverse(self, browser) :
        self.tax_formDetailPublish(browser, self.tax, self.taxFree, self.reverse)
        time.sleep(3)

    # 간편 발행
    def tax_simpleTaxation(self, browser) :
        self.tax_simplePublish(browser, self.tax, self.taxation, self.right)
        time.sleep(3)
    
    def tax_simpleTaxationReverse(self, browser) :
        self.tax_simplePublish(browser, self.tax, self.taxation, self.reverse)
        time.sleep(3)

    def tax_simpleTaxSmall(self, browser) :
        self.tax_simplePublish(browser, self.tax, self.taxSmall, self.right)
        time.sleep(3)

    def tax_simpleTaxSmallReverse(self, browser) :
        self.tax_simplePublish(browser, self.tax, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tax_simpleTaxFree(self, browser) :
        self.tax_simplePublish(browser, self.tax, self.taxFree, self.right)
        time.sleep(3)
    
    def tax_simpleTaxFreeReverse(self, browser) :
        self.tax_simplePublish(browser, self.tax, self.taxFree, self.reverse)
        time.sleep(3)

    # 간편 저장 > 리스트 발행
    def tax_simpleListTaxation(self, browser) :
        self.tax_simpleListPublish(browser, self.tax, self.taxation, self.right)
        time.sleep(3)
    
    def tax_simpleListTaxationReverse(self, browser) :
        self.tax_simpleListPublish(browser, self.tax, self.taxation, self.reverse)
        time.sleep(3)

    def tax_simpleListTaxSmall(self, browser) :
        self.tax_simpleListPublish(browser, self.tax, self.taxSmall, self.right)
        time.sleep(3)

    def tax_simpleListTaxSmallReverse(self, browser) :
        self.tax_simpleListPublish(browser, self.tax, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tax_simpleListTaxFree(self, browser) :
        self.tax_simpleListPublish(browser, self.tax, self.taxFree, self.right)
        time.sleep(3)
    
    def tax_simpleListTaxFreeReverse(self, browser) :
        self.tax_simpleListPublish(browser, self.tax, self.taxFree, self.reverse)
        time.sleep(3)

    # 간편 저장 > 상세 발행
    def tax_simpleDetailTaxation(self, browser) :
        self.tax_simpleDetailPublish(browser, self.tax, self.taxation, self.right)
        time.sleep(3)
    
    def tax_simpleDetailTaxationReverse(self, browser) :
        self.tax_simpleDetailPublish(browser, self.tax, self.taxation, self.reverse)
        time.sleep(3)

    def tax_simpleDetailTaxSmall(self, browser) :
        self.tax_simpleDetailPublish(browser, self.tax, self.taxSmall, self.right)
        time.sleep(3)

    def tax_simpleDetailTaxSmallReverse(self, browser) :
        self.tax_simpleDetailPublish(browser, self.tax, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tax_simpleDetailTaxFree(self, browser) :
        self.tax_simpleDetailPublish(browser, self.tax, self.taxFree, self.right)
        time.sleep(3)
    
    def tax_simpleDetailTaxFreeReverse(self, browser) :
        self.tax_simpleDetailPublish(browser, self.tax, self.taxFree, self.reverse)
        time.sleep(3)
    
    # 거래명세서 양식발행
    def tr_formTaxation(self, browser) :
        self.tax_formPublish(browser, self.trading, self.taxation, self.right)
        time.sleep(3)

    def tr_formTaxationReverse(self, browser) :
        self.tax_formPublish(browser, self.trading, self.taxation, self.reverse)
        time.sleep(3)

    def tr_formTaxSmall(self, browser) :
        self.tax_formPublish(browser, self.trading, self.taxSmall, self.right)
        time.sleep(3)
    
    def tr_formTaxSmallReverse(self, browser) :
        self.tax_formPublish(browser, self.trading, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tr_formTaxFree(self, browser) :
        self.tax_formPublish(browser, self.trading, self.taxFree, self.right)
        time.sleep(3)
    
    def tr_formTaxFreeReverse(self, browser) :
        self.tax_formPublish(browser, self.trading, self.taxFree, self.reverse)
        time.sleep(3)

    # 거래명세서 양식 저장 > 리스트 발행
    def tr_formListTaxation(self, browser) :
        self.tax_formListPublish(browser, self.trading, self.taxation, self.right)
        time.sleep(3)
    
    def tr_formListTaxationReverse(self, browser) :
        self.tax_formListPublish(browser, self.trading, self.taxation, self.reverse)
        time.sleep(3)

    def tr_formListTaxSmall(self, browser) :
        self.tax_formListPublish(browser, self.trading, self.taxSmall, self.right)
        time.sleep(3)
    
    def tr_formListTaxSmallReverse(self, browser) :
        self.tax_formListPublish(browser, self.trading, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tr_formListTaxFree(self, browser) :
        self.tax_formListPublish(browser, self.trading, self.taxFree, self.right)
        time.sleep(3)
    
    def tr_formListTaxFreeReverse(self, browser) :
        self.tax_formListPublish(browser, self.trading, self.taxFree, self.reverse)
        time.sleep(3)

    # 거래명세서 양식 저장 > 상세 발행
    def tr_formDetailTaxation(self, browser) :
        self.tax_formDetailPublish(browser, self.trading, self.taxation, self.right)
        time.sleep(3)
    
    def tr_formDetailTaxationReverse(self, browser) :
        self.tax_formDetailPublish(browser, self.trading, self.taxation, self.reverse)
        time.sleep(3)

    def tr_formDetailTaxSmall(self, browser) :
        self.tax_formDetailPublish(browser, self.trading, self.taxSmall, self.right)
        time.sleep(3)
    
    def tr_formDetailTaxSmallReverse(self, browser) :
        self.tax_formDetailPublish(browser, self.trading, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tr_formDetailTaxFree(self, browser) :
        self.tax_formDetailPublish(browser, self.trading, self.taxFree, self.right)
        time.sleep(3)
    
    def tr_formDetailTaxFreeReverse(self, browser) :
        self.tax_formDetailPublish(browser, self.trading, self.taxFree, self.reverse)
        time.sleep(3)

    # 거래명세서 첨부 발행
    def tr_attachmentTaxation(self, browser) :
        self.tr_attachmentPublish(browser, self.trading, self.taxation, self.right)
        time.sleep(3)
    
    def tr_attachmentTaxationReverse(self, browser) :
        self.tr_attachmentPublish(browser, self.trading, self.taxation, self.reverse)
        time.sleep(3)

    def tr_attachmentTaxSmall(self, browser) :
        self.tr_attachmentPublish(browser, self.trading, self.taxSmall, self.right)
        time.sleep(3)

    def tr_attachmentTaxSmallReverse(self, browser) :
        self.tr_attachmentPublish(browser, self.trading, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tr_attachmentTaxFree(self, browser) :
        self.tr_attachmentPublish(browser, self.trading, self.taxFree, self.right)
        time.sleep(3)
    
    def tr_attachmentTaxFreeReverse(self, browser) :
        self.tr_attachmentPublish(browser, self.trading, self.taxFree, self.reverse)
        time.sleep(3)

    # 거래명세서 양식 저장 > 리스트에서 첨부발행
    def tr_attachmentListTaxation(self, browser) :
        self.tr_attachmentListPublish(browser, self.trading, self.taxation, self.right)
        time.sleep(3)
    
    def tr_attachmentListTaxationReverse(self, browser) :
        self.tr_attachmentListPublish(browser, self.trading, self.taxation, self.reverse)
        time.sleep(3)

    def tr_attachmentListTaxSmall(self, browser) :
        self.tr_attachmentListPublish(browser, self.trading, self.taxSmall, self.right)
        time.sleep(3)

    def tr_attachmentListTaxSmallReverse(self, browser) :
        self.tr_attachmentListPublish(browser, self.trading, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tr_attachmentListTaxFree(self, browser) :
        self.tr_attachmentListPublish(browser, self.trading, self.taxFree, self.right)
        time.sleep(3)
    
    def tr_attachmentListTaxFreeReverse(self, browser) :
        self.tr_attachmentListPublish(browser, self.trading, self.taxFree, self.reverse)
        time.sleep(3)

    # 거래명세서 양식 저장 > 상세에서 첨부발행
    def tr_attachmentDetailTaxation(self, browser) :
        self.tr_attachmentDetailPublish(browser, self.trading, self.taxation, self.right)
        time.sleep(3)
    
    def tr_attachmentDetailTaxationReverse(self, browser) :
        self.tr_attachmentDetailPublish(browser, self.trading, self.taxation, self.reverse)
        time.sleep(3)

    def tr_attachmentDetailTaxSmall(self, browser) :
        self.tr_attachmentDetailPublish(browser, self.trading, self.taxSmall, self.right)
        time.sleep(3)

    def tr_attachmentDetailTaxSmallReverse(self, browser) :
        self.tr_attachmentDetailPublish(browser, self.trading, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tr_attachmentDetailTaxFree(self, browser) :
        self.tr_attachmentDetailPublish(browser, self.trading, self.taxFree, self.right)
        time.sleep(3)
    
    def tr_attachmentDetailTaxFreeReverse(self, browser) :
        self.tr_attachmentDetailPublish(browser, self.trading, self.taxFree, self.reverse)
        time.sleep(3)

    # 거래명세서 간편 발행
    def tr_simpleTaxation(self, browser) :
        self.tax_simplePublish(browser, self.trading, self.taxation, self.right)
        time.sleep(3)
    
    def tr_simpleTaxationReverse(self, browser) :
        self.tax_simplePublish(browser, self.trading, self.taxation, self.reverse)
        time.sleep(3)

    def tr_simpleTaxSmall(self, browser) :
        self.tax_simplePublish(browser, self.trading, self.taxSmall, self.right)
        time.sleep(3)

    def tr_simpleTaxSmallReverse(self, browser) :
        self.tax_simplePublish(browser, self.trading, self.taxSmall, self.reverse)
        time.sleep(3)
    
    def tr_simpleTaxFree(self, browser) :
        self.tax_simplePublish(browser, self.trading, self.taxFree, self.right)
        time.sleep(1)
    
    def tr_simpleTaxFreeReverse(self, browser) :
        self.tax_simplePublish(browser, self.trading, self.taxFree, self.reverse)
        time.sleep(3)

    # 전자세금계산서 삭제
    def tax_todayDeleteBtn(self, browser) :
        self.tax_todayDelete(browser, self.tax)
        self.tax_todayDelete(browser, self.trading)
        self.tax_todayDelete(browser, self.receipt)
        self.tax_todayDelete(browser, self.deposit)
    
    def tax_savedDeleteBtn(self, browser) :
        self.tax_savedDelete(browser, self.tax)
        self.tax_savedDelete(browser, self.trading)
        self.tax_savedDelete(browser, self.receipt)
        self.tax_savedDelete(browser, self.deposit)

class Meet :
    def meet_create(self, browser, reserve=None) :
        meetName = varname.meetingName; sameName = varname.sameMeetingName
        participant =varname.meetingParticipant; createBtn = varname.meetingCreateBtn
        reserveBtn=varname.meetingReserveBtn; hour=varname.meetingHour; min=varname.meetingMinute

        browser_click(browser, 'start', CLASS_NAME)
        time.sleep(3)
        enter(browser, meetName, '화상대화방방')
        time.sleep(1)
        if '중복되는 회의명입니다.' in context(browser, sameName) :
            browser_sendKey(browser, meetName, str(currentTime())[5:16])
        time.sleep(1)

        inputUser(browser, participant, sec=5)
        time.sleep(1)
        if wehagoBrand != 3 :
            browser_click(browser, 'common_onoff_switch.false', CLASS_NAME)

        if reserve :
            browser_click(browser, reserveBtn)
            browser_sendKey(browser, hour, currentTime().strftime('%I'))
            time.sleep(0.5)
            browser_sendKey(browser, min, currentTime().strftime('%M'))

        browser_click(browser, 'WSC_LUXSpriteIcon', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)

    def meet_createMeeting(self, browser) :
        self.meet_create(browser)
        time.sleep(5)
        if hasxpath(browser, varname.meetingPopup) :
            if context(browser, varname.meetingPopup) == '회의명 중복' :
                browser_click(browser, varname.confirm)
                Common().close(browser)
                raise Exception('화상회의 생성 확인 필요')
        browser.switch_to.window(browser.window_handles[1])
        browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)

        title = '화상회의 초대안내'
        if not self.meet_checkMail(browser, title) : raise Exception('화상회의 생성 메일 확인 필요')
        browser.switch_to.window(browser.window_handles[1])

    def meet_checkMail(self, browser, title, contents=None):
        time.sleep(15)
        checkUrl = getUrl('mail/sent?pageNo=1')
        browser.execute_script(f'window.open("{checkUrl}");')
        time.sleep(5)
        tab = len(browser.window_handles) - 1
        try :
            browser.switch_to.window(browser.window_handles[tab])
            if checkText(browser, WSC_LUXButton, '다음에') : btn_click(browser, WSC_LUXButton, '다음에')
            browser_click(browser, 'mail_list_item_0', ID)
            time.sleep(3)
            if contents : 
                if title in context(browser, varname.meet_mailContent) : return True
                else : return False
            else :
                if title in context(browser, varname.meet_mailTitle) : return True
                else: return False
        finally :
            browser.close()
            browser.switch_to.window(browser.window_handles[tab-1])

    def meet_createReservedMeeting(self, browser) :
        self.meet_create(browser, True)
        if hasxpath(browser, varname.meetingPopup) : 
            if context(browser, varname.meetingPopup) == '일정 중복' :
                browser_click(browser, varname.confirm)
        time.sleep(1)

        if not checkText(browser, 'join', '예약정보 확인') : raise Exception('화상회의 예약 확인 필요')

        if not self.meet_checkMail(browser, '예정시간', True) : raise Exception('화상회의 예약 메일 확인 필요')

    def meet_modifyReservationMeeting(self, browser) :
        hour=varname.meetingHour; min=varname.meetingMinute
        btn_click(browser, 'join', '예약정보 확인')
        time.sleep(1)
        modifyTime = currentTime() + datetime.timedelta(minutes=27)
        browser_sendKey(browser, hour, modifyTime.strftime('%I'))
        time.sleep(0.5)
        browser_sendKey(browser, min, modifyTime.strftime('%M'))
        time.sleep(0.5)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(1)

        title = '화상회의 변경안내'
        if not self.meet_checkMail(browser, title) : raise Exception('화상회의 변경 메일 확인 필요')
    
    def meet_reservationcancel(self, browser) :
        # reserve = varname.meetingReservation; cancel = varname.meetingReservationCancel

        btn_click(browser, 'join', '예약정보 확인')
        time.sleep(3)
        btn_click(browser, WSC_LUXButton, '예약취소')
        time.sleep(1)
        browser_click(browser, varname.confirm)

        title = '화상회의 삭제안내'
        if not self.meet_checkMail(browser, title) : raise Exception('화상회의 예약취소 메일 확인 필요')

    def meet_reservedList(self, browser) :
        btn_click(browser, 'details', '참석 예정자 명단')
        time.sleep(3)
        try :
            if '2' != context(browser, 'nomg', CLASS_NAME) :
                raise Exception('화상회의 참석예정자 명단 확인 필요')
        finally :
            Common().close(browser)

    def meet_screenShare(self, browser) :
        time.sleep(3)
        browser_click(browser, 'btn.btn_screenshare', CLASS_NAME)
        try :
            browser.switch_to.alert.dismiss()
        except :
            raise Exception('화면공유 확인 필요')
    
    def meet_documentShare(self, browser) :
        browser_click(browser, 'btn.btn_documentshare', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'doc', CLASS_NAME)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2', confirm)
        time.sleep(1)
        if hasxpath(browser, 'nodata_text', CLASS_NAME) :
            Common().close(browser)
        else :
            browser_click(browser, 'LUX_basic_switch', CLASS_NAME)
            browser_click(browser, varname.addFileConfirm)
            time.sleep(5)
            if hasxpath(browser, 'LUX_basic_btn.Default.basic.btn_fileclose', CLASS_NAME) :
                browser_sendKey(browser, 'LUX_basic_btn.Default.basic.btn_fileclose', Keys.ENTER, CLASS_NAME)
                time.sleep(1)
                btn_click(browser, WSC_LUXButton, confirm)
            else :
                raise Exception('문서공유 확인 필요')

    def meet_externalSharing(self, browser) : 
        time.sleep(1)
        browser_click(browser, 'btn.btn_rtcshare', CLASS_NAME)
        time.sleep(1)
        copyList = browser.find_elements(By.CLASS_NAME, 'sp_rtc')
        copyList[-2].click()
        url = clipboard.paste()
        copyList[-1].click()
        code = clipboard.paste()
        time.sleep(1)
        Common().close(browser)
        browser2 = chromeBrowser()
        browser2.get(url)
        time.sleep(5)
        if wehagoBrand == 3 : joinCode = varname.v_joinCode; joinName = varname.v_joinName
        else : joinCode = varname.joinCode; joinName = varname.joinName
        browser_sendKey(browser2, joinCode, code)
        browser_sendKey(browser2, joinName, '외부참여자123')
        browser_click(browser2, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
        time.sleep(1)
        btn_click(browser2, WSC_LUXButton, confirm)
        time.sleep(5)
        try :
            if wehagoBrand == 3 :
                browser_click(browser, '//*[@id="root"]/div/div/div[2]/div[4]/div/div/div[3]/button[1]')
                time.sleep(5)
            if not hasxpath(browser2, 'label.smallfont', CLASS_NAME) : raise Exception('화상회의 외부참여자 확인 필요')
        finally :
            browser2.quit()
    
    def meet_inviteMail(self, browser) :
        message = '화상회의 생성 후 이메일 초대'
        browser_click(browser, 'btn.btn_rtcshare', CLASS_NAME)
        time.sleep(1)
        if wehagoBrand == 3 :
            enter(browser, varname.meetInviteMail, 'vqatest02@wehagov.com')
        else :
            enter(browser, varname.meetInviteMail, 'stestjy_1919@wehago.com')
        browser_sendKey(browser, varname.meetInviteMessage, message)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.basic2 ', CLASS_NAME)
        time.sleep(5)
        Common().close(browser)
        browser2 = chromeBrowser()
        time.sleep(3)
        self.meet_mailEnter(browser2, message)
        if wehagoBrand == 3 :
            browser_click(browser, '//*[@id="root"]/div/div/div[2]/div[4]/div/div/div[3]/button[1]')
            time.sleep(5)
        browser2.quit()

    def meet_mailEnter(self, browser, message) :
        # 메일 확인해서, 
        if wehagoBrand == 3 :
            Login().login(browser, 'vqatest02')
        else :
            Login().login(browser, 'stestjy_1919')
        browser.get(getUrl('mail'))
        time.sleep(5)
        browser_click(browser, 'mail_list_item_0', ID)
        time.sleep(3)
        mailText = browser.find_element(By.XPATH, varname.meet_mailText).text
        if message != mailText : raise Exception('화상회의 이메일 초대 확인 필요')
        pageDown(browser, 'em_content.null', CLASS_NAME)
        browser_click(browser, varname.meet_mailEnter)
        time.sleep(5)
        count = len(browser.window_handles)
        if count != 2 : raise Exception('메일에서 접속 버튼 클릭 확인필요')
        else :
            browser.switch_to.window(browser.window_handles[1])
            if wehagoBrand == 3 : name = '//*[@id="root"]/div/div/div[2]/div/div/div[1]/div/table/tbody/tr/td/div/div/input'
            else : name = '//*[@id="root"]/div/div[1]/div/div[2]/div/div/div[1]/div/table/tbody/tr/td/div/div/input'
            browser_sendKey(browser, name, '메이루')
            browser_click(browser, 'LUX_basic_btn.Confirm.basic2', CLASS_NAME)
            time.sleep(1)
            btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
    
    def meet_chatting(self, browser) :
        browser_click(browser, 'btn.btn_rtcchat', CLASS_NAME)
        enter(browser, 'input_msg', '화상회의~!', CLASS_NAME)
        if not hasxpath(browser, 'msg', CLASS_NAME) :
            raise Exception('화상회의 채팅 확인 필요')

    def meet_exportUser(self, browser) :
        if not hasxpath(browser, 'user_area.party.full', CLASS_NAME) : browser_click(browser, 'btn.btn_rtcppl', CLASS_NAME)
        time.sleep(1)
        if '(1/50)' in context(browser, 'user_area.party.full', CLASS_NAME) :
            raise Exception('화상회의 참여자목록 확인 필요')
        user = browser.find_elements(By.CLASS_NAME, 'moremore ')
        user[-1].click()
        time.sleep(1)
        browser.find_element(By.XPATH, '//li[contains(., "내보내기")]').click()
        btn_click(browser, WSC_LUXButton, confirm)

        # if '(1/50)' not in context(browser, 'user_area.party.full', CLASS_NAME) :
        #     raise Exception('화상회의 내보내기 확인')
        
    def meet_searchRecord(self, browser) :
        btn_click(browser, 'no_depth ', '회의기록')
        browser_click(browser, 'round_btn.more', CLASS_NAME)
        time.sleep(1)
        enter(browser, varname.meet_searchParticipant, '메이루', sec=3)
        browser_click(browser, 'round_btn.blue', CLASS_NAME)
        time.sleep(3)
        if hasxpath(browser, 'empty_area.v2', CLASS_NAME) : raise Exception('회의기록 검색 확인 필요')

class Fax :
    def fax_number(self) :
        if wehagoBrand == 1 :
            faxNumber = '050717977148'
        else :
            faxNumber = '050717977142'
        return faxNumber

    def fax_quickSendFax(self, browser) :
        browser_click(browser, varname.sendFax)
        browser_click(browser, 'sp_fx.ico_quick_view', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, varname.faxReceiver)
        action = ActionChains(browser)
        action.send_keys(self.fax_number()).pause(1).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        waitseconds(20)
        # 30초 대기했는데 변환 안됬다고 가정
        if context(browser, varname.q_faxCount) == '0장' :
            waitseconds(10)
        btn_click(browser, WSC_LUXButton, '팩스 보내기')
        if sameText(browser, '전송문서를 첨부해주세요.') :
            btn_click(browser, WSC_LUXButton, confirm)
            raise Exception('팩스전송 확인')

        btn_click(browser, WSC_LUXButton, confirm)
        progress(browser)
        if sameText(browser, '포인트가 부족합니다.') :
            browser_click(browser, varname.confirm)
            raise Exception('포인트 없음')
        browser.refresh()
        time.sleep(3)

    def fax_generalSendFax(self, browser) :
        browser_click(browser, 'sp_fx.ico_normal_view', CLASS_NAME)
        time.sleep(1)
        fax = browser.find_element(By.XPATH, '//*[@id="gridSmartComplete1"]/div/canvas')
        action = ActionChains(browser)
        action.move_to_element_with_offset(fax, 50, 16).double_click().send_keys(self.fax_number()).pause(0.5).send_keys(Keys.TAB).perform()
        action.reset_actions()
        time.sleep(1)
        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        waitseconds(30)
        # 30초 대기했는데 변환 안됬다고 가정
        if context(browser, varname.g_faxCount) == '0장' :
            waitseconds(10)
        browser_click(browser, varname.g_sendFaxButton)
        if sameText(browser, '전송문서를 첨부해주세요.') :
            browser_click(browser, varname.confirm)
            raise Exception('팩스전송 확인')
        elif sameText(browser, '팩스번호를 입력해주세요') :
            browser_click(browser, varname.confirm)
            action = ActionChains(browser)
            action.move_to_element_with_offset(fax, 50, 16).double_click().send_keys(self.fax_number()).pause(0.5).send_keys(Keys.TAB).perform()
            action.reset_actions()
            time.sleep(1)
            browser_click(browser, varname.g_sendFaxButton)
        browser_click(browser, varname.g_faxConfirm)
        progress(browser)
        browser.refresh()
        time.sleep(3)

    def fax_deleteFax(self, browser) :
        # 팩스함 삭제
        browser_click(browser, varname.faxbox)
        progress(browser)
        browser_click(browser, 'WSC_LUXCheckBox', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, '추가기능')
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, delete)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)
        # 전송결과 삭제
        browser_click(browser, varname.transmission)
        progress(browser)
        browser_click(browser, 'WSC_LUXCheckBox', CLASS_NAME)
        btn_click(browser, WSC_LUXButton, delete)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(3)

class Sms :
    sendsns='문자보내기'
    def sms_sendButton(self, browser) :
        try :
            print('3')
            pageDown(browser, 'sms_content', CLASS_NAME)
            print(hasxpath(browser, 'SMSSend', ID))
            browser_click(browser, 'SMSSend', ID)
            time.sleep(1)
            if sameText(browser, '핸드폰번호를 입력해주세요.') :
                print('4')
                browser_click(browser, varname.confirm)
                browser_click(browser, 'SMSSend', ID)
                time.sleep(3)
            print('5')
            pageDown(browser, 'dialog_content.sms_ver', CLASS_NAME)
            btn_click(browser, WSC_LUXButton, self.sendsns)
            time.sleep(5)
            if sameText(browser, '문자전송이 실패하였습니다.') :
                browser_click(browser, varname.confirm)
                raise Exception('지금 포인트 없어요?')
            if hasxpath(browser, 'gl_bx_cnt', CLASS_NAME) :
                browser_click(browser, varname.smsCancel)
                raise Exception('포인트 부족')
        finally :
            Common().close(browser)

    def sms_sendText(self, browser) :
        li_click(browser, self.sendsns)
        browser_sendKey(browser, '//*[@id="tAreaMsg"]', currentTime().strftime('%H:%M') + ' 일반 문자보내기' + str(wehagoBrand))
        sms = browser.find_element(By.XPATH, '//*[@id="grdNormal"]/div/canvas')
        action = ActionChains(browser)
        action.move_to_element_with_offset(sms, 50, 16).double_click().send_keys('01045681896').pause(3).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(3)
        self.sms_sendButton(browser)
    
    def sms_sendExcel(self, browser) :
        li_click(browser, self.sendsns)
        li_click(browser, '엑셀 보내기')
        time.sleep(3)
        browser_sendKey(browser, '//*[@id="tAreaMsg"]', currentTime().strftime('%H:%M') + ' 엑셀 문자보내기' + str(wehagoBrand))
        for i in range(1,5) :
            button = '//*[@id="BODY_CLASS"]/div[3]/div/div/div/div[1]/div[2]/div/div[3]/div[1]/div/div[3]/ul/li['
            button = button + str(i) + ']'
            browser_click(browser, button)
        time.sleep(3)
        print('1')
        sms = browser.find_element(By.XPATH, '//*[@id="grdEachExcel"]/div/canvas')
        action = ActionChains(browser)
        action.move_to_element_with_offset(sms, 50, 16).double_click().send_keys('01045681896').pause(3).send_keys(Keys.TAB).send_keys(Keys.ENTER)
        action.send_keys('테스트회사').pause(1).send_keys(Keys.TAB).send_keys(Keys.ENTER).send_keys('이대표').pause(1).send_keys(Keys.TAB).send_keys(Keys.ENTER)
        action.send_keys('하나둘셋').pause(1).send_keys(Keys.ENTER).pause(1).send_keys(Keys.RIGHT).send_keys('321').pause(1).send_keys(Keys.ENTER).pause(1).send_keys(Keys.RIGHT)
        action.send_keys('one Two Three').pause(1).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(3)
        self.sms_sendButton(browser)

    def sms_sendIndividualText(self, browser) :
        li_click(browser, self.sendsns)
        li_click(browser, '엑셀 보내기')
        time.sleep(1)
        browser_click(browser, varname.individualText)
        sms = browser.find_element(By.XPATH, '//*[@id="grdAllExcel"]/div/canvas')
        action = ActionChains(browser)
        action.move_to_element_with_offset(sms, 50, 16).double_click().send_keys('01045681896').pause(3).send_keys(Keys.TAB).send_keys(Keys.ENTER)
        action.send_keys('테스트회사').pause(1).send_keys(Keys.TAB).send_keys(Keys.ENTER).send_keys(currentTime().strftime('%H:%M') + ' 엑셀 개별문자보내기' + str(wehagoBrand)).pause(1).send_keys(Keys.ENTER).perform()
        action.reset_actions()
        time.sleep(3)
        self.sms_sendButton(browser)

class WeStudio :
    channel = '채널스~'; title = '동영상업로드'; timeLink = '타임링크추가'
    video='동영상'; live='라이브'
    def ws_createChannel(self, browser) :
        browser_click(browser, 'channel', CLASS_NAME)
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.Default.darkmode', '채널추가')
        time.sleep(1)
        browser_sendKey(browser, 'title_input', currentTime().strftime('%H:%M') + self.channel, CLASS_NAME)
        Common().fileUpload(browser, 'btn_webot.png')
        browser_click(browser, '//*[@id="containerWrap"]/div/div/div[2]/span/div/span[3]/span')
        browser_click(browser, 'ant-btn.ant-btn-primary', CLASS_NAME)
        time.sleep(3)
        btn_click(browser, 'ant-btn ant-btn-primary', save)
        time.sleep(1)
        btn_click(browser, WSC_LUXButton, confirm)
        time.sleep(5)
        if not hasxpath(browser, 'cha_mng', CLASS_NAME) :
            raise Exception('채널 생성 확인 필요') 

        browser_click(browser, 'cha_mng', CLASS_NAME)
        time.sleep(3)
        if '채널관리자' not in context(browser, 'wetv_channel_listitem', CLASS_NAME) :
            raise Exception('채널 관리 진입 확인 필요')

    def ws_deleteChannel(self, browser) :
        browser_click(browser, 'setting', CLASS_NAME)
        time.sleep(1)
        while True :
            if hasxpath(browser, 'LUX_basic_btn.SAOverConfirm.darkmode2', CLASS_NAME) :
                btn_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode2', '채널삭제')
                btn_click(browser, WSC_LUXButton, '삭제')
                time.sleep(5)
            else : break

        browser_click(browser, 'channel', CLASS_NAME)
        time.sleep(1)
        enter(browser, '//*[@id="btn_submit"]', self.channel)
        if not hasxpath(browser, 'channel_empty_wrap', CLASS_NAME) :
            raise Exception('채널 삭제 확인 필요')

    def ws_searchChannel(self, browser) :
        browser_click(browser, 'channel', CLASS_NAME)
        time.sleep(1)
        enter(browser, '//*[@id="btn_submit"]', self.channel)
        browser_click(browser,'wetv_channel_listitem', CLASS_NAME)
        time.sleep(1)

    def ws_researvedLive(self, browser) :
        if hasxpath(browser, varname.liveStart):
            # 라이브 예약
            time.sleep(1)
            browser_click(browser, varname.liveStart)
        time.sleep(1)
        browser_sendKey(browser, 'title_input', currentTime().strftime('%H:%M') + '라이브예약', CLASS_NAME)
        Common().fileUpload(browser, 'btn_webot.png')
        btn_click(browser, 'LUXrabx', '비공개')
        btn_click(browser, 'LUXrabx', '사용')
        btn_click(browser, 'LUXrabx', '설정')
        time.sleep(1)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode2', CLASS_NAME)
        time.sleep(5)
        # 예약한 라이브가 라이브관리에서 보이는지
        browser_click(browser, 'live_mng', CLASS_NAME)
        browser_click(browser, varname.reservedLive)
        time.sleep(3)
        try :
            if not hasxpath(browser, '//*[@id="westudio_lnb"]/div[2]/div[2]/div/div/div[1]/div/div/div/div[2]/ul[2]/li[1]') :
                raise Exception('라이브 예약 확인 필요')
        finally : Common().close(browser)

    def ws_changeReservation(self, browser) :
        while True :
            browser_click(browser, 'live_mng', CLASS_NAME)
            browser_click(browser, varname.reservedLive)
            time.sleep(1)
            if hasxpath(browser, varname.reservedLiveList) :
                browser_click(browser, varname.reservedLiveList)
                time.sleep(3)
                btn_click(browser, 'LUXrabx', '설정안함(즉시공개)')
                time.sleep(1)
                browser_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode2', CLASS_NAME)
                time.sleep(5)
                if not checkText(browser, 'LUX_basic_btn.Default.darkmode', 'LIVE종료') :
                    raise Exception('예약 라이브 설정변경 확인 필요')
                btn_click(browser, 'LUX_basic_btn.Default.darkmode', 'LIVE종료')
                btn_click(browser, WSC_LUXButton, '종료')
                time.sleep(3)
            else :
                Common().close(browser)
                break 

    def ws_uploadLocalDetail(self, browser, option=None) :
        if hasxpath(browser, varname.uploadVideo) :
            browser_click(browser, varname.uploadVideo) 
        time.sleep(3)
        fileUp = browser.find_elements_by_css_selector('input[type="file"]')
        fileUp[0].send_keys(path+'//videotest.mp4')
        for i in range (0,30) :
            if hasxpath(browser, 'LS_loader', CLASS_NAME) : time.sleep(3)
            else : break
        fileUp[1].send_keys(path+'//btn_webot.png')
        time.sleep(3)
        if option : title = self.title + self.timeLink
        else : title = self.title
        browser_sendKey(browser, varname.videoTitle, currentTime().strftime('%H:%M') + title)
        pageDown(browser, 'file_upload.with_elev', CLASS_NAME)
        # 공개여부 설정
        btn_click(browser, 'LUXrabx', '비공개')
        time.sleep(0.5)
        if option : self.ws_uploadLocalSetting(browser)
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode2', '저장')
        self.ws_waitUpload(browser)

    def ws_uploadLocalSetting(self, browser) :
        # 카테고리 추가
        browser_click(browser, 'inputElement', ID)
        time.sleep(1)
        # IT과학기술
        browser_click(browser,'//*[@id="scrollElement"]/div/ul/div[3]/li')
        time.sleep(1)
        
        # 타임링크 추가
        btn = browser.find_elements(By.CLASS_NAME, 'LUXrabx')
        btn[-2].click()
        time.sleep(1)
        action = ActionChains(browser)
        action.send_keys(Keys.TAB).send_keys('타임링크추가').send_keys(Keys.TAB).send_keys('00:00:06').send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
        action.reset_actions()

    def ws_waitUpload(self, browser) :
        count = 1
        while True :
            count += 1
            if hasxpath(browser, 'ico_done.sp_tv', CLASS_NAME) :
                browser_click(browser, '//*[@id="wrap"]/div[3]/div/button[2]/span')
                break
            else :
                if count < 60 : time.sleep(1)
                else : raise Exception('동영상 업로드 확인 필요')

    def ws_updateChannel(self, browser, type) :
        browser_click(browser, 'update.brdtop', CLASS_NAME)
        time.sleep(3)
        enter(browser, varname.updChannel, self.channel)
        browser_click(browser, '//*[@id="westudio_lnb"]/div[1]/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]/ul/li')
        if type == self.video : browser_click(browser, varname.updVideo)
        elif type == self.live : browser_click(browser, varname.updLive)
        time.sleep(1)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode2', CLASS_NAME)
        time.sleep(1)

    def ws_uploadVideo_ch(self, browser) :
        self.ws_searchChannel(browser)
        self.ws_uploadLocalDetail(browser)

    def ws_uploadVideo_upd(self, browser) :
        self.ws_updateChannel(browser, self.video)
        self.ws_uploadLocalDetail(browser)

    def ws_uploadVideoOption(self, browser) :
        self.ws_searchChannel(browser)
        self.ws_uploadLocalDetail(browser, True)

    def ws_uploadUrlDetail(self, browser) :
        if hasxpath(browser, varname.uploadVideo) :
            browser_click(browser, varname.uploadVideo)
        browser_click(browser, varname.uploadUrl)
        browser_sendKey(browser, varname.urlAddress, 'https://www.youtube.com/watch?v=e2hfX_Yr6Wg')
        browser_sendKey(browser, varname.videoTitle, currentTime().strftime('%H:%M') + 'URL동영상업로드')
        Common().fileUpload(browser, 'btn_webot.png')
        # 공개여부 설정
        btn_click(browser, 'LUXrabx', '비공개')
        time.sleep(0.5)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode2', '저장')
        time.sleep(3)
    
    def ws_uploadUrl_ch(self, browser) :
        self.ws_searchChannel(browser)
        self.ws_uploadUrlDetail(browser)

    def ws_uploadUrl_upd(self, browser) :
        self.ws_updateChannel(browser, self.video)
        self.ws_uploadUrlDetail(browser)

    def ws_researvedLive_ch(self, browser) :
        self.ws_searchChannel(browser)
        self.ws_researvedLive(browser)

    def ws_researvedLive_upd(self, browser) :
        self.ws_updateChannel(browser, self.live)
        self.ws_researvedLive(browser)

    def ws_searchVideo(self, browser) :
        self.ws_searchChannel(browser)
        enter(browser, '//*[@id="containerWrap"]/div/div[2]/div/div/input', '동영상')
        time.sleep(1)
        if hasxpath(browser, 'channel_empty_wrap', CLASS_NAME) :
            raise Exception('동영상 검색 확인 필요')

    def ws_modifyVideo(self, browser) :
        self.ws_searchChannel(browser)
        browser_click(browser, 'wetv_video_listitem.v2', CLASS_NAME)
        time.sleep(3)
        btn_click(browser, 'LUX_basic_btn.Default.darkmode', '수정')
        time.sleep(1)
        browser_sendKey(browser, varname.videoTitleModify, '수정~')
        browser_click(browser, varname.saveModifyVideoBtn)

    def ws_deleteVideo(self, browser) :
        self.ws_searchChannel(browser)
        while hasxpath(browser, 'wetv_video_listitem.v2', CLASS_NAME) :
            browser_click(browser, 'wetv_video_listitem.v2', CLASS_NAME)
            time.sleep(1)
            btn_click(browser, 'LUX_basic_btn.Default.darkmode', '수정')
            time.sleep(1)
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode', delete)
            btn_click(browser, WSC_LUXButton, delete)
            time.sleep(3)

    def ws_addPlaylist(self, browser) :
        self.ws_searchChannel(browser)
        browser.find_element(By.XPATH, '//li[contains(., "재생목록")]').click()
        time.sleep(0.5)
        browser_click(browser, 'LUX_basic_btn.SAOverConfirm2.basic2', CLASS_NAME)
        time.sleep(1)
        textClear(browser, varname.playlistName)
        enter(browser, varname.playlistName, '재생목록하나')
        btn_click(browser, 'LUX_basic_btn.Default.darkmode2', save)
        time.sleep(3)
        btn_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode2', '닫기')
        time.sleep(1)
        if '생성된 재생목록 (1)' not in context(browser, 'list_title.clearfix', CLASS_NAME) :
            raise Exception('재생목록 추가 확인 필요')

    def ws_deletePlaylist(self, browser) :
        browser_click(browser, varname.editPlaylist)
        browser_click(browser, 'btn_delete', CLASS_NAME)
        time.sleep(3)
        Common().close(browser)

    def ws_checkOption(self, browser) :
        browser_click(browser, '//*[@id="category"]/ul/li[2]')
        time.sleep(1)
        video = browser.find_elements(By.CLASS_NAME, 'ellipsis2')
        video[0].click()
        time.sleep(3)
        title = browser.find_element(By.CLASS_NAME, 'titlebox').text
        if self.timeLink not in title : raise Exception('위스튜디오 카테고리 이동 확인 필요')
        if not hasxpath(browser, 'listitem', CLASS_NAME) : raise Exception('타임링크 추가 확인 필요')
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.Default.darkmode', '수정')
        time.sleep(1)
        try :
            if not hasxpath(browser, 'timelink_li', CLASS_NAME) : raise Exception('수정화면에서 타임라인 확인 필요')
            if 'IT/과학기술' != context(browser, '//*[@id="inputElement"]') : raise Exception('수정화면에서 카테고리 확인 필요')
        finally :
            btn_click(browser, 'LUX_basic_btn.SAOverConfirm.darkmode', '취소')
            browser_click(browser, varname.confirm_ws)

    def ws_addComment(self, browser) : 
        browser_sendKey(browser, 'reply_inputbox', '여기가 위스튜디오 댓글입니까', ID)
        browser_click(browser, 'LS_btn.basic2', CLASS_NAME)
        time.sleep(1)
        if '(1)' not in context(browser, 'replycount', CLASS_NAME) : raise Exception('위스튜디오 댓글 확인 필요')

    def ws_checkChannel(self, browser) :
        browser2 = chromeBrowser()
        browser2.get('https://www.wehago.com/westudio/channel')
        time.sleep(5)
        try :
            if checkText(browser2, 'wetv_channel_listitem', self.channel) : raise Exception('비공개 채널 조회 확인 필요')
        finally : browser2.quit()
        
    def ws_watchRecord(self, browser) :
        browser_click(browser, '//*[@id="lnbmy"]/ul/li')
        time.sleep(3)
        if '최근시청기록' not in context(browser, 'con_title', CLASS_NAME) : raise Exception('최근 시청기록 클릭 확인 필요')
        if hasxpath(browser, 'empty_txt.v5', CLASS_NAME) : raise Exception('최근 시청 기록 확인 필요')
        time.sleep(1)
        btn_click(browser, 'LUX_basic_btn.Default.darkmode', '최근시청기록 삭제')
        browser_click(browser, varname.confirm_ws)
        time.sleep(5)

        # 기록 중지
        btn_click(browser, 'LUX_basic_btn.Default.darkmode', '기록저장 중지')
        browser_click(browser, varname.confirm_ws)
        time.sleep(1)
        browser_click(browser, '//*[@id="category"]/ul/li[2]')
        time.sleep(1)
        browser_click(browser, 'wetv_video_listitem.v2', CLASS_NAME)
        browser_click(browser, '//*[@id="lnbmy"]/ul/li')
        time.sleep(3)
        if not hasxpath(browser, 'empty_txt.v5', CLASS_NAME) : raise Exception('기록 저장 중지 확인 필요')

        # 기록 시작
        time.sleep(5)
        btn_click(browser, 'LUX_basic_btn.Default.darkmode', '기록저장 시작')
        time.sleep(1)

    def ws_sharedBtn(self, browser) :
        btn_click(browser, 'LUX_basic_btn.Default.darkmode', '공유')
        browser_click(browser, 'btn_copyurl', CLASS_NAME)
        link = clipboard.paste()
        return link

    def ws_sharedVideo(self, browser) :
        self.ws_searchChannel(browser)
        # 새탭 확인
        browser_click(browser, 'wetv_video_listitem.v2', CLASS_NAME)
        time.sleep(1)
        videoName = browser.find_element(By.CLASS_NAME, 'video_tit.ellipsis').text
        link = self.ws_sharedBtn(browser)
        browser.execute_script(f'window.open("{link}");')
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[1])
        videoName2 = browser.find_element(By.CLASS_NAME, 'video_tit.ellipsis').text
        try :
            if videoName != videoName2 : raise Exception('위스튜디오 새탭열어서 공유 확인 필요')
        finally :
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        time.sleep(1)

        # 새창 확인
        browser2 = chromeBrowser()
        browser2.get(link)
        time.sleep(5)
        try :
            if not hasxpath(browser2, 'convert', CLASS_NAME) : raise Exception('위스튜디오 비공개 동영상 공유 확인 필요')
        finally : 
            browser2.quit()

class Webot :
    def wb_user(self, browser) :
        browser.get(path+'/webot-sample.html')
        time.sleep(3)
        browser_click(browser, 'wb-plugin', ID)
        time.sleep(1)
        browser.switch_to.frame(0)
        browser_click(browser, 'btn_start', CLASS_NAME)
        time.sleep(3)
        # 이용가이드 고 > 상담원 연결 고 (시나리오 변경 시 수정 )
        browser_click(browser, 'btn_basic', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'btn_basic', CLASS_NAME)
        time.sleep(1)
        # 사용자 정보 입력
        inputlist = browser.find_elements(By.CLASS_NAME, 'inp_basic')
        inputlist[0].send_keys('김더존')
        inputlist[1].send_keys('01011111111')
        inputlist[2].send_keys('smile_1896@naver.com')
        inputlist[3].send_keys('테스트_위봇테스트중')
        inputlist[4].send_keys('1111111119')
        # 약관동의 
        browser_click(browser, 'switch_basic', CLASS_NAME)
        time.sleep(1)
        browser_click(browser, 'btn_basic.check', CLASS_NAME)
        # 완료 후 자동 창 닫히는 부분 확인 필요
        time.sleep(1)
    
    def wb_userSendMessage(self, browser) :
        enter(browser, 'chat_input', '고객이 메시지 보냅니다.', by=CLASS_NAME)
        if not checkText(browser, 'chat_balloon', '고객이 메시지 보냅니다.') :
            raise Exception('고객 메시지 전송 확인 필요')
    
        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        time.sleep(3)
        if not hasxpath(browser, 'ico_down', CLASS_NAME) :
            raise Exception('고객 파일 업로드 확인 필요')

    def wb_counselorConnection(self, browser) : 
        browser.get('https://www.wehago.com/webot/#/')
        time.sleep(5)
        browser_click(browser, 'item_btn_bx', CLASS_NAME)
        time.sleep(3)
        browser_click(browser, '//*[@id="wrap"]/div/div/div[2]/div/div[1]/div/ul/li/div/div/div[1]')
        time.sleep(1)
        # 상담연결
        browser_click(browser, 'btn_basic.v2', CLASS_NAME)
        time.sleep(3)
        if not checkText(browser, 'chat_balloon', '상담원과 연결이 되었습니다.') :
            raise Exception('상담원 연결 확인 필요')    
    
    def wb_counselorSendMessage(self, browser) :
        enter(browser, 'chat_input', '상담원이 메시지 보냅니다.', by=CLASS_NAME)
        if not checkText(browser, 'chat_balloon', '상담원이 메시지 보냅니다.') :
            raise Exception('상담원 메시지 전송 확인 필요')

        Common().fileUpload(browser, 'Contacts_SampleFile.xlsx')
        time.sleep(3)
        fileList = browser.find_elements(By.CLASS_NAME, 'ico_down')
        if len(fileList) != 2 :
            raise Exception('상담원 파일 업로드 확인 필요')

    def wb_counselorSearch(self, browser) :
        li_click(browser, '진행중')
        time.sleep(3)
        browser_click(browser, 'btn_search', CLASS_NAME)
        time.sleep(0.5)
        enter(browser, '//*[@id="wrap"]/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div/input', '김더존')
        time.sleep(3)
        if checkText(browser, 'empty_txt.v2', '현재 진행중인 상담이 없습니다.') :
            raise Exception('위봇 검색 확인 필요')
 
    def wb_counselorHolding(self, browser) :
        btn_click(browser, 'btn_basic', '보류')
        browser_click(browser, varname.confirm)
        progress(browser)
        li_click(browser, '보류')
        time.sleep(3)
        if checkText(browser, 'empty_txt.v2', '보류 상담카드가 존재하지 않습니다.') :
            raise Exception('위봇 보류상태 확인 필요')

    def wb_counselorClose(self, browser) :
        # 완료
        browser_click(browser, 'btn_basic.v2', CLASS_NAME)
        browser_click(browser, varname.confirm)
        progress(browser)
        time.sleep(3)
        if not checkText(browser, 'chat_balloon', '상담이 종료되었습니다') :
            raise Exception('상담원 종료 확인 필요')    

    def wb_test(self,browser) :
        guestbrowser = chromeBrowser()
        self.wb_user(browser)
        self.wb_counselorConnection(browser)
        self.wb_userSendMessage(browser)
        self.wb_counselorSendMessage(browser)
        self.wb_counselorHolding(browser)
        self.wb_counselorClose(browser)

