#-*- coding: utf-8 -*-
import time, datetime, os, platform
import wehagotestrun, wehagotest, varname
import wehagoReport
from driver import wehagoID, chromeBrowser, checkSerivce

# service=(['message', 'accounts', 'contacts', 'schedule', 'communication', 'mail', 'todo',
#         'wecrm', 'wepms', 'note', 'approval', 'corporateCard', 'personalCard', 'attendance', 
#         'meet', 'companyboard', 'invoice', 'fax', 'sms', 'westudio', 'webot', 'webuilder', 'other'])
# serviceTest={}

if __name__ == "__main__" :
    #현재 폴더 경로 받아옴
    path = os.getcwd()
    version = int(input('1-기본 / 2-체크리스트 / 3-특정서비스\n(숫자만입력) '))
    if version != 3 :
        brand = int(input('1-WEHAGO / 2-WEHAGOT / 3-WEHAGOV / 4-발행\n(숫자만입력) '))
        id = wehagoID(version, brand)
        if brand == 4 or version == 2: checkSerivce(invoice=True)
        else : checkSerivce(invoice=False)
    else : 
        # 특정 서비스만 실행
        print('0-메시지/1-거래처/2-연락처/3-일정/4-메신저/5-메일\n6-할일/7-crm/8-pms/9-노트/10-전자결재')
        print('11-법인카드/12-개인카드/13-근태관리/14-화상회의/15-회사게시판\n16-전자세금계산서/17-팩스/18-문자/19-위스튜디오/20-위봇')
        number = map(int, input('\n숫자만 입력 ').split())
        id = wehagoID(version)
        checkSerivce(num=number)
    if version == 1 :
        # 메인
        count = 0
        while count < 300 :
            count += 1
            browser = chromeBrowser()
            print('WEHAGO 테스트 ' + str(count) + '번째 시작!')
            if brand == 4 :
                result = wehagoReport.WehagoResult()
                wehagotest.Login().login(browser, id)
                wehagotestrun.WehagoRun().invoiceRun(browser, version)
                result.savexl(3)
            else :
                wehagotestrun.WehagoRun().wehagoRun(browser, id, version, brand)
            print(str(count) + '번끝!')
            browser.quit()
    elif version == 2 :
        # 체크리스트
        browser = chromeBrowser() 
        print('WEHAGO 체크리스트 시작!')
        if brand != 3:
            wehagotestrun.WehagoRun().wehagoSetting(browser, id, version, brand)
        wehagotestrun.WehagoRun().wehagoRun(browser, id, version, brand)
        wehagoReport.reportRun(version, brand, False)
        print('WEHAGO 테스트 끝')
        browser.quit()
    elif version == 3 :
        # 특정 서비스
        browser = chromeBrowser()
        wehagotestrun.WehagoRun().wehagoRun(browser, id, version, 1)
    else :
        print('BYE')