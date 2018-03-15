from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import re
import os
import random
from operator import contains
from itertools import imap, repeat
import calendar
import csv

class ApplicationLibrary:
    
    def date_select(self,date):
        
        selenium = BuiltIn().get_library_instance('Selenium2Library')
        months = {'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June','7':'July','8':'August','9':'Septmeber','10':'October','11':'November','12':'December'}
        self.navigate_to_backward()
        string = str(date)
        if string.find('/')>0:
            values = string.split('/')
            print "Enter in to first condition"
        elif string.find('-')>0:
            values = string.split('-')
            print values
            print "Enter in to second condition"
        if int(values[0])> 31:
           print "date vaule is exceed"
        if int(values[1]) > 12:
           print "month value is exceed" 
        month = months.get(str(int(values[1])))
        print "month:"+str(month)
        year = values[2]
        print "year:"+str(year)
        value = values[0]
        print "value:"+str(value)
        status = self.navigate_to_required_month(month,year,value)
        print "Date Selection status:"+str(status)
        return status
        
    def navigate_to_required_month(self,month,year,value):
        
        selenium = BuiltIn().get_library_instance('Selenium2Library')
        count = int(selenium.get_matching_xpath_count("//div[@id='ui-datepicker-div']/div[contains(@class,'datepicker-group')]"))
        try:
            nextBtnEnableStatus = selenium._is_visible("//div[@id='ui-datepicker-div' and contains(@style,'display: block')]/div[contains(@class,'datepicker-group')]//div[contains(@class,'datepicker-header')]/a[@data-handler='next']")
            print "nextBtnEnableStatus:"+str(nextBtnEnableStatus)
        except:
            print "Exception Raise in next button"
            nextBtnEnableStatus = False
        for icount in range(1,count+1):
            monthValue = selenium.get_text("//div[@id='ui-datepicker-div']/div[contains(@class,'datepicker-group')]["+str(icount)+"]/div[contains(@class,'datepicker-header')]//span[@class='ui-datepicker-month']")
            if monthValue.strip() == month:
               yearValue = selenium.get_text("//div[@id='ui-datepicker-div']/div[contains(@class,'datepicker-group')]["+str(icount)+"]/div[contains(@class,'datepicker-header')]//span[@class='ui-datepicker-year']")
               if yearValue.strip() == year:
                   try:
                       status = selenium._is_visible("//div[@id='ui-datepicker-div' and contains(@style,'display: block')]/div[contains(@class,'datepicker-group')]["+str(icount)+"]/table[@class='ui-datepicker-calendar']//td[contains(@class,'state-disabled')]/span[text()='"+str(value)+"']")
                       
                   except:
                        status = False
                   
                   if status!= True:
                       try:
                           status = selenium._is_visible("//div[@id='ui-datepicker-div' and contains(@style,'display: block')]/div[contains(@class,'datepicker-group')]["+str(icount)+"]/table[@class='ui-datepicker-calendar']//td[not(contains(@class,'state-disabled'))]/a[text()='"+str(value)+"']")
                       except:
                            status = False
                       if status:
                           selenium.click_element("//div[@id='ui-datepicker-div' and contains(@style,'display: block')]/div[contains(@class,'datepicker-group')]["+str(icount)+"]/table[@class='ui-datepicker-calendar']//td[not(contains(@class,'state-disabled'))]/a[text()='"+str(value)+"']")
                           print "date is selected"
                           time.sleep(5)
                           return True
                       else:
                            print "May be you selected month "+str(month)+" doesn't have "+str(value)+"OR given date value is past date."
               elif icount == count and nextBtnEnableStatus != True:
                   print "Please pass the correct year,Given year is: "+str(year)
                   return False
            elif icount == count and nextBtnEnableStatus != True:
                print "Please pass the correct month" +str(month)+"and year "+str(year)
                return False
            elif icount == count and nextBtnEnableStatus == True:
                print "enter in to condional block to click next button"
                selenium.click_element("//div[@id='ui-datepicker-div' and contains(@style,'display: block')]/div[contains(@class,'datepicker-group')]//div[contains(@class,'datepicker-header')]/a[@data-handler='next']")
                time.sleep(5)
                return self.navigate_to_required_month(month,year,value)

    def navigate_to_backward(self):
        
        selenium = BuiltIn().get_library_instance('Selenium2Library')
        print "navigate_to_backward keyword called"
        try:
            prevBtnEnableStatus = selenium._is_visible("//div[@id='ui-datepicker-div' and contains(@style,'display: block')]/div[contains(@class,'datepicker-group')]//div[contains(@class,'datepicker-header')]/a[@data-handler='prev']")
        except:
            prevBtnEnableStatus = False
            print "prevBtnEnableStatus"
        if prevBtnEnableStatus:
            selenium.click_element("//div[@id='ui-datepicker-div' and contains(@style,'display: block')]/div[contains(@class,'datepicker-group')]//div[contains(@class,'datepicker-header')]/a[@data-handler='prev']")
            time.sleep(5)
            self.navigate_to_backward()
        else:
            print "Navigate to backward done successfully"
