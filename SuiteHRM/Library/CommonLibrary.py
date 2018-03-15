from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os
import random
from operator import contains
from itertools import imap, repeat
import calendar
import csv
import win32clipboard
from pytz import timezone
import pytz
import calendar
from datetime import datetime, time, date
from datetime import datetime
from datetime import date
from dateutil.parser import parse
import datetime
import socket
import string
import xlrd
import collections
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from sys import exit
from random import randint

class CommonLibrary:
                
                def __init__(self):
                        pass
    
                def get_unique_id(self,value=None):
                    """Returns Unique Value by adding Time Stamp
                    """
                    if (value == None or value == ''):
                        return str(time.localtime().tm_year)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)
                    else:
                        return str(value)+str(time.localtime().tm_sec)+str(int(round(time.time() * 1000)))[-2:] + str(random.randint(int(0000),int(9999)))

                def get_time_stamp(self,timezoneName='EST5EDT'):
                    """Returns the Current Date and Time
                    """
                    return datetime.datetime.now(timezone(str(timezoneName))).strftime('%a %m/%d/%Y %I:%M %p')
                
                def close_alert_message(self):
                    """Returns 'True'if any alert message displayed returns 'False' if not"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        selenium.get_alert_message()
                        return True
                    except:
                        return False


                def click_element_using_javascript(self,locator,n=1):
                    """Returns 'True' if the element clciking by Java Script with the 'locator' in the corresponding page else returns 'False' """

                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        elements = selenium._element_find(locator,False,True)
                        selenium._current_browser().execute_script("arguments[0].click();", elements[n-1])
                        return True
                    except Exception as exp:
                        print "not clcikable by JS, "+ str(exp)
                        return False
                
                def get_ip_address(self):
                    """It returns system IP address"""
                    return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
                                
                def verify_element_present(self,locator):
                    """Returns 'True' if the element found with the 'locator' in the corresponding page else returns 'False'
                    """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        bStatus = selenium._is_element_present(locator)
                        if(str(bStatus) != str(True)) and (str(BuiltIn().get_variable_value("${BROWSER}"))!="ie"):
                            selenium.capture_page_screenshot()
                        return bStatus
                    except:
                        print "Got Exception"
                        return True

                def wait_for_element_present(self,locator,timeout=None):
                    """Returns 'True' if the element present with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,3):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locator,timeout)
                            return True
                        except:
                            print "ValueError: Element locator "+str(locator) +" did not visible within "+str(timeout) +" time out"
                            print "locator: "+str(locator)
                    return False

                def wait_for_element_not_present(self,locator,timeout=None):
                    """Returns 'True' if the element not present with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    if(timeout == None):
                        timeout = "5s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,10):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_for_element_invisible(locator,"5s")
                            
                        except:
                            print "exception : element is not present"
                            return True
                    return False

                def verify_element_visible(self,locator):
                    """Returns 'True' if the element visible with the 'locator' in the corresponding page else returns 'False'
                    """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,3):
                        try:
                            bStatus = selenium._is_visible(locator)
                            if(str(bStatus) != str(True)) and (str(BuiltIn().get_variable_value("${BROWSER}"))!="ie"):
                                selenium.capture_page_screenshot()
                            return bStatus
                        except:
                            print "Got exception"
                    return False
                
                def wait_for_element_visible(self,locator,timeout=None,messgae=''):
                    """Returns 'True' if the element visible with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,3):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locator,timeout)
                            selenium.wait_until_element_is_visible(locator,timeout)
                            return True
                        except:
                            if(len(messgae)>0):
                                print "Error Message:" +str(messgae)
                            print "ValueError: Element locator "+str(locator) +" did not visible within "+str(timeout) +" time out"
                            print "locator: "+str(locator)
                    return False

                def wait_for_element_invisible(self,locator,timeout=None):
                    """Returns 'True' if the element invisible with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    if(timeout == None):
                        timeout = "3s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,20):
                        print "iCounter: "+str(iCounter)
                        try:
                            time.sleep(3)
                            selenium.wait_until_page_contains_element(locator,timeout)
                            selenium.wait_until_element_is_visible(locator,timeout)
                        except:
                            print "exception : element is not visible"
                            return True
                    return False

                def get_text(self,locator,timeout=None):
                    """Returns the element visible text values other wise keyword will fail with proper reason """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    textVal = ""
                    bStatus = self.wait_for_element_visible(locator,timeout)
                    for iCounter in range(1,10):
                        print "get_text iCounter: "+str(iCounter)
                        if bStatus==False:
                            break
                        try:
                            textVal = selenium.get_text(locator)
                            print "textVal="+str(textVal)
                            return textVal
                        except:
                            print "Unable get text"
                    raise AssertionError("Unable to get text from specified locator locator= "+str(locator))

                def mouse_scrolling(self,locator,timeout=None):
                    """Returns the element visible text values other wise keyword will fail with proper reason """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = self.wait_for_element_visible(locator,timeout)
                    if bStatus==False:
                        return False
                    for iCounter in range(1,5):
                        print "mouse_scrolling iCounter: "+str(iCounter)
                        try:
                            textVal = selenium.mouse_scroll(locator)
                            return True
                        except:
                            print "Unable do scrolling"
                    raise AssertionError("Unable perform mouse scroll on specified locator locator= "+str(locator))


                def enter_text(self,locator,inputValue,timeout=None):
                    """It will enter the specified value into the specifies text field  """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    textVal = ""
                    bStatus = self.wait_for_element_visible(locator,timeout)
                    for iCounter in range(1,10):
                        print "enter text: iCounter: "+str(iCounter)
                        if bStatus==False:
                            break
                        try:
                            textVal = selenium.input_text(locator,inputValue)
                            print "textVal="+str(textVal)
                            return textVal
                        except:
                            print "Unable get text"
                            time.sleep(1)
                    raise AssertionError("Unable to enter text into the specified field vased locator ,locator= "+str(locator))


                def get_element_attribute_value(self,locator,timeout=None):
                    """Returns the element attribute values """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    attVal = None
                    locator = str(locator)
                    print "locator="+str(locator)
                    elementlocator = locator[0:int(locator.rfind("@"))]
                    try:
                        selenium.wait_until_page_contains_element(elementlocator,timeout)
                        bStatus = True
                    except:
                        print "element not present"
                        bStatus = False
                    for iCounter in range(1,6):
                        print "get_element_attribute iCounter: "+str(iCounter)
                        if bStatus==False:
                            break
                        try:
                            attVal = selenium.get_element_attribute(locator)
                            print "attVal="+str(attVal)
                            return attVal
                        except:
                            print "Unable get text"
                    raise AssertionError("Unable get element attribute value ,locator= "+str(locator))


                def wait_for_dropdown_selection(self,locatorxpath,listVal,timeout=None):
                    """This keyword will wait upto selection was done  and return the True or False"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if(timeout == None):
                        timeout = "20s"
                    for iCounter in range(1,3):
                        print "wait_for_dropdown_selection iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locatorxpath+"/option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            selenium.wait_until_element_is_visible(locatorxpath+"/option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            return True
                        except:
                            print "drop down option was not selected within "+str(timeout) +" time out"
                            print "locator: "+str(locatorxpath)
                        
                        try:
                            selenium.wait_until_page_contains_element(locatorxpath+"//option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            selenium.wait_until_element_is_visible(locatorxpath+"//option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            return True
                        except:
                            print "drop down option was not selected within "+str(timeout) +" time out"
                            print "locator: "+str(locatorxpath)
                    return False
                
                def is_digit(self,string):
                    """ Returns True if passed argument is a digit"""
                    return string.isdigit()
                
                def list_comparison(self, li_actual, li_expected,message=''):
                    """ Takes Two lists as Arguments and Pass if the two lists are equal else Fails"""
                    print 'Expected: %s\n' % str(li_expected)
                    print 'Actual: %s' % str(li_actual)
                    if li_actual == []:
                        raise AssertionError('Actual is empty')                    
                    for index in range(0,len(li_expected)):
                        if li_expected[index] in li_actual:
                            continue
                        for actualIndex in range(0,len(li_actual)):
                            if li_expected[index][:14] in li_actual[actualIndex]:
                                break
                        else:
                            raise AssertionError('Actual does not match expected'+str(message))
                
                def list_difference(self, li_actual, li_expected):
                    """Takes Two lists as arguments and returns a list containing the difference of the two lists"""
                    return list(set(li_expected).difference(set(li_actual)))    
                             
                def list_comparison_partially(self,li_actual, li_expected):
                    """ Takes Two lists as Arguments and Pass if the two lists are equal else Fails"""
                    print 'Expected: %s\n' % str(li_expected)
                    print 'Actual: %s' % str(li_actual)
                    if li_actual == []:
                        raise AssertionError('Actual is empty')                    
                    
                    if len(li_actual)==len(li_expected):
                        for index in range(0,len(li_actual)):
                            element1=li_actual[index].lower()
                            element2=li_expected[index].lower()
                            if not (element2.find(element1)>=0 or element1.find(element2))>=0:
                                print "error "
                                return False
                    else:
                        print "len vals not same"
                        return False
                    return True

                def partial_value_count_in_list(self,list_actual, item):
                    """ It will return count of value in the specified values"""
                    print 'Expected val ' +str(item)
                    print 'Actual: %s' % str(list_actual)
                    intCount = 0
                    for index in range(0,len(list_actual)):
                        element1=list_actual[index].lower()
                        if element1.find(item)>=0:
                            intCount = intCount +1
                    return intCount

                def type_keys_into_textbox(self, text_locator,value):
                    """Enters text 'value' into 'text_locator' after checking the presence of the locator"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCnt in range(0,4):
                        try:
                            selenium.wait_until_page_contains_element(text_locator)
                            selenium._element_find(text_locator,True,True).send_keys(value)
                            return True
                        except:
                            time.sleep(3)
                            print "got exception"
                    return False
                
                def mouse_move(self, locator):
                    """Moves the Mouse to the 'locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium.mouse_over(locator)
                    
                def wait_for_ajax(self,time_out=5):
                    """ Wailt for given time"""
                    '''selenium = BuiltIn().get_library_instance('Selenium2Library')
                    status = selenium._selenium.get_eval('(window.jQuery || { active : 0 }).active')
                    print status'''
                    timeout = 0
                    while(timeout<time_out):
                        '''status = selenium._selenium.get_eval('(window.jQuery || { active : 0 }).active')
                        if(status):
                            return True'''
                        time.sleep(1)
                        timeout=timeout+1
                    return True
                                                  
                def input_file_name(self,locator,value):
                    """Enters the 'value' into the field located by 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator)
                    selenium._element_find(locator,True,True).send_keys(value)
                    return True
                
                def get_current_date(self,timezoneName="EST5EDT"):
                    """ Returns the current date in the format month date year"""
                    if timezoneName==None:
                        cdate = datetime.datetime.now()
                        cdate = cdate.strftime("%m/%d/%Y")
                    else:
                        cdate = datetime.datetime.now(timezone(str(timezoneName))).strftime('%m/%d/%Y')
                    return cdate

                def get_from_date(self, fromDate,timezoneName='EST5EDT'):
                    """Substracts the days from the current date to get the From date"""
                    cdate = datetime.datetime.now(timezone(str(timezoneName)))
                    fromdate = cdate - datetime.timedelta(days=int(fromDate))
                    return fromdate.strftime("%m/%d/%Y")

                def get_last_week_last_date(self,timezoneName="EST5EDT"):
                    """Returns the Last week last date to compare with the To date after selecting the Date dropdown item 'Previous Week'"""
                    cdate = datetime.datetime.now(timezone(str(timezoneName)))
                    print "cdate: "+str(cdate)
                    lastweeklastday = datetime.datetime.now(timezone(str(timezoneName))).weekday()
                    if int(lastweeklastday)==6:
                        lastweeklastday = 1
                    else:
                        lastweeklastday = lastweeklastday + 2
                    lastday = cdate - datetime.timedelta(days=int(lastweeklastday))
                    return lastday.strftime("%m/%d/%Y")
                    
                def get_last_week_first_date(self,timezoneName="EST5EDT"):
                    """Returns the Last week first date to compare with the From date after selecting the Date dropdown item 'Previous Week'"""
                    cdate = datetime.datetime.now(timezone(str(timezoneName)))
                    lastweeklastday = datetime.datetime.now(timezone(str(timezoneName))).weekday()
                    if int(lastweeklastday)==6:
                        lastweeklastday = 7
                    else:
                        lastweeklastday = lastweeklastday + 8
                    firstday = cdate - datetime.timedelta(days=int(lastweeklastday))
                    return firstday.strftime("%m/%d/%Y")

                def get_last_month_last_date(self,timezoneName="EST5EDT"):
                    """Returns the Last month last date to compare with the To date after selecting the Date dropdown item 'Previous Month'"""
                    first_day_of_current_month = datetime.datetime.now(timezone(str(timezoneName))).today().replace(day=1)
                    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
                    return last_day_of_previous_month.strftime("%m/%d/%Y")

                def get_last_month_first_date(self,timezoneName="EST5EDT"):
                    """Returns the Last Month first date to compare with the From date after selecting the Date dropdown item 'Previous Month'"""
                    first_day_of_current_month = datetime.datetime.now(timezone(str(timezoneName))).today().replace(day=1)
                    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
                    first_day_of_last_month = datetime.date(day=1, month= last_day_of_previous_month.month, year= last_day_of_previous_month.year)
                    return first_day_of_last_month.strftime("%m/%d/%Y")

                def get_timezone_from_date(self,timezone):
                    """Returns the Time zone from the 'timezone'"""
                    words = timezone.split()
                    splitleft = words[1].split("(")
                    splitright = splitleft[1].split(")")
                    return splitright[0]
                
                def delete_space(self,word):
                    """deletes an undesired spce from the 'word' and returns the word """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    words = str(word)
                    deletespace = words.replace(' ','')
                    return deletespace
                              
                def change_date_format(Self, date):
                    """ Returns a date after changing its format from 'month/date/year' to 'Year month date'"""
                    #date = date.replace('/',",")
                    return datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y,%m,%d')
                
                def compare_dates_for_given_range(self, date1, date2):
                    """ Returns True if the 'date1' is less than 'date2' else fails"""
                    date1 = self.change_date_format(str(date1))
                    date2 = self.change_date_format(str(date2))
                    return datetime.date(date1)<datetime.date(date2)
                
                def list_comp_by_sequence(self, actualList,expectedList):
                    """Takes lists 'actualList' and 'expectedList'as arguments and compares them in the sequence """
                    if cmp(actualList,expectedList)!=0:
                        return False
                    return True
                
                def get_length_of_list(self, actuallist):
                    """Takes the list 'actuallist' as argument and finds the length of the list. Fails if the length of the list equal to Zero""" 
                    if len(actuallist)==0:
                        raise AssertionError('Actual is empty')
                    return len(actuallist)
                               
                def get_sum_of_values_in_list(self, actuallist):
                    """Takes a list 'actualList' containing float values as argument and returns the sum of the list items"""
                    sum = 0
                    for index in range(0,len(actuallist)):
                        val = actuallist[int(index)]
                        print val
                        if val=="":
                            continue
                        sum = sum + int(val)
                    return sum
                
                def get_sum_of_float_values_in_list(self, actuallist):
                    """Takes a list 'actualList' containing float values as argument and returns the sum of the list items"""
                    sum = 0
                    for index in range(0,len(actuallist)):
                        val = actuallist[int(index)]
                        if val=="":
                            continue
                        sum = sum +float(val)
                    return round(sum, 2)

                def clear_text(self,locator):
                    """Clears Text From the field located by 'locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium._element_find(locator,True,True).clear()
                                                                    
                def get_sorted_list(self, actualList):
                    """Returns the sorted list by taking a list 'actualList' as argument"""
                    for iCounter in range(0,len(actualList)-1):
                        print "forloop"
                        if (int(actualList[iCounter]) > int(actualList[iCounter+1])):
                            print "ifloop"
                            print "actualList[iCounter]:"+str(actualList[iCounter])
                            print "actualList[iCounter+1]:"+str(actualList[iCounter+1])
                            temp = actualList[iCounter]
                            actualList[iCounter] = actualList[iCounter+1]
                            actualList[iCounter+1] = temp
                        print actualList
                    return actualList
                
                def sort_list_for_strings(self, actualList):
                    """Returns String values into a list in sorted order"""
                    if len(actualList)==0:
                        return 0
                    return sorted(actualList)

                def sort_list_for_integers(self, actualList):
                    """Returns integer values into a list in sorted order"""
                    if len(actualList)==0:
                        return 0
                    return sorted(actualList,key=int)
                
                def reverse_list_for_integers(self, actualList):
                    """Returns integer values into a list in reverse sorted order"""
                    if len(actualList)==0:
                        return 0
                    return sorted(actualList,key=int,reverse=True)

                def reverse_list_for_strings(self, actualList):
                    """Returns String values into a list in reverse sorted order"""
                    if len(actualList)==0:
                        return 0
                    return sorted(actualList,reverse=True)
                
                def get_float_values_in_sorted_list(self, actualList):
                    """Returns float values into a list in sorted order"""
                    return sorted(actualList,key=float)

                def get_float_values_in_reverse_sorted_list(self, actualList):
                    """Returns float values into a list in Reverse sorted order"""
                    print actualList
                    print ".................."
                    print sorted(actualList,key=float,reverse=True)
                    return sorted(actualList,key=float,reverse=True)
                
                def get_values_in_reverse_sort(self, actualList):
                    """Takes a list 'actualList' as an argument and returns the list in reverse sort"""
                    for iCounter in range(len(actualList)-1,0):
                        if (int(actualList[iCounter]) > int(actualList[iCounter+1])):
                            print "actualList[iCounter]:"+str(actualList[iCounter])
                            print "actualList[iCounter+1]:"+str(actualList[iCounter+1])
                            temp = actualList[iCounter]
                            actualList[iCounter] = actualList[iCounter+1]
                            actualList[iCounter+1] = temp
                    print actualList
                    return actualList
                
                def get_float_values_in_reverse_sort(self, actualList):
                    """Returns float values into a list in reverse sorted order"""
                    return sorted(actualList,key=float,reverse=True)

                def string_should_contain(self,string,substring):
                    """Returns True if The string contains substring else False' """
                    ind=string.find(substring)
                    print ind
                    if ind>=0:
                        return True
                    return False

                def string_should_contain_any_of_elements_in_the_list(self,mainString,elementsOfList):
                    """returns true if any one element in the list is the substring of the string"""
                    for i in elementsOfList:
                        if i in mainString:
                            print str(i)
                            return True
                    return False
                             
                def press_down_key(self,locator):
                    """ Presses the down Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium._element_find(locator,True,True).send_keys(Keys.ARROW_DOWN)
                    
                def press_control_and_key(self,locator,key):
                    """Presses the control Key and Specified key 'key' at element located by the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    loc = selenium._element_find(locator,True,True)
                    loc.send_keys(Keys.CONTROL, 'a')
                    time.sleep(1)
                    loc.send_keys(Keys.CONTROL,key)
                    time.sleep(1)
                    
                def press_up_key(self,locator):
                    """Presses the Up Key at element located by the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.ARROW_UP)
                            return True
                        except:
                            print "Exception in press_up_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_up_key")

                def press_page_down_key(self,locator):
                    """Presses the page down Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.PAGE_DOWN)
                            return True
                        except:
                            print "Exception in press_page_down_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_page_down_key")


                def press_page_up_key(self,locator):
                    """Presses the page up Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.PAGE_UP)
                            return True
                        except:
                            print "Exception in press_page_up_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_page_up_key")

                def press_home_key(self,locator):
                    """Presses the Home Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.HOME)
                            return True
                        except:
                            print "Exception in press_home_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_home_key")

                def press_end_key(self,locator):
                    """Presses the End Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.END)
                            return True
                        except:
                            print "Exception in press_end_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_end_key")

                def press_tab_key(self,locator):
                    """Presses the End Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.TAB)
                            return True
                        except:
                            print "Exception in press_tab_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_tab_key")
                
                def get_csv_file_row_values_into_list(self,path,rowNo):
                    """Returns the list of specified row values from cvs file in Specified File by 'path' """
                    file_Reader = csv.reader(open(path))
                    rowNumber=0
                    lines=[]
                    for row in file_Reader:
                        rowNumber=rowNumber+1
                        if rowNumber==int(rowNo):
                            lines=row
                            break

                    return lines

                def get_csv_file_column_no(self,path,columnname):
                    """Returns the column of specified column by  columnname from cvs file in Specified File by 'path' """
                    file_Reader = csv.reader(open(path))
                    linevalues=[]
                    print "text01"
                    for row in file_Reader:
                        linevalues=row
                        break
                    for index in range(0,len(linevalues)):
                        print "index="+str(index)
                        if len(linevalues)>0:
                            if linevalues[index]==columnname:
                                return index+1
                    return 0

                def get_csv_file_column_values_into_list(self,path,columnname):
                    """Returns the list of specified columns values from cvs file in Specified File by 'path' """
                    print "kw01"
                    keyColno=self.get_csv_file_column_no(path,columnname)
                    keyColno=int(keyColno)-1
                    file_Reader = csv.reader(open(path))
                    rowNumber=0
                    lines=[]
                    columnValues=[]
                    for row in file_Reader:
                        rowNumber=rowNumber+1
                        if rowNumber>1:
                            lines=row
                            try:
                                val= lines[keyColno]
                                print val
                                val = str(val).strip()
                                columnValues.append()
                            except:
                                print "Empty row found"
                                #columnValues.append("")
                    return columnValues

                def get_csv_file_rows_count(self,path):
                    """Return The Total No Rows In Csv File Using The Specified File Path"""
                    file_Reader = csv.reader(open(path))
                    rowsCount=sum(1 for row in file_Reader)
                    return  rowsCount
                
                def clear_clipboard_content(self):
                    """ clears the clipboard content """
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    
                def get_clipboard_content(self):
                    """ Returns the clipboard content """
                    win32clipboard.OpenClipboard()
                    print "clipboard content:"
                    return win32clipboard.GetClipboardData()

                def is_list_contains_value(self,statuslist,value):
                    """ checks the given value in the list """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    statuslistvalues = []
                    statuslistvalues = statuslist
                    return value in statuslistvalues

                def get_random_number_in_given_range(self,start,stop):
                    """ Returns the random from given range"""
                    return random.randint(int(start),int(stop))

                
                def get_unique_string(self,name =None):
                    """ Returns the random from given size"""
                    if name == None:
                        return  'Test'+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+str(time.localtime().tm_year)+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)
                    else:
                        return  str(name)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+str(time.localtime().tm_year)+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)
                                       
                def _isSorted(self, list_items):
                    """  checks the given list is sorted or not """
                    expectedListItems = sorted(list_items)
                    if expectedListItems==list_items:
                        return True

                def days_between(self,d1,d2):
                    d1 = datetime.datetime.strptime(d1, "%m/%d/%Y")
                    d2 = datetime.datetime.strptime(d2, "%m/%d/%Y")
                    return abs((d2 - d1).days)
              
                def get_current_time(self):
                    """Returns current time with date"""
                    ts = time.time()
                    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    return timestamp
    
                def date_sorting(self,actuallist):
                    datelist=[]
                    datelist1=[]
                    for index in range(len(actuallist)):
                        date=datetime.datetime.strptime(actuallist[index], '%m/%d/%Y').strftime('%Y-%m-%d')
                        datelist.append(date)
                    datesort=sorted(datelist)
                    for index in range(len(datesort)):
                        date1=datetime.datetime.strptime(datesort[index], '%Y-%m-%d').strftime('%m/%d/%Y')
                        datelist1.append(date1)
                    return datelist1

                def reverse_date_sorting(self,actuallist):
                    datelist=[]
                    datelist1=[]
                    for index in range(len(actuallist)):
                        date=datetime.datetime.strptime(actuallist[index], '%m/%d/%Y').strftime('%Y-%m-%d')
                        datelist.append(date)
                    datesort=sorted(datelist,reverse=True)
                    for index in range(len(datesort)):
                        date1=datetime.datetime.strptime(datesort[index], '%Y-%m-%d').strftime('%m/%d/%Y')
                        datelist1.append(date1)
                    return datelist1

                def is_list_contains_value(self,listofvals,value):
                    '''Returns True if the "value" found from the list "listofvals" else False'''
                    listofvals = []
                    listofvals = listofvals
                    if value in listofvals:
                        return True
                    else:
                        return False                
                       
                def click_element_and_check_expected_element(self,element_locator1,element_locator2=None):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "element_locator1: "+ str(element_locator1)
                    print "element_locator2: "+ str(element_locator2)
                    for iCounter in range(1,5):
                        try:
                            self.wait_for_element_visible(element_locator1)
                            selenium.click_element(element_locator1)
                            time.sleep(2)
                            if element_locator2==None:
                                return True
                        except:
                            print "element exception"
                        bStatus = self.wait_for_element_visible(element_locator2)
                        if bStatus == True:
                            print "expected element was visible"
                            return bStatus
                        else:
                            print "expected element was not visible"
                    return bStatus

                def wait_and_click_element(self,element_locator1,timeOut=None):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    if timeOut == None:
                        timeOut = "5s"
                    print "element_locator: "+ str(element_locator1)
                    for iCounter in range(1,5):
                        try:
                            bStatus = self.wait_for_element_visible(element_locator1,timeOut)
                            if bStatus==True:
                                selenium.click_element(element_locator1)
                                return True
                            else:
                                continue
                        except:
                            print "element exception"
                    return bStatus
                              
                def wait_for_ajax_call(self):
                    """ Wailt for given time  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')

                    jscript = "return jQuery.active"
                    print jscript
                    
                    for iIndex in range(1,6):
                        try:
                            print int(selenium.execute_javascript(jscript))
                        except:
                            print "exception while reading jQuery.active"
                        try:
                            print int(selenium.execute_javascript("Ajax.activeRequestCount"))
                        except:
                            print "exception while reading Ajax.activeRequestCount"
                
                def mouse_over_on_element(self,actlocator,explocator=None):
                    """Hovering mouse on the actlocator and verify the explocator visiblity"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bstatus=(explocator==None)
                    kwstatus = False
                    for counter1 in range(1,10):
                        try:
                            self.wait_for_element_visible(actlocator)
                            selenium.mouse_over(actlocator)
                            time.sleep(1)
                            if bstatus==True:
                                return True
                            if bstatus==False:
                                expelestatus=self.verify_element_visible(explocator)
                            if expelestatus==True:
                                return True
                        except:
                            print "mouse_over_on_element keyword failed"
                    return kwstatus
                          
                def wait_for_new_window(self,expectedCount=2,timeout=None):
                    """Wait for expected number of windows to be opened"""
                    if (timeout==None or timeout!=None or timeout==''):
                        timeout=5                    
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for icount in range(10):
                        try:
                            windows=selenium.get_window_titles()
                            count=len(windows)
                            if(int(count)==int(expectedCount)):
                                print "window names are"
                                print windows
                                return True
                            else:
                                print "expected window not opened"
                                time.sleep(timeout)
                        except:
                            print "exception occured"
                    return False
                
                def get_value_of_locator(self,locator):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCount in range(10):
                        try:
                            print "iteration count is "+str(iCount)
                            value=selenium.get_value(locator)
                            if(len(value)!=0):
                                return value
                        except:
                            print "Exception occured"

                def drag_and_drop_action(self, source, target):
                    """Drags element identified with `source` which is a locator.
                    Element can be moved on top of another element with `target`argument.
                    `target` is a locator of the element where the dragged object is dropped.
                    Examples:
                        | Drag And Drop | elem1 | elem2 | # Move elem1 over elem2. |"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')   
                    try:
                        src_elem = selenium._element_find(source,True,True)
                        trg_elem =  selenium._element_find(target,True,True)
                        ActionChains(selenium._current_browser()).drag_and_drop(src_elem, trg_elem).perform()
                    except:
                        print "exception occured"
                        src_elem = selenium._element_find(source,True,True)
                        trg_elem =  selenium._element_find(target,True,True)
                        ActionChains(selenium._current_browser()).drag_and_drop(src_elem, trg_elem).perform()
                               
                def mouse_down_and_mouse_up(self,locator,timeout="10s"):
                    """It will perform mouse down and up on specified element based  locator """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(0,3):
                        print "iCounter Val: "+str(iCounter)
                        try:
                           bStatus = self.wait_for_element_visible(locator,timeout)
                           if bStatus==True:
                               selenium.mouse_down(locator)
                               selenium.mouse_up(locator)
                               return True
                           else:
                               print "Required element not visble"
                               continue
                        except:
                            print "got exception while doing mouse actions"
                            continue
                    return False
                    
                def press_control_key(self):
                    """ Presses the Control Key """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium.key_hold(Keys.CONTROL)
                    
                def date_comparison(self,date1,date2,symbol):
                    """Returns boolean True if both the given dates are equal"""
                    try:
                        print date1
                        print date2
                        dates = date1.split("/")
                        date1 = dates[1]+"/"+dates[0]+"/"+dates[2]
                        dates = date2.split("/")
                        date2 = dates[1]+"/"+dates[0]+"/"+dates[2]
                        newdate1 = time.strptime(str(date1), "%d/%m/%Y")
                        print "newdate1"+str(newdate1)
                        newdate2 = time.strptime(str(date2), "%d/%m/%Y")
                        print "newdate2"+str(newdate2)
                        if str(symbol) == ">":
                            print "Enterd in > conditon if block"
                            return newdate1 > newdate2
                        elif str(symbol) == "<":
                            print "Enterd in < conditon if block"
                            return newdate1 < newdate2
                        elif str(symbol) == "==":
                            print "Enterd in == conditon if block"
                            return newdate1 == newdate2
                        elif str(symbol)==">=":
                            print "Enterd in >= conditon if block"
                            return newdate1 >= newdate2
                        elif str(symbol)=="<=":
                            print "Enterd in <= conditon if block"
                            return newdate1 <= newdate2
                        else:
                            raise AssertionError("Please pass third argument either < or > or == or >= or<= and also check date values")
                    except:
                        raise AssertionError("Please pass third argument either < or > or == or >= or<= and also check date values")  

                def click_on_element(self,locator):
                    """It will click on expected element for 5times if exception occured"""
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    elementStatus = self.wait_for_element_visible(locator,"30s")
                    if elementStatus == True:
                        for iCount in range(1,6):
                            try:
                                print "iCount:"+str(iCount)
                                selenium.click_element(locator)
                                return True
                            except:
                                print "exception raised"
                                if iCount == 5:
                                    print iCount+"in exception"
                                    print "Exception raised after five times also"
                                    return False
                    else:
                        print str(locator)+" is not in visible state"
                        return False
               
                def get_chrome_browser_options(self):
                    """It returns the chrome browser ChromeProfile, so that download pop up won't appear"""
                    dictionary= {'profile.default_content_settings.popups':'0'} 
                    chrome_options = Options()
                    chrome_options.add_argument("--disable-extensions")
                    chrome_options.add_argument("test-type")
                    #chrome_options.add_argument("-incognito")
                    chrome_options.add_argument("--disable-popup-blocking")
                    chrome_options.add_argument("--disable-infobars")
                    chrome_options=chrome_options
                    return chrome_options
                               
                def validate_the_sheet_in_ms_excel_file(self,filepath,sheetName):
                    """Returns the True if the specified work sheets exist in the specifed MS Excel file else False"""
                    workbook = xlrd.open_workbook(filepath)
                    snames=workbook.sheet_names()
                    sStatus=False        
                    if sheetName==None:
                        return True
                    else:
                        for sname in snames:
                            if sname.lower()==sheetName.lower():
                                wsname=sname
                                sStatus=True
                                break
                        if sStatus==False:
                            print "Error: The specified sheet: "+str(sheetName)+" doesn't exist in the specified file: "+str(filepath)
                    return sStatus

                def get_ms_excel_column_values_into_list_by_column_name(self,filePath,sheetName,columnName):
                    """ It retuen the list of registration codes"""
                    workbook = xlrd.open_workbook(filePath)
                    columnName=str(columnName)
                    worksheet = workbook.sheet_by_name(sheetName)
                    noofrows = worksheet.nrows
                    headersList = self.get_ms_excel_row_values_into_list(filePath,int(1),sheetName)
                    colIndex = headersList.index(columnName)
                    columnIndex = int(colIndex)+1
                    columnValues = []
                    for rowNo in range(1,int(noofrows)):
                        rowValues=worksheet.row_values(int(rowNo))
                        columnValues.append(rowValues[colIndex])
                    return columnValues

                def get_ms_excel_column_values_into_list(self,filepath,colNumber,sheetName=None):
                    """Returns the list of values given column in the MS Excel file """
                    workbook = xlrd.open_workbook(filepath)
                    snames=workbook.sheet_names()
                    tempList=[]
                    if sheetName==None:
                        sheetName=snames[0]      
                    if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                        return tempList
                    worksheet=workbook.sheet_by_name(sheetName)
                    noofrows=worksheet.nrows
                    #print "No.of Rows:" +str(noofrows)
                    tempList=[]
                    for rowno in range(1,noofrows):
                        row=worksheet.row(rowno)
                        for colno in range(0,len(row)):
                            cellval=worksheet.cell_value(rowno,colno)
                            if int(colNumber)==int(int(colno)+1):
                                tempList.append(cellval)
                    #print "Last Value:" +str(cellval)
                    tempList = [str(x) for x in tempList]
                    return tempList
                
                def get_ms_excel_row_values_into_list(self,filepath,rowNumber,sheetName=None):
                    """Returns the list of values given row in the MS Excel file """
                    workbook = xlrd.open_workbook(filepath)
                    snames=workbook.sheet_names()
                    tempList=[]
                    if sheetName==None:
                        sheetName=snames[0]      
                    if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                        return tempList
                    worksheet=workbook.sheet_by_name(sheetName)
                    noofrows=worksheet.nrows
                    tempList=[]
                    for rowno in range(0,noofrows):
                        row=worksheet.row(rowno)
                        for colno in range(0,len(row)):
                            cellval=worksheet.cell_value(rowno,colno)
                            if int(rowNumber)==int(int(rowno)+1):
                                tempList.append(cellval)
                    return tempList
                
                def get_ms_excel_file_rows_count(self,filepath,sheetName=None):
                    """Return The Total No Rows In MS Excel File Using The Specified File filepath"""
                    workbook = xlrd.open_workbook(filepath)
                    snames=workbook.sheet_names()
                    if sheetName==None:
                        sheetName=snames[0]      
                    if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                        return -1
                    worksheet=workbook.sheet_by_name(sheetName)
                    return worksheet.nrows

                def get_ms_excel_row_values_into_list(self,filepath,rowNumber,sheetName=None):
                    """Returns the list of values given row in the MS Excel file """
                    workbook = xlrd.open_workbook(filepath)
                    snames=workbook.sheet_names()
                    tempList=[]
                    if sheetName==None:
                        sheetName=snames[0]      
                    if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                        return tempList
                    worksheet=workbook.sheet_by_name(sheetName)
                    noofrows=worksheet.nrows
                    tempList=[]
                    for rowno in range(0,noofrows):
                        row=worksheet.row(rowno)
                        for colno in range(0,len(row)):
                            cellval=worksheet.cell_value(rowno,colno)
                            if int(rowNumber)==int(int(rowno)+1):
                                tempList.append(cellval)
                    return tempList

                def get_ms_excel_row_values_into_dictionary(self,filepath,rowNumber,sheetName=None):
                    """Returns the dictionary of values given row in the MS Excel file """
                    workbook = xlrd.open_workbook(filepath)
                    snames=workbook.sheet_names()
                    dictVar={}
                    if sheetName==None:
                        sheetName=snames[0]      
                    if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                        return dictVar
                    worksheet=workbook.sheet_by_name(sheetName)
                    noofrows=worksheet.nrows
                    dictVar={}
                    headersList=worksheet.row_values(int(0))
                    print 'headersList'
                    print headersList
                    rowValues=worksheet.row_values(int(rowNumber)+1)
                    for rowIndex in range(0,len(rowValues)):
                        dictVar[str(headersList[rowIndex])]=str(rowValues[rowIndex])
                    return dictVar

                def get_ms_excel_row_values_into_dictionary_based_on_key(self,filepath,keyName,sheetName=None):
                    """Returns the dictionary of values given row in the MS Excel file """
                    workbook = xlrd.open_workbook(filepath)
                    snames=workbook.sheet_names()
                    dictVar={}
                    if sheetName==None:
                        sheetName=snames[0]      
                    if self.validate_the_sheet_in_ms_excel_file(filepath,sheetName)==False:
                        return dictVar
                    worksheet=workbook.sheet_by_name(sheetName)
                    noofrows=worksheet.nrows
                    dictVar={}
                    headersList=worksheet.row_values(int(0))
                    for rowNo in range(1,int(noofrows)):
                        rowValues=worksheet.row_values(int(rowNo))
                        if str(rowValues[0])!=str(keyName):
                            continue
                        for rowIndex in range(0,len(rowValues)):
                            cell_data=rowValues[rowIndex]
                            cell_data=self.get_unique_test_data(cell_data)
                        
                            dictVar[str(headersList[rowIndex])]=str(cell_data)
                    return dictVar

                def get_unique_test_data(self,testdata):
                    """Returns the unique if data contains unique word """
                    testdata=str(testdata)
                    timestamp=self.get_unique_five_digits_number()
                    testdata=testdata.replace("unique",timestamp)
                    testdata=testdata.replace("Unique",timestamp)
                    return testdata

                def get_current_time(self):
                    """Return the Current date value"""
                    return time.strftime("%H-%M-%S")

                def get_current_time_stamp(self,bStatus=True):
                    """Return the Current date value"""
                    ts=datetime.datetime.now()
                    if bStatus==True:
                            ts=(str(ts).split(".")[0]).replace("-","").replace(":","").replace(" ","")
                    else:
                            ts=(str(ts).split(" ")[1]).replace(".","").replace(":","")
                            n=randint(1,99)
                            ts=str(ts)+str(n)
                    return ts
                
                def get_unique_five_digits_number(self):
                    try:
                        return str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))
                    except Exception as exp:
                        print "Number can't be generated"+ str(exp)




                
class est(datetime.tzinfo):
    def utcoffset(self, dt):
        """ returns the time and date"""
        return datetime.timedelta(hours=-4)
    def dst(self, dt):
        return datetime.timedelta(0)
