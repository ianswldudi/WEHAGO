from typing import Tuple
import wehagotest
import wehagoReport
import datetime, os, time
from driver import chromeBrowser, serviceTest

def tabClose(browser) :
    count = len(browser.window_handles)
    if count != 1 :
        for i in range(count, 1, -1) :
            browser.switch_to.window(browser.window_handles[i-1])
            browser.close()
        browser.switch_to.window(browser.window_handles[0])

def serviceRun (browser, functionRun, serviceFunctionName, close=True) :
    result = wehagoReport.WehagoResult()
    global exer
    start = time.time()
    now = datetime.datetime.now()
    path = os.path.join(os.getcwd(), 'result/image/')
    fileName = now.strftime('%m-%d %Ih%Mm') + serviceFunctionName + ' Fail.png'
    try :
        if close :
            tabClose(browser)
        time.sleep(1)
        functionRun(browser)
        result.testSuccess(serviceFunctionName)
    except Exception as ex :
        print(serviceFunctionName)
        # 실패한 상황 캡쳐
        browser.save_screenshot(path + fileName)
        print(ex)
        exer = str(ex)
        result.testFailure(serviceFunctionName, exer[:45], fileName)
    result.runTime(serviceFunctionName, start)

def getUrl(service, by=True) :
    url = 'https://www.wehago'
    if by :
        if wehagotest.wehagoBrand == 3 :
            url = url + 'v.com/#/'
        elif wehagotest.wehagoBrand == 2 :
            url = url + 't.com/#/'
        else: 
            url = url + '.com/#/'
        url = url + service
    else :
        if wehagotest.wehagoBrand == 3 :
            url = url + 'v.com/'
        elif wehagotest.wehagoBrand == 2 :
            url = url + 't.com/'
        else: 
            url = url + '.com/'
        url = url + service  + '/#/'
    return url

def browserTitle (browser, title) :
    if title in browser.title : 
        return True
    else :
        return False

def appName (browser, service) :
    appName = browser.find_elements_by_class_name('app_name')
    for service in appName :
        if service.text == service :
            service.click()

class WehagoRun() :
    result = wehagoReport.WehagoResult()

    def invoiceRun(self, browser, version) :
        if version == 2:
            wehagotest.Login().logout(browser)
            wehagotest.Login().login(browser, 'iqatest')
            if serviceTest['invoice'] : InvoiceRun().invoiceUpdate(browser)
        else :
            # 전자세금계산서 테스트
            if serviceTest['invoice'] : InvoiceRun().invoice(browser)
        # 팩스 테스트
        if serviceTest['fax'] : FaxRun().fax(browser)
        # 문자 테스트
        if serviceTest['sms'] : SmsRun().sms(browser)
        # WEstudio 테스트
        if serviceTest['westudio'] : WeStudioRun().westudio(browser)
        # 위봇 테스트
        if serviceTest['webot'] : WebotRun().webot(browser)

    def wehagoRun(self, browser, id, version, brand) :
        wehagotest.Common().set_wehagoBrand(version, brand)
        #로그인 테스트
        wehagotest.Login().login(browser, id)
        #메시지 테스트
        if serviceTest['message'] : MessageRun().message(browser)
        #거래처 테스트
        if serviceTest['accounts'] : AccountsRun().accounts(browser)
        #연락처 테스트
        if serviceTest['contacts'] : ContactsRun().contacts(browser)
        #일정 테스트
        if serviceTest['schedule'] : ScheduleRun().schedule(browser)
        #메신저 테스트
        if serviceTest['communication'] : CommunicationRun().communication(browser)
        #메일 테스트
        if serviceTest['mail'] : MailRun().mail(browser)
        #할일 테스트
        if serviceTest['todo'] : TodoRun().todo(browser)
        #CRM 테스트
        if serviceTest['wecrm'] : WecrmRun().wecrm(browser)
        #PMS 테스트
        if serviceTest['wepms'] : WepmsRun().wepms(browser)
        #노트 테스트
        if serviceTest['note'] : NoteRun().note(browser)
        #전자결재 테스트
        if serviceTest['approval'] : ApprovalRun().approval(browser)
        #법인카드 테스트
        if serviceTest['corporateCard'] : CorporateCardRun().corporateCard(browser)
        #개인카드 테스트
        if serviceTest['personalCard'] : PersonalCardRun().personalCard(browser)
        #근태관리 테스트
        if serviceTest['attendance'] : AttendanceRun().attendance(browser)
        #회사게시판 테스트
        if serviceTest['companyboard'] : CompanyboardRun().companyboard(browser)
        # 화상회의 테스트
        if serviceTest['meet'] : MeetRun().meet(browser)
        if brand != 3 : 
            # 위빌더 테스트
            if serviceTest['webuilder'] : WebuilderRun().webuilder(browser)
            
        # 다른 사용자 테스트
        if serviceTest['other'] : UserCheck().userCheck(browser, version)
        self.invoiceRun(browser, version)
        self.result.savexl(version)

    # 회원가입~가입완료
    def wehagoJoinRun(self, browser, id, name, pay) :
        # wehago 회원가입
        wehagotest.Join().wehagoJoin(browser, id, name, pay)
        # 초기설정 진행
        wehagotest.Plan().plan(browser, pay, name)
        # 마켓 구매
        service = {'법인카드':'구매O', '개인카드':'구매O', '할일':'구매O', 'WE CRM':'구매O', 'WE PMS':'구매O', '전자결재':'구매O','근태관리':'구매O'}
        wehagotest.Market().market(browser, pay, name, service)
        # 정기결제 수단 등록, 도메인 구매, 직원초대
        CompanyRun().companySetting(browser)
        # # qatest123으로 가입
        # wehagotest.Join().employeeJoin(wehago)

    # 초기설정 팝업 노출되는 부분 작업
    def wehagoSetting(self, browser, id, version, brand) :
        wehagotest.Common().set_wehagoBrand(version, brand)
        #로그인 테스트
        wehagotest.Login().login(browser, id)
        # 개인설정 - 기본이메일 수정
        wehagotest.Personal().pe_setMail(browser, id)
        #회사설정 (서비스배포, 관리자권한 부여)
        CompanyRun().company(browser)
        #PMS 테스트 (초기설정 팝업창 입력)
        WepmsRun().wepmsSetting(browser)
        #CRM 테스트 (초기설정 팝업창 입력)
        WecrmRun().wecrmSetting(browser)
        #전자결재 자주쓰는 결재 등록
        ApprovalRun().approvalSetting(browser)
        #법인카드 등록
        CorporateCardRun().corporateCardSetting(browser)
        #개인카드 카드등록
        PersonalCardRun().personalCardSetting(browser)
        #근태관리 직원휴가일설정
        AttendanceRun().attendanceSetting(browser)
        wehagotest.Login().logout(browser)
        print('logout s')
        time.sleep(3)

class CompanyRun(wehagotest.Company) :
    def company(self, browser) :
        print("company s")
        browser.get(getUrl('company/management'))
        time.sleep(5)
        if browserTitle(browser, '회사정보 : 회사정보관리') :
            serviceRun(browser, self.cs_distribution, 'cs_distribution')
            # serviceRun(browser, self.cs_resignation, 'cs_resignation')
            # serviceRun(browser, self.cs_searchRetiree, 'cs_searchRetiree')
            # serviceRun(browser, self.cs_useCompanyMail, 'cs_useCompanyMail')
            # serviceRun(browser, self.cs_distributeDomain, 'cs_distributeDomain')
            # serviceRun(browser, self.cs_sharedMailSetting, 'cs_sharedMailSetting')
            browser.get(getUrl('company/management'))
            time.sleep(3)
            serviceRun(browser, self.cs_setAdministor, 'cs_setAdministor')
            time.sleep(3)

    def companySetting(self, browser) :
        print("company s")
        browser.get(getUrl('company/management'))
        time.sleep(5)
        if browserTitle(browser, '회사정보 : 회사정보관리') :
            # serviceRun(browser, self.cs_billingManagement, 'cs_billingManagement')
            # browser.get(getUrl('company/management'))
            # serviceRun(browser, self.cs_domainRegister, 'cs_domainRegister')
            # 직원 초대
            self.cs_addEmpolyee(browser)

class CommunicationRun(wehagotest.Communication) : 
    def communication (self, browser) :
        print("Communication s")
        browser.get(getUrl('communication2'))
        time.sleep(5)
        if browserTitle(browser, '메신저') :
            serviceRun(browser, self.cc_acceptParticipation, 'cc_acceptParticipation')
            serviceRun(browser, self.cc_acceptInvitedUser, 'cc_acceptInvitedUser')
            serviceRun(browser, self.cc_refusalParticipation, 'cc_refusalParticipation')
            serviceRun(browser, self.cc_exportUser, 'cc_exportUser')
            serviceRun(browser, self.cc_leaveChatRoom, 'cc_leaveChatRoom')
            serviceRun(browser, self.cc_createRoomByContacts, 'cc_createRoomByContacts')
            serviceRun(browser, self.cc_createRoomByInput, 'cc_createRoomByInput')
            serviceRun(browser, self.cc_createRoomByOrganization, 'cc_createRoomByOrganization')
            serviceRun(browser, self.cc_sendChat, 'cc_sendChat')
            serviceRun(browser, self.cc_deleteChat, 'cc_deleteChat')
            serviceRun(browser, self.cc_copyChat, 'cc_copyChat')
            serviceRun(browser, self.cc_addComment, 'cc_addComment')
            # serviceRun(browser, self.cc_addNotice, 'cc_addNotice')
            serviceRun(browser, self.cc_uploadLocal, 'cc_uploadLocal')
            serviceRun(browser, self.cc_uploadWedrive, 'cc_uploadWedrive')
            serviceRun(browser, self.cc_uploadFileTab, 'cc_uploadFileTab')
            serviceRun(browser, self.cc_collectFile, 'cc_collectFile')
            serviceRun(browser, self.cc_openWebOffice, 'cc_openWebOffice')
            serviceRun(browser, self.cc_appendingSchedule, 'cc_appendingSchedule')
            serviceRun(browser, self.cc_appendingAccount, 'cc_appendingAccount')
            serviceRun(browser, self.cc_appendingContact, 'cc_appendingContact')
            serviceRun(browser, self.cc_appendingMeet, 'cc_appendingMeet')
            serviceRun(browser, self.cc_appendingVote, 'cc_appendingVote')
            serviceRun(browser, self.cc_listVote, 'cc_listVote')
            serviceRun(browser, self.cc_appendingVideo, 'cc_appendingVideo')
            serviceRun(browser, self.cc_recentChat, 'cc_recentChat')
            serviceRun(browser, self.cc_searchChat, 'cc_searchChat')
            serviceRun(browser, self.cc_sharedChat, 'cc_sharedChat')
            serviceRun(browser, self.cc_settingGroup, 'cc_settingGroup')
            serviceRun(browser, self.cc_favoriteConversation, 'cc_favoriteConversation')
            serviceRun(browser, self.cc_unfavoriteConversation, 'cc_unfavoriteConversation')
            serviceRun(browser, self.cc_searchMention, 'cc_searchMention')
            serviceRun(browser, self.cc_checkUserProfile, 'cc_checkUserProfile')
            serviceRun(browser, self.cc_setAsMaster, 'cc_setAsMaster')
            serviceRun(browser, self.cc_createChat, 'cc_createChat')
            serviceRun(browser, self.cc_leaveChat, 'cc_leaveChat')
        else : 
            print('메신저 확인')
        time.sleep(3)

    def cc_update(self, browser, version, brand) :
        wehagotest.Login().og_login(browser, version, brand)
        print("Communication s")
        browser.get(getUrl('communication2'))
        time.sleep(5)
        if browserTitle(browser, '메신저') :
            serviceRun(browser, self.cc_acceptParticipation, 'cc_acceptParticipation')
            serviceRun(browser, self.cc_acceptInvitedUser, 'cc_acceptInvitedUser')
            serviceRun(browser, self.cc_refusalParticipation, 'cc_refusalParticipation')
            serviceRun(browser, self.cc_exportUser, 'cc_exportUser')
            serviceRun(browser, self.cc_leaveChatRoom, 'cc_leaveChatRoom')
        else : 
            print('메신저 확인')
        time.sleep(3)

class CompanyboardRun(wehagotest.Companyboard) :
    def companyboard(self, browser) :
        print("companyboard s")
        browser.get(getUrl('companyboard', False))
        time.sleep(5)
        if browserTitle(browser, '게시판') :
            serviceRun(browser, self.cb_createBoard, 'cb_createBoard')
            serviceRun(browser, self.cb_createPost_basic, 'cb_createPost_basic')
            serviceRun(browser, self.cb_comment_basic, 'cb_comment_basic')
            serviceRun(browser, self.cb_deletePost, 'cb_deletePost')
            serviceRun(browser, self.cb_createPost_blog, 'cb_createPost_blog')
            serviceRun(browser, self.cb_comment_blog, 'cb_comment_blog')
            serviceRun(browser, self.cb_createPost_gall, 'cb_createPost_gall')
            serviceRun(browser, self.cb_comment_gall, 'cb_comment_gall')
            serviceRun(browser, self.cb_createPost_feed, 'cb_createPost_feed')
            serviceRun(browser, self.cb_comment_feed, 'cb_comment_feed')
            serviceRun(browser, self.cb_removeBoard, 'cb_removeBoard')
        else : 
            print('회사게시판 확인')
        time.sleep(3)

class MessageRun(wehagotest.Message) :
    def message (self, browser) :
        print("message s")
        browser.get(getUrl('communication2/message/inbox'))
        time.sleep(5)
        if browserTitle(browser, '메시지') :
            serviceRun(browser, self.ms_sendMessage, 'ms_sendMessage')
            serviceRun(browser, self.ms_sendSecurityMessage, 'ms_sendSecurityMessage')
            serviceRun(browser, self.ms_addBoilerplate, 'ms_addBoilerplate')
            serviceRun(browser, self.ms_applyBoilerplate, 'ms_applyBoilerplate')
            serviceRun(browser, self.ms_readBoilerplate, 'ms_readBoilerplate')
            serviceRun(browser, self.ms_delBoilerplate, 'ms_delBoilerplate')
            serviceRun(browser, self.ms_sendImportantMessage, 'ms_sendImportantMessage')
            serviceRun(browser, self.ms_sendReservationMessage, 'ms_sendReservationMessage')
            serviceRun(browser, self.ms_resendMessage, 'ms_resendMessage')
            serviceRun(browser, self.ms_replyAllMessage, 'ms_replyAllMessage')
            serviceRun(browser, self.ms_replyMessage, 'ms_replyMessage')
            serviceRun(browser, self.ms_forwardMessage, 'ms_forwardMessage')
            serviceRun(browser, self.ms_readMessageAll, 'ms_readMessageAll')
            serviceRun(browser, self.ms_readSecurityMessage, 'ms_readSecurityMessage')
            serviceRun(browser, self.ms_searchMessage, 'ms_searchMessage')
            serviceRun(browser, self.ms_bookmark, 'ms_bookmark')
            serviceRun(browser, self.ms_deleteReceiveMessage, 'ms_deleteReceiveMessage')
            serviceRun(browser, self.ms_deleteSendMessage, 'ms_deleteSendMessage')
        else :
            print('메시지 확인')
        time.sleep(3)

class AccountsRun(wehagotest.Accounts) :
    def accounts (self, browser) :
        print("accounts s")
        browser.get(getUrl('accounts'))
        time.sleep(5)
        if browserTitle(browser, '거래처') :
            serviceRun(browser, self.ac_createGroup, 'ac_createGroup')
            serviceRun(browser, self.ac_registAccount, 'ac_registAccount')
            serviceRun(browser, self.ac_modifyAccount, 'ac_modifyAccount')
            serviceRun(browser, self.ac_deleteAccount, 'ac_deleteAccount')
            serviceRun(browser, self.ac_deleteGroup, 'ac_deleteGroup')
            serviceRun(browser, self.ac_createSharedGroup, 'ac_createSharedGroup')
            serviceRun(browser, self.ac_deleteSharedGroup, 'ac_deleteSharedGroup')
        else : 
            print('거래처 확인')
        time.sleep(3)

class ContactsRun(wehagotest.Contacts) :
    def contacts (self, browser) :
        print("contacts s")
        browser.get(getUrl('contacts'))
        time.sleep(5)
        if browserTitle(browser, '연락처') :
            serviceRun(browser, self.ct_deleteContact, 'ct_deleteContact')
            serviceRun(browser, self.ct_registerContacts, 'ct_registerContacts')
            serviceRun(browser, self.ct_createGroup, 'ct_createGroup')
            serviceRun(browser, self.ct_modifyGroup, 'ct_modifyGroup')
            serviceRun(browser, self.ct_deleteGroup, 'ct_deleteGroup')
            serviceRun(browser, self.ct_createSharedGroup, 'ct_createSharedGroup')
            serviceRun(browser, self.ct_deleteSharedGroup, 'ct_deleteSharedGroup')
            serviceRun(browser, self.ct_contactImport, 'ct_contactImport')
            serviceRun(browser, self.ct_organizeContact, 'ct_organizeContact')
        else : 
            print('연락처 확인')
        time.sleep(3)
 
class ScheduleRun(wehagotest.Schedule) :
    def schedule (self, browser) :
        print("schedule s")
        browser.get(getUrl('schedule'))
        time.sleep(5)
        if browserTitle(browser, '일정') :
            serviceRun(browser, self.sc_deleteSchedule, 'sc_deleteSchedule')
            serviceRun(browser, self.sc_createCalendar, 'sc_createCalendar')
            serviceRun(browser, self.sc_createSharedCalendar, 'sc_createSharedCalendar')
            serviceRun(browser, self.sc_modifyCalendar, 'sc_modifyCalendar')
            serviceRun(browser, self.sc_dragCalender, 'sc_dragCalender')
            serviceRun(browser, self.sc_deleteCalendar, 'sc_deleteCalendar')
            serviceRun(browser, self.sc_registerSchedule, 'sc_registerSchedule')
            serviceRun(browser, self.sc_addComment, 'sc_addComment')
            serviceRun(browser, self.sc_clickCalendar, 'sc_clickCalendar')
            serviceRun(browser, self.sc_searchSchedule, 'sc_searchSchedule')
        else : 
            print('일정 확인')
        time.sleep(3)

class MailRun(wehagotest.Mail) :
    def mail (self, browser) :
        print("mail s")
        browser.get(getUrl('mail'))
        time.sleep(5)
        if browserTitle(browser, '메일') :
            duplicatePopup = '//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div'
            text = browser.find_element_by_xpath(duplicatePopup).text
            if text == '권한이 없습니다.' :
                print('메일 권한 없음')
                browser.find_element_by_xpath('//*[@id="confirm"]').click()
            else :
                serviceRun(browser, self.ma_deleteMail, 'ma_deleteMail')
                serviceRun(browser, self.ma_emptyTrash, 'ma_emptyTrash')
                serviceRun(browser, self.ma_sendReservedMail, 'ma_sendReservedMail')
                serviceRun(browser, self.ma_sendSecureMail, 'ma_sendSecureMail')
                serviceRun(browser, self.ma_sendMail, 'ma_sendMail')
                serviceRun(browser, self.ma_sendMailWedrive, 'ma_sendMailWedrive')
                serviceRun(browser, self.ma_sendMailLocalWedrive, 'ma_sendMailLocalWedrive')
                serviceRun(browser, self.ma_temporarySave, 'ma_temporarySave')
                serviceRun(browser, self.ma_replyMailAll, 'ma_replyMailAll')
                serviceRun(browser, self.ma_replyMail, 'ma_replyMail')
                serviceRun(browser, self.ma_deliveryMail, 'ma_deliveryMail')
                serviceRun(browser, self.ma_automaticClassification, 'ma_automaticClassification')
                serviceRun(browser, self.ma_deleteAutomatic, 'ma_deleteAutomatic')
                # if wehagotest.wehagoBrand != 3 :
                #     serviceRun(browser, self.ma_addExternalMail, 'ma_addExternalMail')
                #     serviceRun(browser, self.ma_externalMailLinkEtc, 'ma_externalMailLinkEtc')
        else : 
            print('메일 확인')
        time.sleep(3)

class TodoRun(wehagotest.Todo) :
    def todo (self, browser) :
        print("todo s")
        browser.get(getUrl('todo', False))
        time.sleep(5)
        if browserTitle(browser, '할일') :
            serviceRun(browser, self.td_deleteProject, 'td_deleteProject')
            serviceRun(browser, self.td_createProject, 'td_createSharedProject')
            serviceRun(browser, self.td_modifyProject, 'td_modifyProject')
            serviceRun(browser, self.td_createBoard, 'td_createBoard')
            serviceRun(browser, self.td_deleteBoard, 'td_deleteBoard')
            serviceRun(browser, self.td_createTodo, 'td_createTodo')
            serviceRun(browser, self.td_addComment, 'td_addComment')
            serviceRun(browser, self.td_completeTodo, 'td_completeTodo')
            serviceRun(browser, self.td_searchTodo, 'td_searchTodo')
            serviceRun(browser, self.td_deleteTodo, 'td_deleteTodo')
        else : 
            print('할일 확인')
        time.sleep(3)

class WecrmRun(wehagotest.Wecrm) :
    def wecrm (self, browser) :
        # pms 삭제하고, crm 삭제하기
        serviceRun(browser, wehagotest.Wepms().pms_deleteProject, 'pms_deleteProject')
        print("WeCRM s")
        browser.get(getUrl('wecrm'))
        time.sleep(5)
        serviceRun(browser, self.crm_settingUnuse, 'crm_settingUnuse')
        serviceRun(browser, self.crm_settingUse, 'crm_settingUse')
        serviceRun(browser, self.crm_deleteSales, 'crm_deleteSales')
        serviceRun(browser, self.crm_deleteAccounts, 'crm_deleteAccounts')
        serviceRun(browser, self.crm_registerAccounts, 'crm_registerAccounts')
        serviceRun(browser, self.crm_registerOpportunity, 'crm_registerOpportunity')
        serviceRun(browser, self.crm_opportunity, 'crm_opportunity')
        serviceRun(browser, self.crm_registerGoods, 'crm_registerGoods')
        serviceRun(browser, self.crm_addContactPerson, 'crm_addContactPerson')
        serviceRun(browser, self.crm_deleteContactPerson, 'crm_deleteContactPerson')
        serviceRun(browser, self.crm_issueManagement, 'crm_issueManagement')
        serviceRun(browser, self.crm_addGoals, 'crm_addGoals')
        serviceRun(browser, self.crm_copyGoals, 'crm_copyGoals')
        serviceRun(browser, self.crm_delGoals, 'crm_delGoals')
        time.sleep(3)

    def wecrmSetting(self, browser) :
        browser.get(getUrl('wecrm'))
        time.sleep(5)
        serviceRun(browser, self.crm_basicset, 'crm_basicset')
        serviceRun(browser, self.crm_registerAccounts, 'crm_registerAccounts')

class WepmsRun(wehagotest.Wepms) :
    def wepms (self, browser) :
        print("Wepms s")
        browser.get(getUrl('wepms'))
        time.sleep(5)
        if browserTitle(browser, 'PMS') :
            # PMS 삭제는 user B 확인 후 삭제
            serviceRun(browser, self.pms_delBudgetExecution, 'pms_delBudgetExecution')
            serviceRun(browser, self.pms_delUse, 'pms_delUse')
            serviceRun(browser, self.pms_deleteProjectType, 'pms_deleteProjectType')
            serviceRun(browser, self.pms_settingUnuse, 'pms_settingUnuse')
            serviceRun(browser, self.pms_deleteProject, 'pms_deleteProject')
            serviceRun(browser, self.pms_settingUse, 'pms_settingUse')
            serviceRun(browser, self.pms_addUse, 'pms_addUse')
            serviceRun(browser, self.pms_addProjectType, 'pms_addProjectType')
            serviceRun(browser, self.pms_registerCrmProject_new, 'pms_registerCrmProject_new')
            serviceRun(browser, self.pms_registerExternalProject_new, 'pms_registerExternalProject_new')
            serviceRun(browser, self.pms_registerInternalProject_new, 'pms_registerInternalProject_new')
            serviceRun(browser, self.pms_registerCrmProject, 'pms_registerCrmProject')
            serviceRun(browser, self.pms_registerExternalProject, 'pms_registerExternalProject')
            serviceRun(browser, self.pms_registerInternalProject, 'pms_registerInternalProject')
            serviceRun(browser, self.pms_manpower, 'pms_manpower')
            serviceRun(browser, self.pms_schedulePlan, 'pms_schedulePlan')
            serviceRun(browser, self.pms_budget, 'pms_budget')
            serviceRun(browser, self.pms_budgetExecution, 'pms_budgetExecution')
            serviceRun(browser, self.pms_createIssue, 'pms_createIssue')
            serviceRun(browser, self.pms_usercreateIssue, 'pms_usercreateIssue')
            serviceRun(browser, self.pms_userProjectManamger, 'pms_userProjectManamger')
        else : 
            print('PMS 확인 ')
        time.sleep(3)

    def wepmsSetting(self, browser) :
        browser.get(getUrl('wepms'))
        time.sleep(5)
        serviceRun(browser, self.pms_basicset, 'pms_basicset')
    
class NoteRun(wehagotest.Note) :
    def note (self, browser) :
        print("note s")
        browser.get(getUrl('note', False))
        time.sleep(5)
        if browserTitle(browser, '노트') :
            serviceRun(browser, self.nt_createSharedSpace, 'nt_createSharedSpace')
            serviceRun(browser, self.nt_deleteSharedSpace, 'nt_deleteSharedSpace')
            serviceRun(browser, self.nt_createNote, 'nt_createNote')
            serviceRun(browser, self.nt_deleteNote, 'nt_deleteNote')
            serviceRun(browser, self.nt_emptyTrash, 'nt_emptyTrash')
        else : 
            print('노트 확인')
        time.sleep(3)

class AttendanceRun(wehagotest.Attendance) :
    def attendance (self, browser) :
        print("attendance s")
        browser.get(getUrl('attendance'))
        time.sleep(5)
        if browserTitle(browser, '근태관리') :
            serviceRun(browser, self.at_settingWorkingGroup, 'at_settingWorkingGroup')
            serviceRun(browser, self.at_assignmentWorkingGroup, 'at_assignmentWorkingGroup')
            serviceRun(browser, self.at_settingWorkingPlace, 'at_settingWorkingPlace')
            serviceRun(browser, self.at_assignmentWorkingPlace, 'at_assignmentWorkingPlace')
            serviceRun(browser, self.at_addAttendanceItem, 'at_addAttendanceItem')
            serviceRun(browser, self.at_deleteAttendanceItem, 'at_deleteAttendanceItem')
            serviceRun(browser, self.at_vacationApplication, 'at_vacationApplication')
            serviceRun(browser, self.at_vacationApplicationCancel, 'at_vacationApplicationCancel')
            serviceRun(browser, self.at_deleteWorkingGroup, 'at_deleteWorkingGroup')
            serviceRun(browser, self.at_deleteWorkingPlace, 'at_deleteWorkingPlace')
            # 현재 데이터 꼬여있어서 v일때 제외처리
            # if wehagotest.wehagoBrand != 3 :
            #     serviceRun(browser, self.at_registerholiday, 'at_registerholiday')
            #     serviceRun(browser, self.at_deleteHoliday, 'at_deleteHoliday')
            serviceRun(browser, self.at_authorization, 'at_authorization')
            serviceRun(browser, self.at_deauthorization, 'at_deauthorization')
        else :
            print('근태관리 확인')
        time.sleep(3)

    def attendanceSetting(self, browser) :
        browser.get(getUrl('attendance/settings/VacationSetting'))
        time.sleep(3)
        serviceRun(browser, self.at_settingVacation, 'at_settingVacation')

class CorporateCardRun(wehagotest.CorporateCard) :
    def corporateCard (self, browser) :
        print("CorporateCard s")
        browser.get(getUrl('expense'))
        time.sleep(5)
        if browserTitle(browser, '법인카드') :
            serviceRun(browser, self.cca_setAdminstor, 'cca_setAdminstor')
            serviceRun(browser, self.cca_unsetAdminstor, 'cca_unsetAdminstor')
            serviceRun(browser, self.cca_settingUse, 'cca_settingUse')
            serviceRun(browser, self.cca_scraping, 'cca_scraping')
            serviceRun(browser, self.cca_expenseClaim, 'cca_expenseClaim')
            serviceRun(browser, self.cca_requestApproval, 'cca_requestApproval')
            serviceRun(browser, self.cca_settingUnuse, 'cca_settingUnuse')
            if wehagotest.wehagoBrand != 3 :
                serviceRun(browser, self.ex_request, 'ex_request')
                serviceRun(browser, self.cca_expenseClaimRequest, 'cca_expenseClaimRequest')
            serviceRun(browser, self.ex_approve, 'ex_approve')
            serviceRun(browser, self.ex_approveCancel, 'ex_approveCancel')
            serviceRun(browser, self.ex_reject, 'ex_reject')
            serviceRun(browser, self.ex_rejectCancel, 'ex_rejectCancel')
            serviceRun(browser, self.cca_returnCard, 'cca_returnCard')
        else :
            print('법인카드 확인')
        time.sleep(3)

    def corporateCardSetting(self, browser) :
        browser.get(getUrl('expense'))
        time.sleep(5)
        if browserTitle(browser, '법인카드') :
            serviceRun(browser, self.cca_clause, 'cca_clause')
            serviceRun(browser, self.cca_cardRegist, 'cca_cardRegist')
        else :
            print('법인카드 확인')

class PersonalCardRun(wehagotest.PersonalCard) :
    def personalCard (self, browser) :
        print("PersonalCard s")
        browser.get(getUrl('expensepersonalcard'))
        time.sleep(5)
        if browserTitle(browser, '개인카드') :
            serviceRun(browser, self.pca_settingUse, 'pca_settingUse')
            serviceRun(browser, self.pca_scraping, 'pca_scraping')
            serviceRun(browser, self.pca_transmitExpenseClaim, 'pca_transmitExpenseClaim')
            serviceRun(browser, self.pca_excludeDetails, 'pca_excludeDetails')
            serviceRun(browser, self.pca_directInput, 'pca_directInput')
            serviceRun(browser, self.pca_expenseClaim, 'pca_expenseClaim')
            serviceRun(browser, self.pca_requestApproval, 'pca_requestApproval')
            serviceRun(browser, self.ex_request, 'ex_request')
            serviceRun(browser, self.pca_settingUnuse, 'pca_settingUnuse')
            serviceRun(browser, self.pca_expenseClaimRequest, 'pca_expenseClaimRequest')
            serviceRun(browser, self.ex_approve, 'ex_approve')
            serviceRun(browser, self.ex_approveCancel, 'ex_approveCancel')
            serviceRun(browser, self.ex_reject, 'ex_reject')
            serviceRun(browser, self.ex_rejectCancel, 'ex_rejectCancel')
        else :
            print('개인카드 확인')
        time.sleep(3)

    def personalCardSetting(self, browser) :
        browser.get(getUrl('expensepersonalcard'))
        time.sleep(5)
        if browserTitle(browser, '개인카드') :
            serviceRun(browser, self.pca_clause, 'pca_clause')
            serviceRun(browser, self.pca_addManager, 'pca_addManager')
            serviceRun(browser, self.pca_cardRegist, 'pca_cardRegist')
        else :
            print('개인카드 확인')

class ApprovalRun(wehagotest.Approval) :
    def approval (self, browser) :
        print("Approval s")
        browser.get(getUrl('eapprovals'))
        time.sleep(5)
        if browserTitle(browser, '전자결재') :
            serviceRun(browser, self.ap_deleteApprove, 'ap_deleteApprove')
            serviceRun(browser, self.ap_approval, 'ap_approval')
            serviceRun(browser, self.ap_reApproval, 'ap_reApproval')
            serviceRun(browser, self.ap_modifyApproval, 'ap_modifyApproval')
            serviceRun(browser, self.ap_createArchive, 'ap_createArchive')
            serviceRun(browser, self.ap_approveDocumentArchive, 'ap_approveDocumentArchive')
            serviceRun(browser, self.ap_moveDocumentArchive, 'ap_moveDocumentArchive')
            serviceRun(browser, self.ap_deleteArchive, 'ap_deleteArchive')
            serviceRun(browser, self.ap_approve, 'ap_approve')
            serviceRun(browser, self.ap_reject, 'ap_reject')
            serviceRun(browser, self.ap_enforcement, 'ap_enforcement')
            if wehagotest.wehagoBrand != 3 :
                serviceRun(browser, self.ap_postApproval, 'ap_postApproval')
            serviceRun(browser, self.ap_preApproval, 'ap_preApproval')
            serviceRun(browser, self.ap_addDocumentForm, 'ap_addDocumentForm')
            serviceRun(browser, self.ap_approvebyUser, 'ap_approvebyUser')
            serviceRun(browser, self.ap_rejectbyUser, 'ap_rejectbyUser')
            serviceRun(browser, self.ap_deleteDocumentForm, 'ap_deleteDocumentForm')
        else :
            print('전자결재 확인')
        time.sleep(3)

    def approvalSetting(self, browser) :
        browser.get(getUrl('eapprovals'))
        time.sleep(5)
        if browserTitle(browser, '전자결재') :
            serviceRun(browser, self.ap_basicset, 'ap_basicset')
            serviceRun(browser, self.ap_settingType, 'ap_approvalType')
        else : 
            print('전자결재 확인')

class WebuilderRun(wehagotest.Webuilder) :
    def webuilder(self, browser) :
        print('WEbuilder s')
        serviceRun(browser, self.wb_webuilder, 'wb_webuilder')

class InvoiceRun(wehagotest.InvoicePublish) :
    def invoice(self, browser) :
        print('Invoice s')
        browser.get(getUrl('invoice'))
        time.sleep(5)
        if browserTitle(browser, '전자세금계산서') :
            # 저장데이터 삭제
            serviceRun(browser, self.tax_todayDeleteBtn, 'tax_todayDeleteBtn')
            serviceRun(browser, self.tax_savedDeleteBtn, 'tax_savedDeleteBtn')

            # 세금계산서
            serviceRun(browser, self.tax_formTaxation, 'tax_formTaxation')
            serviceRun(browser, self.tax_formTaxationReverse, 'tax_formTaxationReverse')
            serviceRun(browser, self.tax_formListTaxSmall, 'tax_formListTaxSmall')
            serviceRun(browser, self.tax_formListTaxSmallReverse, 'tax_formListTaxSmallReverse')
            serviceRun(browser, self.tax_formDetailTaxFree, 'tax_formDetailTaxFree')
            serviceRun(browser, self.tax_formDetailTaxFreeReverse, 'tax_formDetailTaxFreeReverse')
            serviceRun(browser, self.tax_simpleTaxation, 'tax_simpleTaxation')
            serviceRun(browser, self.tax_simpleTaxationReverse, 'tax_simpleTaxationReverse')
            serviceRun(browser, self.tax_simpleListTaxSmall, 'tax_simpleListTaxSmall')
            serviceRun(browser, self.tax_simpleListTaxSmallReverse, 'tax_simpleListTaxSmallReverse')
            serviceRun(browser, self.tax_simpleDetailTaxFree, 'tax_simpleDetailTaxFree')
            serviceRun(browser, self.tax_simpleDetailTaxFreeReverse, 'tax_simpleDetailTaxFreeReverse')
            serviceRun(browser, self.tax_modifyInvoice_detail, 'tax_modifyInvoice_detail')
            serviceRun(browser, self.tax_modifyInvoice_list, 'tax_modifyInvoice_list')
            serviceRun(browser, self.tax_modifyInvoice_approval, 'tax_modifyInvoice_approval')

            # 거래명세서
            serviceRun(browser, self.tr_formTaxation, 'tr_formTaxation')
            serviceRun(browser, self.tr_formTaxationReverse, 'tr_formTaxationReverse')
            serviceRun(browser, self.tr_formListTaxSmall, 'tr_formListTaxSmall')
            serviceRun(browser, self.tr_formListTaxSmallReverse, 'tr_formListTaxSmallReverse')
            serviceRun(browser, self.tr_formDetailTaxFree, 'tr_formDetailTaxFree')
            serviceRun(browser, self.tr_formDetailTaxFreeReverse, 'tr_formDetailTaxFreeReverse')
            serviceRun(browser, self.tr_attachmentTaxation, 'tr_attachmentTaxation')
            serviceRun(browser, self.tr_attachmentTaxationReverse, 'tr_attachmentTaxationReverse')
            serviceRun(browser, self.tr_attachmentListTaxSmall, 'tr_attachmentListTaxSmall')
            serviceRun(browser, self.tr_attachmentListTaxSmallReverse, 'tr_attachmentListTaxSmallReverse')
            serviceRun(browser, self.tr_attachmentDetailTaxFree, 'tr_attachmentDetailTaxFree')
            serviceRun(browser, self.tr_attachmentDetailTaxFreeReverse, 'tr_attachmentDetailTaxFreeReverse')
            serviceRun(browser, self.tr_simpleTaxation, 'tr_simpleTaxation')
            serviceRun(browser, self.tr_simpleTaxationReverse, 'tr_simpleTaxationReverse')

            # 입금표
            serviceRun(browser, self.de_formPublish, 'de_formPublish')
            serviceRun(browser, self.de_listPublish, 'de_listPublish')
            serviceRun(browser, self.de_detailPublish, 'de_detailPublish')
            serviceRun(browser, self.de_simplePublish, 'de_simplePublish')

            # 영수증
            serviceRun(browser, self.re_formPublish, 're_formPublish')
            serviceRun(browser, self.re_listPublish, 're_listPublish')
            serviceRun(browser, self.re_detailPublish, 're_detailPublish')
            serviceRun(browser, self.re_simplePublish, 're_simplePublish')
            
            # 전자청구서
            serviceRun(browser, self.eb_formPublish, 'eb_formPublish')
            serviceRun(browser, self.eb_detailPublish, 'eb_detailPublish')
            serviceRun(browser, self.eb_simplePublish, 'eb_simplePublish')
            serviceRun(browser, self.eb_deleteEbill, 'eb_deleteEbill')
        else :
            print('전자세금계산서 확인')

    def invoiceUpdate(self, browser) :
        print('Invoice s')
        browser.get(getUrl('invoice'))
        time.sleep(3)
        if browserTitle(browser, '전자세금계산서') :
            # 세금계산서
            serviceRun(browser, self.tax_formTaxation, 'tax_formTaxation')
            serviceRun(browser, self.tax_formListTaxSmallReverse, 'tax_formListTaxSmallReverse')
            serviceRun(browser, self.tax_formDetailTaxFree, 'tax_formDetailTaxFree')
            serviceRun(browser, self.tax_simpleTaxationReverse, 'tax_simpleTaxationReverse')
            serviceRun(browser, self.tax_simpleListTaxSmall, 'tax_simpleListTaxSmall')
            serviceRun(browser, self.tax_simpleDetailTaxFreeReverse, 'tax_simpleDetailTaxFreeReverse')
            serviceRun(browser, self.tax_modifyInvoice_detail, 'tax_modifyInvoice_detail')
            serviceRun(browser, self.tax_modifyInvoice_list, 'tax_modifyInvoice_list')
            serviceRun(browser, self.tax_modifyInvoice_approval, 'tax_modifyInvoice_approval')

            # 거래명세서
            serviceRun(browser, self.tr_formTaxation, 'tr_formTaxation')
            serviceRun(browser, self.tr_formListTaxSmallReverse, 'tr_formListTaxSmallReverse')
            serviceRun(browser, self.tr_formDetailTaxFree, 'tr_formDetailTaxFree')
            serviceRun(browser, self.tr_attachmentTaxationReverse, 'tr_attachmentTaxationReverse')
            serviceRun(browser, self.tr_attachmentListTaxSmall, 'tr_attachmentListTaxSmall')
            serviceRun(browser, self.tr_attachmentDetailTaxFreeReverse, 'tr_attachmentDetailTaxFreeReverse')
            serviceRun(browser, self.tr_simpleTaxation, 'tr_simpleTaxation')
            serviceRun(browser, self.tr_simpleTaxationReverse, 'tr_simpleTaxationReverse')

            serviceRun(browser, self.de_formPublish, 'de_formPublish')
            serviceRun(browser, self.de_listPublish, 'de_listPublish')
            serviceRun(browser, self.re_detailPublish, 're_detailPublish')
            serviceRun(browser, self.re_simplePublish, 're_simplePublish')
        else :
            print('전자세금계산서 확인')

class MeetRun(wehagotest.Meet) :
    def meet(self, browser) :
        print('Meet s')
        browser.get(getUrl('wehagomeet', False))
        time.sleep(5)
        if browserTitle(browser, '화상회의') :
            serviceRun(browser, self.meet_createMeeting, 'meet_createMeeting', False)
            serviceRun(browser, self.meet_inviteMail, 'meet_inviteMail', False)
            serviceRun(browser, self.meet_chatting, 'meet_chatting', False)
            serviceRun(browser, self.meet_exportUser, 'meet_exportUser', False)
            serviceRun(browser, self.meet_documentShare, 'meet_documentShare', False)
            serviceRun(browser, self.meet_externalSharing, 'meet_externalSharing', False)
            serviceRun(browser, self.meet_createReservedMeeting, 'meet_createReservedMeeting')
            serviceRun(browser, self.meet_reservedList, 'meet_reservedList')
            serviceRun(browser, self.meet_modifyReservationMeeting, 'meet_modifyReservationMeeting')
            serviceRun(browser, self.meet_reservationcancel, 'meet_reservationcancel')
        else :
            print('화상회의 확인')

class FaxRun(wehagotest.Fax) :
    def fax(self, browser) :
        print('Fax s')
        browser.get(getUrl('fax'))
        time.sleep(5)
        if browserTitle(browser, '팩스') :
            serviceRun(browser, self.fax_deleteFax, 'fax_deleteFax')
            serviceRun(browser, self.fax_quickSendFax, 'fax_quickSendFax')
            # serviceRun(browser, self.fax_generalSendFax, 'fax_generalSendFax')
        else :
            print('팩스 확인')

class SmsRun(wehagotest.Sms) :
    def sms(self, browser) :
        print('sms s')
        browser.get(getUrl('sms'))
        time.sleep(5)
        serviceRun(browser, self.sms_sendText, 'sms_sendText')
        serviceRun(browser, self.sms_sendExcel, 'sms_sendExcel')
        serviceRun(browser, self.sms_sendIndividualText, 'sms_sendIndividualText')

class WeStudioRun(wehagotest.WeStudio) :
    def westudio(self, browser) :
        print('westudio s')
        browser.get('https://www.wehago.com/westudio')
        time.sleep(5)
        serviceRun(browser, self.ws_createChannel, 'ws_createChannel')
        serviceRun(browser, self.ws_checkChannel, 'ws_checkChannel')
        serviceRun(browser, self.ws_uploadVideo_upd, 'ws_uploadVideo_upd')
        serviceRun(browser, self.ws_uploadVideo_ch, 'ws_uploadVideo_ch')
        serviceRun(browser, self.ws_uploadVideoOption, 'ws_uploadVideoOption')
        serviceRun(browser, self.ws_checkOption, 'ws_checkOption')
        serviceRun(browser, self.ws_watchRecord, 'ws_watchRecord')
        serviceRun(browser, self.ws_uploadUrl_ch, 'ws_uploadUrl_ch')
        serviceRun(browser, self.ws_uploadUrl_upd, 'ws_uploadUrl_upd')
        serviceRun(browser, self.ws_modifyVideo, 'ws_modifyVideo')
        serviceRun(browser, self.ws_searchVideo, 'ws_searchVideo')
        serviceRun(browser, self.ws_researvedLive_ch, 'ws_researvedLive_ch')
        serviceRun(browser, self.ws_researvedLive_upd, 'ws_researvedLive_upd')
        serviceRun(browser, self.ws_changeReservation, 'ws_changeReservation')
        serviceRun(browser, self.ws_sharedVideo, 'ws_sharedVideo')
        serviceRun(browser, self.ws_addPlaylist, 'ws_addPlaylist')
        # serviceRun(browser, self.ws_deletePlaylist, 'ws_deletePlaylist')
        serviceRun(browser, self.ws_deleteVideo, 'ws_deleteVideo')
        serviceRun(browser, self.ws_deleteChannel, 'ws_deleteChannel')

class UserCheck(wehagotest.Other) :
    def userCheck(self, browser, version) :
        print('user B check')
        self.ot_login(browser, version)
        serviceRun(browser, self.ot_deleteNote, 'ot_deleteNote')
        serviceRun(browser, self.ot_deleteMail, 'ot_deleteMail')
        serviceRun(browser, self.ot_deleteMessage, 'ot_deleteMessage')
        serviceRun(browser, self.ot_checkUserCreateIssue, 'ot_checkUserCreateIssue')
        serviceRun(browser, self.ot_checkUserProjectManager, 'ot_checkUserProjectManager')
        serviceRun(browser, self.ot_checkPostApproval, 'ot_checkPostApproval')
        serviceRun(browser, self.ot_checkTodoAddBoard, 'ot_checkTodoAddBoard')
        serviceRun(browser, self.ot_checkTodoDeleteBoard, 'ot_checkTodoDeleteBoard')
        serviceRun(browser, self.ot_participationChat, 'ot_participationChat')
        serviceRun(browser, self.ot_addUserChat, 'ot_addUserChat')

class WebotRun(wehagotest.Webot) :
    def webot(self, browser) :
        print('webot s')
        guestbrowser = chromeBrowser()
        serviceRun(guestbrowser, self.wb_user, 'wb_user')
        serviceRun(browser, self.wb_counselorConnection, 'wb_counselorConnection')
        serviceRun(guestbrowser, self.wb_userSendMessage, 'wb_userSendMessage')
        serviceRun(browser, self.wb_counselorSendMessage, 'wb_counselorSendMessage')
        serviceRun(browser, self.wb_counselorSearch, 'wb_counselorSearch')
        serviceRun(browser, self.wb_counselorHolding, 'wb_counselorHolding')
        serviceRun(browser, self.wb_counselorClose, 'wb_counselorClose')
