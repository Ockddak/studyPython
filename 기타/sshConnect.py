#!/usr/bin/env python
# coding: utf-8

import paramiko
import numpy as np
import pandas as pd
import os
import time
import io

print(paramiko.__version__)


def waitStrems(chan): 
    time.sleep(1) 
    outdata=errdata = "" 
    while chan.recv_ready(): 
        outdata += str(chan.recv(1000).decode('utf-8', 'ignore'))      
    while chan.recv_stderr_ready(): 
        errdata += str(chan.recv_stderr(1000).decode('utf-8', 'ignore')) 
    return outdata, errdata


try :
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('IP', username='ID', password='Password'
                , key_filename='pub file Path' , look_for_keys=False, allow_agent=False)
    print('ssh connected.')
    
    # session 사용
    se1 = ssh.invoke_shell()
    se1.settimeout(9999)
    se1.send('cd bin\n')
    se1.send('pwd\n')
    se1.send('ls\n')
    outdata, errdata = waitStrems(se1)
#     print(outdata)
    
    se1.send(conv_str)
    status='Normal'
    while status!='End':
        time.sleep(1)
        resp = str(se1.recv(100000).decode('utf-8', 'ignore'))
        print(resp)
        if resp.count(input_file) > 1:
            status='End'

    print('Thank you!')    

    ssh.close()
except Exception as err:
    print(err)

# ftp 사용(파일 업로드)
import ftplib

ftp = ftplib.FTP()
ftp.connect(host='IP')
ftp.encoding='인코딩'
ftp.decode='디코딩'
ftp.login(user='ID', passwd = 'Password')
ftp.retrlines('LIST')
files = ftp.nlst()
print(files)

