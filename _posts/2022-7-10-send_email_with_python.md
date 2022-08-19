--- 
layout: post
title:  "send email with python"
date:   2022-7-10 11:00:12 +0800
categories: smtp
---


## python demo

send email python demo code
```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


class Sender(object):
    def __init__(self):
        # smtp server of qq mail 
        host_server = 'smtp.exmail.qq.com'
        # qq mail auth code
        pwd = 'xxxxxxx'
        self.sender_qq_mail = 'xx@xx.com'

        # ssl login
        self.smtp = SMTP_SSL(host_server)
        # set_debuglevel(): 1 turn on the debug mode, 0 turn off the debug mode.
        self.smtp.set_debuglevel(1)
        self.smtp.ehlo(host_server)
        self.smtp.login(self.sender_qq_mail, pwd)

    def send(self, usd_cny):
        mail_content = 'xxx'
        mail_title = 'this is title'
        receiver = self.sender_qq_mail
        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = self.sender_qq_mail
        msg["To"] = receiver
        self.smtp.sendmail(self.sender_qq_mail, receiver, msg.as_string())
        self.smtp.quit()

```