import time
import wmi
from win32com.client import Dispatch
import os
from robot.libraries.BuiltIn import BuiltIn
import multiprocessing.pool
import functools
import pythoncom
import thread
import win32com.client


class Insurance:

    def __init__(self):
        pass

    def open_console(self,AppConnPath):
        """Invokes the Emulator by passing the .ws file path"""
        try:
            autECLConnMgr = Dispatch("PCOMM.autECLConnMgr")
            autSession = Dispatch("PCOMM.autECLSession")
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            autECLConnMgr.autECLConnList.Refresh()
            print 'connection list',autECLConnMgr.autECLConnList.Count
            if autECLConnMgr.autECLConnList.Count == 0:
                if not os.path.exists(AppConnPath):
                    print "File path doesnt Exists: "+AppConnPath
                    return False,'File path doesnt Exists: '+AppConnPath
                else:
                    print "File path Exists: "+AppConnPath
                autECLConnMgr.StartConnection("profile=" + AppConnPath + " winstate=MAX") 
                timeout = 0
                while (timeout < 10):
                    processList = wmi.WMI()
                    for process in processList.Win32_Process ():
                        if process.Name.lower()=='pcsws.exe':
                            return True,'Pass'
                    timeout = timeout + 1
                print "Connection timout. Emulator did not open in 10 secs"
                return False,'Connection timout. Emulator dint open in 10 secs'
            else:
                self.connection_reset()
                return True
        except Exception as exp:
            print "Got exception in open_console keyword.Error: "+str(exp)
            return False,'Got exception in open_console keyword.Error: '+str(exp)

    def shutdown_console(self):
        """Stops the ongoing connection and closes the Emulator"""
        try:
            autECLConnMgr = Dispatch("PCOMM.autECLConnMgr")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            autECLPSObj = Dispatch("PCOMM.autECLPS")

            if autECLConnMgr.autECLConnList.Count > 0:
                autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
                autECLPSObj.StopCommunication()
                autECLConnMgr.StopConnection(autECLConnMgr.autECLConnList(1).Handle, "saveprofile=no")
            return True
        except Exception as exp:
            print "Got exception in shutdown_console keyword.Error: "+str(exp)
            return False

    def connection_reset(self):
        """resets the available connection"""
        try:
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            
            autECLConnList.Refresh()
            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            return True
        except Exception as exp:
            print "Got exception in connection_reset keyword.Error: "+str(exp)
            return False
        
    def get_connection_count(self):
        """gets the available number of connections"""
        autECLConnMgr = Dispatch("PCOMM.autECLConnMgr")
        return autECLConnMgr.autECLConnList.Count
    
    def wait_for_text(self, sSearchText, iTime=5):
        """Waits for the text for the time mentioned, to be displayed in the screen. Time in seconds"""
        try:
            iTime = int(iTime)
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")

            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            row = 1
            col = 1
            timeout = 0
            while (timeout < iTime):
                autECLPSObj.autECLFieldList.Refresh()
                if autECLPSObj.SearchText(sSearchText, 1, row, col)[0]:
                    return True
                timeout = timeout + 1
                time.sleep(1)
            print "No Text found: "+sSearchText
            self.capture_screenshot()
            return False
        except Exception as exp:
            print "Got exception in wait_for_text keyword.Error: "+str(exp)
            self.capture_screenshot()
            return False

    def wait_for_text_until_invisible(self, sSearchText, iTime=10):
        """Waits for the text until it is invisible on screen. Time in seconds"""
        try:
            iTime = int(iTime)
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")

            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            row = 1
            col = 1
            timeout = 0
            while (timeout < iTime):
                autECLPSObj.autECLFieldList.Refresh()
                if not autECLPSObj.SearchText(sSearchText, 1, row, col)[0]:
                    return True
                timeout = timeout + 1
                time.sleep(1)
            print "Text is still visible"
            self.capture_screenshot()
            return False
        except Exception as exp:
            print "Got exception in wait_for_text_until_invisible keyword.Error: "+str(exp)
            return False
        

    def press_key(self, Keyvalue,count=1):
        """"Use to perform keyboard events."""
        try:
            count = int(count)
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            
            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            autECLPSObj.autECLFieldList.Refresh()
            if count == 1:
                autECLPSObj.SendKeys(Keyvalue)
                return True
            
            for i in range(0,count):
                autECLPSObj.SendKeys(Keyvalue)
                time.sleep(2)
            return True
        except Exception as exp:
            print "Got exception in press_key.Error: "+str(exp)
            return False

    def capture_screenshot(self):
        """"It will capture the screenshots based on ${globalScreenShot}  global variable value."""
        try:
            screenshot = BuiltIn().get_library_instance("Screenshot")
            bStatus = BuiltIn().get_variable_value("${globalScreenShot}")
            print "bStatus: "+str(bStatus)
            if(str(bStatus).lower()=='true'):
                screenshot.take_screenshot()
        except Exception as exp:
            print "Got exception in capture_screenshot keyword.Error: "+str(exp)
            return False
        
    def get_value_by_field_name(self, sFieldName, iPos=0):
        """To capture the Field Text by the given Field Label """
        try:
            iPos = int(iPos)
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            
            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            autECLPSObj.autECLFieldList.Refresh()
            i = 1
            row = 1
            col = 1
            if not autECLPSObj.SearchText(sFieldName, 1, row, col)[0]:
                return "NA"
            while i <= autECLPSObj.autECLFieldList.Count:
                if autECLPSObj.autECLFieldList(i).GetText().strip() == sFieldName:
                    return autECLPSObj.autECLFieldList(i+iPos).GetText()
                i = i + 1
        except Exception as ex:
            print "Got Exception in get_value_by_field_nameL.Error: "+str(ex)
            return "NA"

    def extract_all_fields_from_screen(self, sFilePath=None):
        """Extract all the field names to a given text file with their Field Positions"""
        try:
            if sFilePath == None:
                sFilePath = "FieldDetails.txt"
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")

            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            autECLPSObj.autECLFieldList.Refresh()
            if autECLPSObj.autECLFieldList.Count==0:
                self.write_text_file("*************No Fields Available***************", sFilePath, False)
                print "No fields available on the screen"
                return False
            self.write_text_file("*************Extracting all the fields in the Screen***************", sFilePath, False)
            index = 1
            print "Field List.Count:"
            print autECLPSObj.autECLFieldList.Count
            while index < autECLPSObj.autECLFieldList.Count:
                self.write_text_file("Field Index: "+str(index)+" Field label: " + autECLPSObj.autECLFieldList(index).GetText(), sFilePath, True)
                index = index + 1
            self.write_text_file("*************End of - Extracting all the fields in the Screen***************", sFilePath, True)
            return True
        except Exception as exp:
            print "Got exception in extract_all_fields_from_screen keyword.Error: "+str(exp)
            return False

    def write_text_file(self, sText, fPath, append=True):
        """write data to given text file"""
        if append:
            myFile = open(fPath, 'a')
        else:
             myFile = open(fPath, 'w')
        myFile.write(str(sText)+"\n")
        myFile.close()
        return True

    def enter_text_by_field_Name(self, sSearchText, sValue="", instance=1):
        """To enter the text against a field label. The first parameter is mandate and other two are optional.Instance is used in the case of multiple fields with same name.If you want to erase the field value, pass Value as "empty" from your test data."""
        try:
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")

            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            autECLPSObj.autECLFieldList.Refresh()
            if sSearchText != "":
                if str(sValue).lower()=='na':
                    return True
                bstatus = self.set_cursor_position(sSearchText,instance)
                if not bstatus:
                    return False
                autECLPSObj.SendKeys("[TAB]")
                time.sleep(1)
                autECLPSObj.SendKeys("[erase eof]")
                if sValue != "":
                    autECLPSObj.setText(sValue)
                    return True
                elif sValue == "":
                    print "No value in Sheet"
                    return True
                else:
                    return False
            else:
                return False
        except Exception as exp:
            
            print "Got Exception in enter_text_by_field_Name.Error: "+str(exp)
            self.capture_screenshot()
            return False

    def set_cursor_position(self, sSearchText, instance=1):
        """To set the cursor at the start of the text passed as parameter.Instance is used if we have more than 1 identical text in the screen."""
        try:
            instance = int(instance)
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            
            autECLPSObj.autECLFieldList.Refresh()
            row = 1
            col = 1
            newcol = 0
            Temprow = 0
            temp = autECLPSObj.SearchText(sSearchText, 1, row, col)
            if temp[0]:
                row = temp[1]
                col = temp[2]
                if instance > 1:
                    ints = 1
                    while ints <= instance:
                        newcol = newcol+ 1
                        autECLPSObj.SetCursorPos(row, newcol)
                        result = autECLPSObj.SearchText(sSearchText, 1, row, newcol)
                        if result[0]:
                            row = result[1]
                            newcol = result[2]
                            if (ints == instance):
                                autECLPSObj.SetCursorPos(row, newcol)
                                return True
                            ints = ints + 1
                else:
                    autECLPSObj.SetCursorPos(row, col)
                    return True
            else:
                self.capture_screenshot()
                return False
            
        except Exception as exp:
            print "Got Exception in set_cursor_position keyword. Error: "+str(exp)
            self.capture_screenshot()
            return False

    def set_cursor_position_for_menu(self, sSearchMenuText, instance=1):
        """To set the cursor at the start of the menutext passed as parameter.Instance is used if we have more than 1 identical text in the screen."""
        try:
            instance = int(instance)
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            
            autECLPSObj.autECLFieldList.Refresh()
            row = 1
            col = 1
            newcol = 0
            Temprow = 0
            temp = autECLPSObj.SearchText(sSearchMenuText, 1, row, col)
            if temp[0]:
                row = temp[1]
                col = temp[2]
                if instance > 1:
                    ints = 1
                    while ints <= instance:
                        newcol = newcol+ 1
                        autECLPSObj.SetCursorPos(row, newcol)
                        result = autECLPSObj.SearchText(sSearchMenuText, 1, row, newcol)
                        if result[0]:
                            row = result[1]
                            newcol = result[2]
                            if (ints == instance):
                                autECLPSObj.SetCursorPos(row, newcol - 4)
                                return True
                            ints = ints + 1
                else:
                    autECLPSObj.SetCursorPos(row, col - 4)
                    return True
            else:
                print sSearchMenuText+" no available on screen"
                self.capture_screenshot()
                return False
            
        except Exception as exp:
            self.capture_screenshot()
            print "Got Exception in set_cursor_position_for_menu keyword. Error: "+str(exp)
            return False

    def select_menu_Item(self, sMenuName, instance=1):
        """To Select the Module or Sub module."""
        try:
            bstatus = self.set_cursor_position_for_menu(sMenuName,instance)
            if not bstatus:
                return False
            self.press_key("[TAB]")
            self.press_key("[ENTER]")
            return True
        except Exception as exp:
            print "Got Exception in select_menu_Item keyword. Error: "+str(exp)
            return False
            

    def get_cursor_position(self):
        """This gets the current position of the cursor in the presentation space for the connection associated"""
        try:
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            
            autECLPSObj.autECLFieldList.Refresh()
            curRow = autECLPSObj.CursorPosRow
            curCol = autECLPSObj.CursorPosCol
            return (curRow,curCol)
        except Exception as exp:
            print "Got Exception in get_cursor_position keyword. Error: "+str(exp)
            return (0,0)

    def check_and_mark(self,sSearchVal,keyOpr="[BackTab]",markVal="X"):
        """This gets the current position of the cursor in the presentation space for the connection associated"""
        try:
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")

            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            autECLPSObj.autECLFieldList.Refresh()
            if not (self.set_cursor_position(sSearchVal)):
                return False
            self.press_key(keyOpr)
            self.enter_text(markVal)
            return (curRow,curCol)
        except Exception as exp:
            print "Got Exception in check_and_mark keyword. Error: "+str(exp)
            return (0,0)

    def enter_text(self, sValue):
        """ This keyword will enter text svalue at current position"""
        try:
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")

            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            autECLPSObj.autECLFieldList.Refresh()
            autECLPSObj.setText(sValue)
            return True
        except Exception as exp:
            print "Got Exception in enter_text keyword. Error: "+str(exp)
            return False

    def get_value_by_row_and_column(self, Row, Col, txtLen):
        """To capture the output values or any other values on the screen based on the row, column and length of the text"""
        try:
            Row = int(Row)
            Col = int(Col)
            txtLen = int(txtLen)
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")
            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            return autECLPSObj.GetText(Row, Col, txtLen)
        except Exception as exp:
            print "Got Exception in get_value_by_row_and_column keyword. Error: "+str(exp)
            return "NA"

    def select_item_from_search_table_by_field_name(self,fieldname,selectvalue,instance=1):
        """To capture the output values or any other values on the screen based on the row, column and length of the text"""
        try:
            autECLPSObj = Dispatch("PCOMM.autECLPS")
            autECLConnList = Dispatch("PCOMM.autECLConnList")

            autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
            autECLPSObj.autECLFieldList.Refresh()
            if str(selectvalue).lower()=='na':
                return True
            fieldStatus = self.wait_for_text(fieldname,10)
            bstatus = self.set_cursor_position(fieldname,instance)
            if not bstatus:
                return False
            time.sleep(1)
            self.press_key("[TAB]")
            time.sleep(1)
            self.press_key("[erase eof]")
            self.press_key("[PF4]")
            bstatus = self.wait_for_text("Table Item Search",10)
            if not bstatus:
                return False
            for index in range(1,20):
                bstatus = self.set_cursor_position(selectvalue,1)
                if not bstatus:
                    bMoreStatus = self.wait_for_text("More...",3)
                    if not bMoreStatus:
                        self.press_key("[ENTER]")
                        return False
                    else:
                        self.press_key("[pagedn]")
                else:
                    self.press_key("[backtab]")
                    self.press_key("1")
                    self.press_key("[ENTER]")
                    tableStatus = self.wait_for_text_until_invisible("Table Item Search",10)
                    return tableStatus
            self.press_key("[ENTER]")
            return False
        except Exception as exp:
            print "Got Exception in select_item_from_search_table_by_field_name keyword. Error: "+str(exp)
            return "NA"
           
# Check Below Keywords *********************************************************************
#*******************************************************************************************

    def go_to_screen(self, sScreenName, KeyValue='[PF3]'):
        """Will perform the keyboard operation until the text/screen is displayed"""
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
        
        KeyCnt = 0
        row = 1
        col = 1
        autECLPSObj.autECLFieldList.Refresh()
        if autECLPSObj.SearchText(sScreenName, 1, row, col)[0]:
            return True
        KeyCnt = 0
        while KeyCnt <= 20:
            print "press"+str(KeyCnt)
            autECLPSObj.SendKeys(KeyValue)
            autECLPSObj.autECLFieldList.Refresh()
            if self.wait_for_text(sScreenName,5):
                return True
            KeyCnt = KeyCnt + 1
        return False





    def get_value_by_rectangle(self, StartRow, StartCol, EndRow, EndCol):
        """To get all the data present in the rectangle formed by the StartRow, StartCol, EndRow  and EndCol."""
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
        
        return autECLPSObj.GetTextRect(StartRow, StartCol, EndRow, EndCol)

    def set_cursor_position_in_backward_direction(self, sSearchText, instance=1):
        """To set the cursor before the text from the bottom of the screen in backward direction passed as parameter."""
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
        
        autECLPSObj.autECLFieldList.Refresh()
        row = 24
        col = 1
        newcol = 80
        Temprow = 0
        temp = autECLPSObj.SearchText(sSearchText, 2, row, col)
        if temp[0]:
            row = temp[1]
            col = temp[2]
            if instance > 1:
                ints = 1
                while (ints <= instance):
                    newcol = newcol - 1
                    autECLPSObj.SetCursorPos(row, newcol)
                    result = autECLPSObj.SearchText(sSearchText, 2, row, newcol)
                    if result[0]:
                        row = result[1]
                        newcol = result[2]
                        if (ints == instance and Temprow > row):
                            autECLPSObj.SetCursorPos(row, newcol - 1)
                            return True
                        Temprow = row
                        ints = ints + 1
            else:
                autECLPSObj.SetCursorPos(row, col - 1)
                return True
        else:
            return False

    def set_cursor_position_before_value(self, sSearchText, instance=1):
        """To set the cursor before the text passed as parameter.Instance is used if we have more than 1 identical text in the screen."""
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
        
        autECLPSObj.autECLFieldList.Refresh()
        row = 1
        col = 1
        newcol = 0
        temp = autECLPSObj.SearchText(sSearchText, 1, row, col)
        if temp[0]:
            row = temp[1]
            col = temp[2]
            if instance > 1:
                ints = 1
                while (ints <= instance):
                    newcol = col + 1
                    autECLPSObj.SetCursorPos(row, newcol)
                    result = autECLPSObj.SearchText(sSearchText, 1, row, newcol)
                    if result[0]:
                        row = result[1]
                        newcol =  result[2]
                        if (ints == instance):
                            autECLPSObj.SetCursorPos(row, newcol-1)
                            return True
                        ints = ints+1
            else:
                autECLPSObj.SetCursorPos(row, col-1)
                return True
        else:
            return False

    def set_cursor_position_dup(self, sSearchText, row, col, instance=1):
        """Searches the given text from the given row and column and sets the cursor at the given text."""
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
        
        autECLPSObj.autECLFieldList.Refresh()
        newcol = 0
        temp = autECLPSObj.SearchText(sSearchText, 1, row, col)
        if temp[0]:
            row = temp[1]
            col = temp[2]
            if instance > 1:
                newcol = col + 1
                autECLPSObj.SetCursorPos(row, newcol)
                result = self._autECLPSObj.SearchText(sSearchText, 1, row, newcol)
                if result[0]:
                    row = result[1]
                    newcol = result[2]
                    autECLPSObj.SetCursorPos(row, newcol - 1)
                    return True
            else:
                autECLPSObj.SetCursorPos(row, col - 1)
                return True
        else:
            return False





    def edit_and_update_value(self, sSearchText, row, col, sValue):
        """Update the value of a editable field with new value provided."""
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
        
        bstatus = set_cursor_position_dup(sSearchText, row, col)
        if not bstatus:
            return False
        press_key("[Tab]")
        enter_text(sValue)
        return True


    def validate_text_on_screen(self, sSearchText, instance=1):
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
        
        autECLPSObj.autECLFieldList.Refresh()
        row = 1
        col = 1
        newcol = 1
        Temprow = 0
        if instance > 1:
            ints = 1
            while ints <= instance:
                newcol = newcol + 1
                autECLPSObj.SetCursorPos(row, newcol)
                temp = autECLPSObj.SearchText(sSearchText, 1, row, newcol)
                if temp[0]:
                    row= temp[1]
                    newcol = temp[2]
                    if (ints == instance):
                        return True
                    ints = ints + 1
        else:
            if autECLPSObj.SearchText(sSearchText, row, col)[0]:
                return True
            else:
                return False

    def enter_text_by_field_name_back(self, sSearchText, sValue, instance=1):
        """To enter the text against a field label (ex: if the text field is before the field label). The first parameter is mandate and other two are optional.
        Instance is used in the case of multiple fields with same name"""
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)
        
        bstatus = set_cursor_position(sSearchText,instance)
        if not bstatus:
            return False
        autECLPSObj.SendKeys("[backtab]")
        autECLPSObj.setText(sValue)
        return True
    
    def extract_billno_subsidiarymember_(self, Row, Col, txtLen):
        'Bottom'
        'Roll up not permitted'
        autECLPSObj = Dispatch("PCOMM.autECLPS")
        autECLConnList = Dispatch("PCOMM.autECLConnList")
        autECLPSObj.SetConnectionByHandle(autECLConnList(1).Handle)

        
        '''get_text = get_value_by_row_and_column(self, Row, Col, txtLen)
        if get_text == 'Bottom':
            return True
        else:
            press_key("[Page Down]")'''

        bstatus == False
        while bstatus:
            get_text = get_value_by_row_and_column(self, Row, Col, txtLen)
            if get_text == 'Bottom':
                return True
            else:
                press_key("[Page Down]")
            

        
        
    def timeout(max_timeout):
        try:
            """Timeout decorator, parameter in seconds."""
            def timeout_decorator(item):
                """Wrap the original function."""            
                @functools.wraps(item)
                def func_wrapper(*args, **kwargs):
                    """Closure for function."""
                    print "wrapper"
                    pool = multiprocessing.pool.ThreadPool(processes=1)
                    print "pool"
                    async_result = pool.apply_async(item, args, kwargs)
                    print "async"                
                    # raises a TimeoutError if execution exceeds max_timeout
                    async_result.get(max_timeout)
                return func_wrapper
            return timeout_decorator
        except Exception as exp:
            return

    @timeout(5.0)
    def run_macro(self,sfilepath,sMacroName):
        """Select the file and run the macro"""
        pythoncom.CoInitialize()
        xl = win32com.client.Dispatch("Excel.Application")
        xl.Workbooks.Open(sfilepath, ReadOnly=1)
        try:
            macroNames=xl.Application.Run(sMacroName)
            #xl.Workbooks(1).Close(SaveChanges=0)
            #xl.Application.Quit()
            return True
        except:
            #xl.Workbooks(1).Close(SaveChanges=0)
            #xl.Application.Quit()
            return False
    @timeout(5.0)  
    def run_upload(self,sfilepath):
        """To run the upload through python using autoit library"""
        #pythoncom.CoInitialize()
        autoit = BuiltIn().get_library_instance('AutoItLibrary')
        
        try:
            pythoncom.CoInitialize()
            os.system(sfilepath)
            #autoit.win_wait_active("[TITLE:Data Transfer to IBM i - Upload.DTT]",3)
            print "checking for active window"
            #autoit.control_send("[TITLE:Data Transfer to IBM i - Upload.DTT]","Button6")
            #autoit.control_click("[TITLE:Data Transfer to IBM i - Upload.DTT]","Button6")
            #autoit.run(sfilepath)
            return True
        except:
            return False
    

    
    def spool_files_message_validation(self,uploadcount,list_successfull_msg,actual_terminated_msg):
        try:
            #list_successfull_msg = 'List of members successfully added'
            #list_successfull_msg = 'List of members successfully terminated'
            #list_successfull_msg = 'List of members successfully changed'
            list_of_error_msg = 'List of members with errors'
            #actual_terminated_msg = 'Total number of members changed :'
            #actual_terminated_msg = 'Total number of members terminated :'
            #actual_terminated_msg = 'Total number of members added :'
            bottom_msg = 'Bottom'
            total_mem_msg = 'Total number of members :'
            row_no = 4
            btm_count = 0
            bottom_status = 'False'
            page_status = 'True'
            message = self.get_value_by_row_and_column(1, 55, 30)
            
            while True:
                if not 'Display Spooled File' in message:
                    page_status = 'False'
                row_no = row_no+1
                print row_no
                bottom_status = self.verify_bottom_msg()
                if row_no == 24:
                    self.press_key("[pagedn]")
                    row_no = 6
                for row in range(row_no,24):
                    message = self.get_value_by_row_and_column(row, 2, 100)
                    if message == 'NA':
                        print 'Exception in spool_files_message_validation ,get_value_by_row_and_column'
                        break
                    message = message.strip()
                    
                    print 'message in main function:', message                
                    if (list_successfull_msg in message):
                        print 'Entered in List of members with successful record'
                        msg, suc_count_row = self.verify_expected_msg_in_screens(row,actual_terminated_msg)
                        if msg == 'None':
                            print 'Expected message: ',actual_terminated_msg,' not found'
                            return 'False','None','Expected message: '+str(actual_terminated_msg)+' is not found, while '+str(list_successfull_msg)+' message is avialable in screen'
                        success_count = self.split_func_get_count(msg)
                        print 'success_records_count',success_count
                        if(int(uploadcount) != int(success_count)):
                            print 'Entered in different count',uploadcount, success_count
                            print 'uploadcount was mis matched with success records count'
                            failed_records_count = int(uploadcount)- int(success_count)
                            list_err_records,msg = self.verify_member_with_error_get_failed_record_list(suc_count_row,list_of_error_msg,total_mem_msg)
                            if list_err_records == 'None':
                                return 'False','None',msg+'. Records passed count: '+str(success_count)+' is not matching with the upload count '+str(uploadcount)
##                            if len(list_err_records) != int(failed_records_count):
##                                return 'False',list_err_records,'Error records count: '+str(len(list_err_records))+' is not matching with the failure count:'+str(failed_records_count)
                            return 'False',list_err_records,'Uploaded Records count is '+str(uploadcount)+'. Records failure count is: '+str(failed_records_count)
                        else:
                            return 'True','Pass','Total records got passed'
                        
                    if (list_of_error_msg in message):
                        ''' If first we got the List of members with errors then we need tot fail the tesst because no success records available to issue policy'''
                        list_err_records,msg = self.verify_member_with_error_get_failed_record_list(row-1,list_of_error_msg,total_mem_msg)
                        if list_err_records == 'None':
                            return 'Fail',list_err_records,str(msg)+'Total records '+str(uploadcount)+' failed'
                        #if len(list_err_records) == int(uploadcount):
                        return 'Fail',list_err_records,'Total records:'+str(uploadcount)+' failed'
##                        else:
##                            print 'len(list_err_records) == int(uploadcount)',len(list_err_records), int(uploadcount)
##                            return 'Fail',list_err_records,'No Success records found and total member numbers count'+str(len(list_err_records))+' is not matching with upload count '+str(uploadcount)
                    row_no = row
                if bottom_status == 'True':
                    print 'Got the bottom page in main function'
                    return 'False','None','Got the bottom page but no messages:'+str(list_successfull_msg)+' or '+str(list_of_error_msg)+' found'
                if page_status == 'False':
                    print '\n Page in Login scree:\n'
                    return 'False','None','Please check the screen, page is not in Display Spooled file screen'
           
        except Exception as exp:
           print "Got Exception in spool_files_message_validation keyword. Error: "+str(exp)
           return 'False','None',"Got Exception in spool_files_message_validation keyword. Error: "+str(exp)
        return "False",'None','Completed Main function'

    def verify_member_with_error_get_failed_record_list(self,row,mem_err_msg,total_mem_msg):
        try:
            print 'Entered in verify_member_with_error_get_failed_record_list'
            print 'row,mem_err_msg,total_mem_msg',row,mem_err_msg,total_mem_msg
            bottom_status = 'False'
            while True:
                row = row+1
                bottom_status = self.verify_bottom_msg()
                if (row == 24):
                    self.press_key("[pagedn]")                    
                    row = 6
                for err_row in range(row,24):
                    row = err_row
                    message = self.get_value_by_row_and_column(row, 2, 100)
                    if message == 'NA':
                        print 'Exception in verify_member_with_error_get_failed_record_list ,get_value_by_row_and_column'
                        break
                    message = message.strip()
                    print 'Member error message', message
                    if (mem_err_msg in message):
                        print 'Entered in List of members with errors'
                        row = row+6
                        record_list,count,msg = self.get_error_records_list(row,total_mem_msg)
                        if len(record_list) != int(count):
                            return record_list,'No of error Records count: '+str(len(record_list))+' is not matching with the total number of members count: '+str(count)
                        return record_list,msg
                if bottom_status == 'True':
                    return 'None','Got the bottom page and no error records found'
                    
        except Exception, e:
            print 'Exception in verify_member_with_error_get_failed_record_list',str(e)
            return 'None','Exception in verify_member_with_error_get_failed_record_list '+str(e)
            
            
                
                    
    def get_error_records_list(self,row,total_mem_msg):
        try:
            print 'Entered in get_error_records_list'
            error_lsit = []
            bottom_status = 'False'
            policy_status = 'True'
            while True:
                bottom_status = self.verify_bottom_msg()
                if row >= 24:
                    self.press_key("[pagedn]")
                    row = row-24
                    row = row+5
                    print 'Row after page down: ', row
                for i in range(row,24):
                    i = i+1
                    row = i
##                    total_row = i+1
##                    if total_row == 25:
##                        row = 24
##                        break
                    total_ms = self.get_value_by_row_and_column(i, 2, 100)
                    if total_ms == 'NA':                        
                        print 'Exception in get_error_records_list ,get_value_by_row_and_column'
                        break
                    if total_mem_msg in total_ms:
                        print '\n===============Found total members==========\nactual messgae: '+total_ms
                        print 'error_lsit: ',error_lsit
                        failed_count = self.split_func_get_count(total_ms)
                        return error_lsit,failed_count,'Got the total number of members message'
                    message = self.get_value_by_row_and_column(i, 2, 130)
                    if message == 'NA':
                        print 'Exception in get_error_records_list ,get_value_by_row_and_column'
                        break
                    message = message.strip()
                    message = message.replace('                                ', '',3)
                    message = message.replace('      ','')
                    
                    if 'Policy number:' in message:
                        policy_status = 'False'
                        row = i+5
                        break
                    policy_status = 'True'
                    print 'Error record',message
                    error_lsit.append(message)
                    
                print 'Row number in error records: ',row
                
                if bottom_status == 'True' and policy_status == 'True':
                    return error_lsit,0,'Got the bottom page while reading the error records'
        except Exception, e:
            print 'Exception in get_error_records_list',str(e)
            return 'None',0,'Exception in get_error_records_list: '+str(e)
            
        
    def verify_expected_msg_in_screens(self,row,expected_msg):
        try:
                
            bottom_status = 'False'
            print 'print expected_msg: ',expected_msg
            while True:
                print 'row',row
                bottom_status = self.verify_bottom_msg()
                if (row == 24):
                    self.press_key("[pagedn]")                    
                    row = 5
                for i in range (row,24):
                    i=i+1
                    row = i
                    actual_msg = self.get_value_by_row_and_column(i,2,100)
                    if actual_msg == 'NA':
                        print 'Exception in verify_expected_msg_in_screens ,get_value_by_row_and_column'
                        break
                    if (expected_msg in actual_msg):
                        print 'actual_msg : ', actual_msg
                        return actual_msg,i                    
                if bottom_status == 'True':
                    return 'None','No '+str(expected_msg)+' message found '
                
        except Exception,e:
            print 'Exception in verify_expected_msg_in_screens',str(e)
            return 'None','Exception in verify expected msg :'+str(expected_msg)+' in display spooled files screen '+str(e)
    def verify_bottom_msg(self):
        bottom_message = self.get_value_by_row_and_column(25, 1, 133)
        if bottom_message == 'NA':
            print 'Exception in verify_bottom_msg ,get_value_by_row_and_column'
            return 'False'
        bottom_message = bottom_message.strip()
        print bottom_message
        if(bottom_message == 'Bottom'):
            print 'bottom message'
            bottom_status = 'True'
            return 'True'
        else:
            return 'False'
    def split_func_get_count(self,msg):
        msg= msg.split(':')
        records_count = msg[1].strip()
        return records_count
            
    
    def error_records_count(self,row,total_mem_msg):
        while True:

            for i in range (row,26):
                print row
##                row=row+1
                total_num_message=self.get_value_by_row_and_column(i,2,100)
            
                #terminated_message=terminated_message.strip()
                print 'total_num_message',total_num_message
                if (total_mem_msg in total_num_message):
                    print 'total_mem_msg', total_num_message
                    total_num_message= total_num_message.split(':')
                    print 'total_num_message                   :  ',total_num_message
                    error_records_count=total_num_message[1].strip()
                    print 'records_count:\n', error_records_count
                #return error_records_count
                if(row == 26):
                    row = 4
                    self.press_key("[pagedn]")
                    print 'pagedown:'
                    bottom_message=self.get_value_by_row_and_column(25, 1, 133)
                    bottom_message=bottom_message.strip()
                    print bottom_message
                    if(row==25 and bottom_message==bottom_msg):
                        print 'bottom message'
                        #break
        return error_records_count


    def list_of_total_records(self,row,policy_number):
        row=row+1
        policy_number='Policy number:'
        for i in range (row,26):
            message1=self.get_value_by_row_and_column(i,2,100)
            message1=message1.strip()
            print 'error message', message1
            if (list_of_error_msg in message1):
                print 'error msg:\n',message1
                print 'rownumber',i
                
        return i
            
            
 

    


    
        
        

        
    
