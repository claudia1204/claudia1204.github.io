---
layout: post
title:  "selenium robot/python demo"
date:   2020-01-2 20:01:11 +0800
categories: selenium
tags: selenium
---

Selenium is an open source automated testing suite for web applications.  
Selenium has four components:  
Selenium Integrated Development Environment (IDE)  
Selenium Remote Control (RC)  
Webdriver  
Selenium Grid

### Selenium IDE
a firefox extension, support record and playback.

### Selenium RC
 Selenium Core: a js program, tests run directly in browser.
 Cross Origin Problem: If the JS is not included from a HTML page on test.com, it can not access test.com resources.

  Selenium RC: a web server, support remote control browser.
  Trick web browser into believing selenium core and web application in the same origin.
  Can communicate with browser.

### Selenium Grid
distribution of selenium tests, can reduce time of running tests.


### Webdriver

Webdriver is a standard to do operations on browser, like a bridge between tests and browser.  
Different browser has different implementation.  
[Webdriver protocol defined by W3C](https://www.w3.org/TR/Webdriver1/)
> * The Webdriver protocol is organised into commands.
> * Each HTTP request with a method and template defined in this specification represents a single command,
> * and therefore each command produces a single HTTP response. In response to a command,
> * a remote end will run a series of actions against the browser.


<br/>
```
*** Settings ***
Documentation   ref: [robotframwork user guide link](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#variables)

Library         SeleniumLibrary
Library         String

*** Variables ***
${string_pass}    helloworld
${web_url}    https://www.baidu.com
${login_btn_xpath}    //*[@id="s-top-loginbtn"]
${chromedriver_path}    C:/taf/webdrivers/chromedriver_win32/chromedriver.exe

*** Test Cases ***
Open Browser To Login Page
    Open Browser    browser= Chrome    url= ${web_url}    executable_path= ${chromedriver_path}
    Title Should Be    Login Page

```


```python
#!-encoding=utf-8-

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

chrome_option = ChromeOptions()
chrome_option.add_argument("--proxy-server=http://x.x.x.x:8080")
my_chrome = Chrome(chrome_options=chrome_option,
                   executable_path="/Applications/Google Chrome.app/Contents/MacOS/chromedriver")
my_chrome.get('https://www.baidu.com')

baidu_text = my_chrome.find_element_by_id('kw')
baidu_text.send_keys('my search content')

my_chrome.find_element_by_link_text('地图')
my_chrome.find_element_by_class_name('s_ipt')
my_chrome.find_element_by_tag_name('input')
my_chrome.find_element(By.ID, 'kw')

#refresh, back
my_chrome.back()
my_chrome.forward()
my_chrome.refresh()

#set window size
my_chrome.set_window_size(400, 400)
my_chrome.maximize_window()

#mouse events
ActionChains(my_chrome).context_click(baidu_text).perform()  #click baidu input and right click
ActionChains(my_chrome).double_click(baidu_text).perform()  #click baidu input and right click
ActionChains(my_chrome).move_to_element(baidu_text).perform()  #click baidu input and right click







```
