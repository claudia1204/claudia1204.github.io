---
layout: post
title:  "Selenium usage collection"
date:   2021-09-11 20:01:11 +0800
categories: selenium
---


## insert value to input
   When we want to use selenium to insert some value to input element in html, we follow steps as follows:
   step1: clear the text in the input
   step2: insert value

   firstly, we get element:
   ```python
   #!-encoding=utf-8-

   chrome_option = ChromeOptions()
   my_chrome = Chrome(chrome_options=chrome_option,
                       executable_path="/Applications/Google Chrome.app/Contents/MacOS/chromedriver")
   my_chrome.get('https://www.baidu.com')
   baidu_text = my_chrome.find_element_by_id('kw')

   ```

   on step1, we have multiple ways to clear text of input element

   ```python
   from selenium.webdriver.common.keys import Keys
   from selenium.webdriver.common.action_chains import ActionChains

   # by clear
   baidu_text.clear() #some times no effect

   # by actions
   actions = ActionChains(self._driver)
   actions.double_click(elem).perform() #no effect on firefox 69.0, [reference, solution no effect](https://github.com/bhecquet/seleniumRobot/issues/77)
   baidu_text.send_keys(Keys.DELETE)

   # by Ctrl+A
   elem.send_keys(Keys.CONTROL + "a")
   elem.send_keys(Keys.DELETE)

   ```

## close window

   ```python
   my_chrome.quit()  # Quits the driver and closes every associated window.
  
   my_chrome.close()  # Closes the current window.
   ```

   if you want to quit and close all, and safely ends the session with browser, try to use quit.

## execute_script
   execute_script is a way for you to run some js which can not be implemented by selenium.

## set preference for download dir in chrome
   here are some demo for set preference of chrome.

   ```python
   # set download dir
   chromeOptions = webdriver.ChromeOptions()
   chromeOptions.add_argument('--user-agent=iphone')  #mock iphone or android

   prefs = {"download.default_directory": "/path/download"}
   chromeOptions.add_experimental_option("prefs", prefs)

   ```

## chrome options reference
   [links to chrome options list](https://chromium.googlesource.com/chromium/src/+/master/chrome/common/pref_names.cc)
