---
layout: post
title:  "python demo: set proxy on windows"
date:   2019-3-12 16:29:41 +0800
categories: python
---

this is a demo to set proxy on windows with python.  
you can use pyinstaller to package it to an exe and set proxy automatically.  

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import _winreg as winreg
except:
    import winreg

INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                   r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                   0, winreg.KEY_ALL_ACCESS)


def set_key(name, value=None):
    if value is None:
        try:
            winreg.DeleteValue(INTERNET_SETTINGS, name)
        except Exception as exception:
            print('no %s, delete over' % name)
    else:
        try:
            _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
        except:
            reg_type = winreg.REG_SZ
        winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)


def use_proxy():
    set_key('AutoConfigURL', None)
    set_key('ProxyEnable', 1)
    set_key('ProxyOverride', u'*.local;<local>')  # Bypass the proxy for localhost
    set_key('ProxyServer', u'x.x.x.x:port')


def use_default():
    set_key('AutoConfigURL', 'http://x.x.x.x/proxy.pac')
    set_key('ProxyEnable', 0)


if __name__ == '__main__':
    num = input('please choose which mode you want to use: 0 for proxy and 1 for default: \n')
    if num == 0:
        use_proxy()
    elif num == 1:
        use_default()

```
