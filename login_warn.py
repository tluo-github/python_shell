#!/usr/bin/env python
# coding=utf-8
#----------------------------------------------------------
# Name:         服务器登录提醒
# Purpose:      监控服务器用户登录，一旦登录就发送邮件
# Version:      1.0
# Author:       Bruce
# EMAIL:        530308461@qq.com
# Created:      2016-08-22
# Copyright:    (c) Bruce 2016
# Python:       2.4/2.7
#----------------------------------------------------------
from smtplib import SMTP
from email import MIMEText
from email import Header
from datetime import datetime
import commands


#定义主机 帐号 密码 收件人 邮件主题
smtpserver = 'smtp.163.com'
sender = 'luotaosh@163.com'
password = 'passwd'
receiver = '530308461@qq.com'
subject = u'家生活-服务器用户登录提醒'
From = u'家生活-运维管理员'
To = u'530308461@qq.com'
hostname = commands.getoutput('hostname')

def send_mail(context):
    '''发送邮件'''
                                
    #定义邮件的头部信息
    header = Header.Header
    msg = MIMEText.MIMEText(context,'plain','utf-8')
    msg['From'] = header(From)
    msg['To'] = header(To)
    msg['Subject'] = header(subject + '\n')
    #连接SMTP服务器，然后发送信息
    smtp = SMTP(smtpserver)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.close()
def get_now_date_time():
    '''获取当前的日期'''
    now = datetime.now()
    return str(now.year) + "-" + str(now.month) + "-" \
           + str(now.day) + " " + str(now.hour) + ":" \
           + str(now.minute) + ":" + str(now.second)

if __name__ == '__main__':
    problem_server_list = []
    temp_string = 'IP:120.55.85.46  主机名:[%s]  \n有用户登录! at %s \nwho: \n' % (hostname,get_now_date_time())
    who_string = commands.getoutput('who')
    problem_server_list.append(temp_string)
    problem_server_list.append(who_string)
    send_mail(''.join(problem_server_list))