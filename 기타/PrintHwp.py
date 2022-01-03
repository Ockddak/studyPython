"""
API 다운 사이트
https://www.hancom.com/board/devdataList.do?gnb0=25&gnb1=81

참고 사이트
https://blog.naver.com/city4574/222383894665
"""


import win32com.client as win32
import os
import time


hwp=win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.RegisterModule("FilePathCheckDLL", "HwpSecurityDllFilePathChecker")
hwp.Open('D:/sss.hwp', "HWP", "forceopen:true")
time.sleep(0.5)
act = hwp.CreateAction('Print')
pset = act.CreateSet()
act.GetDefault(pset)
act.Execute(pset)
time.sleep(0.5)
hwp.Quit()