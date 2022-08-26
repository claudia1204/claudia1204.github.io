---
layout: post
title:  "Appium mac config guide"
date:   2021-09-20 19:40:41 +0800
categories: appium
tags: appium

---




[appium mac config guide](http://appium.io/docs/en/about-appium/getting-started/)

## 1. install appium
Appium can be installed in one of two ways: via NPM or by downloading Appium Desktop, which is a graphical, desktop-based way to launch the Appium server.

here we use the npm to install appium. firstly confirm node installed.

```
brew install node      
node -v  
npm -v  
npm install -g appium@1.18   #recommend 1.18, tested ok.  
appium -v 
```

then use appium-doctor to check if any dependencies install needed
```
(base) xxxx@M-C02Q90LGFVH6:~/Documents/xxxxx/ios/code/appium/node_modules/appium-webdriveragent$ appium-doctor --ios  
info AppiumDoctor Appium Doctor v.1.15.4  
info AppiumDoctor ### Diagnostic for necessary dependencies starting ###  
info AppiumDoctor  ✔ The Node.js binary was found at: /Users/xxxx/.nvm/versions/node/v14.5.0/bin/node  
info AppiumDoctor  ✔ Node version is 14.5.0  
info AppiumDoctor  ✔ Xcode is installed at: /Applications/Xcode.app/Contents/Developer  
info AppiumDoctor  ✔ Xcode Command Line Tools are installed in: /Applications/Xcode.app/Contents/Developer  
info AppiumDoctor  ✔ DevToolsSecurity is enabled.  
info AppiumDoctor  ✔ The Authorization DB is set up properly.  
info AppiumDoctor  ✔ Carthage was found at: /usr/local/bin/carthage. Installed version is: 0.36.0  
info AppiumDoctor  ✔ HOME is set to: /Users/xxxx  
info AppiumDoctor ### Diagnostic for necessary dependencies completed, no fix needed. ###  
```

## 2. install  XCUITest Driver on ios real device ##

[xcuitest driver]: https://github.com/appium/appium-xcuitest-driver

### 2.1 install external dependencies ###

```
brew install carthage  
gem install xcpretty   # For real devices we can use xcpretty to make Xcode output more reasonable.
```

### 2.2 add devices on apple.developer.com  ###

  [apple developer device list management link](https://developer.apple.com/account/resources/devices/list)
  ![apple developer devices](/images/appium/apple_devices.PNG)
      
#### 2.2.1 find appium path
```

$ which appium  
/Users/xxxx/.nvm/versions/node/v14.5.0/bin/appium  

```

#### 2.2.2 find WebDriverAgent project under appium 

```
cd /Users/xxxx/.nvm/versions/node/v14.5.0/bin/appium/node_modules/appium-webdriveragent  
./Scripts/bootstrap.sh  
```

#### 2.2.3 open WebDriverAgent.xcodeproj in Xcode
Before open project, login Xcode with your account(should be a developer account) and find your teamID later needed. (apple developer link: https://developer.apple.com/account/resources/identifiers )  

![apple developer devices](/images/appium/teamId.png)

And then add device to your resources list on the [apple developer devices list](https://developer.apple.com/account/resources/devices/list):

open WebDriverAgent.xcodeproj under ```/Users/xxxx/.nvm/versions/node/v14.5.0/bin/appium/node_modules/appium-webdriveragent/WebDriverAgent.xcodeproj```


 For both the WebDriverAgentLib and WebDriverAgentRunner targets, select “signing” in "Build Settings”, and then select your Development Team. The outcome should look as shown below:
![teamid](/images/appium/signing.png)


If you add new device for test, you should delete provisioning file now used under ```~/Library/MobileDevice/Provisioning Profiles. ```, then restart Xcode, it will automatically download provisioning files.
![provisioning files](/images/appium/provisioning.png)

## 3.Test with appium 
Prepare a iPhone and connect it with Mac through usb(please select “trust” if question “trust this computer or not?” poped up), then get basic info like “uuid” of iphone after libimobiledevice installed(you can also get udid from Xcode).
  3.1-3.3 steps is not required, you can also get udid from Devices under Xcode.

### 3.1 install libimobiledevice
    Please see the guide and install lib libimobiledevice on mac. [libmobiledevice guide](todo)
### 3.2 get uuid with “idevice_id” provided by libimobiledevice
```
(base) xxxx@M-C02Q90LGFVH6:~/Documents/xxxxx/ios/code/appium/node_modules/appium-webdriveragent$ idevice_id  
f0fbae521xxxxxxxxxxxxxxxxxxx74d0ba11b6ae (USB)  
```
### 3.3 get app list installed on iphone with command “ideviceinstaller -l”
```
(base) xxxx@M-C02Q90LGFVH6:~/Documents/xxxxx/ios/code/appium/node_modules/appium-webdriveragent$ ideviceinstaller -l
CFBundleIdentifier, CFBundleVersion, CFBundleDisplayName
com.skyjos.ftpmanagerfree, "6201", "FTPManager"
com.xxxxx.ultracaller, "13", "ultracaller"  
com.foundry63.tailor, "2.321246456", "Tailor"  
pinterest, "8", "Pinterest"  
com.zhiliaoapp.musically, "178023", "TikTok"  
com.sogou.hotspot, "711", "今日十大热点"  
com.teapotapps.iperf, "11", "iPerf"  
com.facebook.WebDriverAgentRunner.xctrunner, "1", "WebDriverAgentRunner-Runner"  
```
   save the identifier of our target tested app like “iperf”: “com.teapotapps.iperf”
  ### 3.4 start appium server 


Start appium server with command “appium” or  “appium –uuid uuid_number_of_iphone”.
with –udid means you set the device you want to test, and if you do not set it, you can set in your test code like this:
    ```    
    from appium import webdriver
    
    IOS_BASE_CAPBILITIES = {
        # 'app': 'settings',
        'app': 'com.teapotapps.iperf',
        'automationName': 'xcuitest',
        'platformName': 'iOS',
        'platformVersion': os.getenv('IOS_PLATFORM_VERSION') or '12.3',
        'deviceName': 'bigiphone',
        'udid': 'f0fbae521xxxxxxxxxxxxxxxxxxx74d0ba11b6ae',
        'showIOSLog': True,
    }
    
    EXECUTOR = 'http://127.0.0.1:4723/wd/hub'
    
    driver = webdriver.Remote(
        command_executor=EXECUTOR,
        desired_capabilities=IOS_BASE_CAPBILITIES
    )
    ```


    ```
    (base) xxxx@M-C02Q90LGFVH6:~/test/ideviceactivate/libideviceactivation$ appium --udid f0fbae521xxxxxxxxxxxxxxxxxxx74d0ba11b6ae
    [Appium] Welcome to Appium v1.18.3
    [Appium] Non-default server args:
    [Appium]   udid: f0fbae521xxxxxxxxxxxxxxxxxxx74d0ba11b6ae
    [Appium] Deprecated server args:
    [Appium]   -U,--udid => --default-capabilities '{"udid":"f0fbae521xxxxxxxxxxxxxxxxxxx74d0ba11b6ae"}'
    [Appium] Default capabilities, which will be added to each request unless overridden by desired capabilities:
    [Appium]   udid: f0fbae521xxxxxxxxxxxxxxxxxxx74d0ba11b6ae
    [Appium] Appium REST http interface listener started on 0.0.0.0:4723
    ```
  ### 3.5 run your test code 
    ```
    import time
    import copy
    import os
    from appium import webdriver
    
    
    EXECUTOR = 'http://127.0.0.1:4723/wd/hub'
    
    #capabilities ref:http://appium.io/docs/en/writing-running-appium/caps/
    IOS_BASE_CAPBILITIES = {
        # 'app': 'settings',
        'app': 'com.teapotapps.iperf',
        'automationName': 'xcuitest',
        'platformName': 'iOS',
        'platformVersion': os.getenv('IOS_PLATFORM_VERSION') or '12.3',
        'deviceName': 'bigiphone',
        'udid': 'f0fbae521xxxxxxxxxxxxxxxxxxx74d0ba11b6ae', #test iphone
        'showIOSLog': True,
    }
    
    
    def config_settings(driver):
        wifi_ele = driver.find_element_by_name('Wi-Fi')
        print(wifi_ele)
        print(wifi_ele.text)
        # wifi_ele.click()
    
        ele = driver.find_element_by_name('Airplane Mode')
        print(ele)
        print(ele.text)
        ele.click()
    
        time.sleep(5)
        ele.click()
        print('click finished')
    
    
    def get_window_size(driver):
        size = driver.get_window_size()
        print('*********size:')
        print(size)
    
    
    def config_iperf(driver):
        ele = driver.find_element_by_name('Server port')
        print(ele)
    
        print(driver.page_source)
    
        eles = driver.find_elements_by_xpath('//XCUIElementTypeTextField')
        for ele in eles:
            print(ele.get_attribute('value'))
            ele.clear()
            ele.set_value('222')
    
        start_btn = driver.find_element_by_name('Start')
        start_btn.click()
    
    
    if __name__ == "__main__":
        caps = copy.copy(IOS_BASE_CAPBILITIES)
        print(caps['app'])
    
        driver = webdriver.Remote(
            command_executor=EXECUTOR,
            desired_capabilities=caps
        )
    
        config_iperf(driver)
    ```

##  Problems
1. use another new iphone but errors occurred

Problems: can not pair device.

Solution: reconnect to usb and choose “Trust” if question “Trust this computer or not?” poped up.



```
    [Appium] Appium v1.18.3 creating new XCUITestDriver (v3.29.0) session
    [debug] [BaseDriver] W3C capabilities and MJSONWP desired capabilities were provided
    [debug] [BaseDriver] Creating session with W3C capabilities: {
    [debug] [BaseDriver]   "alwaysMatch": {
    [debug] [BaseDriver]     "platformName": "iOS",  
    [debug] [BaseDriver]     "appium:showIOSLog": true,
    [debug] [BaseDriver]     "appium:app": "settings",  
    [debug] [BaseDriver]     "appium:automationName": "xcuitest",  
    [debug] [BaseDriver]     "appium:udid": "bac123dcxxxxxxxxxxx91ab4exxxxxf60b136e7bca",  
    [debug] [BaseDriver]     "appium:deviceName": "iPhone",  
    [debug] [BaseDriver]     "appium:platformVersion": "12.3"  
    [debug] [BaseDriver]   },  
    [debug] [BaseDriver]   "firstMatch": [  
    [debug] [BaseDriver]     {}  
    [debug] [BaseDriver]   ]  
    [debug] [BaseDriver] }  
    [BaseDriver] Session created with session id: f5023dac-8ab4-487f-8090-ae1ab06a002e  
    [debug] [XCUITest] Current user: 'xxxx'  
    [debug] [XCUITest] Available devices: bac123dcxxxxxxxxxxx91ab4exxxxxf60b136e7bca  
    [debug] [XCUITest] Creating iDevice object with udid 'bac123dcxxxxxxxxxxx91ab4exxxxxf60b136e7bca'  
    [XCUITest] Determining device to run tests on: udid: 'bac123dcxxxxxxxxxxx91ab4exxxxxf60b136e7bca', real device: true  
    [debug] [BaseDriver] Event 'xcodeDetailsRetrieved' logged at 1604995579820 (16:06:19 GMT+0800 (China Standard Time))  
    [debug] [BaseDriver] Event 'appConfigured' logged at 1604995579820 (16:06:19 GMT+0800 (China Standard Time))  
    [debug] [BaseDriver] Event 'resetStarted' logged at 1604995579820 (16:06:19 GMT+0800 (China Standard Time))  
    [debug] [XCUITest] Reset: running ios real device reset flow  
    [debug] [BaseDriver] Event 'resetComplete' logged at 1604995579820 (16:06:19 GMT+0800 (China Standard Time))
    [WebDriverAgent] Using WDA path: '/Users/xxxx/.nvm/versions/node/v14.5.0/lib/node_modules/appium/node_modules/appium-webdriveragent'  
    [WebDriverAgent] Using WDA agent: '/Users/xxxx/.nvm/versions/node/v14.5.0/lib/node_modules/appium/node_modules/appium-webdriveragent/WebDriverAgent.xcodeproj'  
    [XCUITest] Continuing without capturing device logs: Could not find a pair record for device 'bac123dcxxxxxxxxxxx91ab4exxxxxf60b136e7bca'. Please first pair with the device  
    [XCUITest] Setting up real device  
    [XCUITest] {}  
```

  2. /usr/local/lib/node_modules/appium/node_modules/appium-webdriveragent/WebDriverAgent.xcodeproj Building for iOS, but the linked and embedded framework 'YYCache.framework' was built for iOS + iOS Simulator.
 
ref https://github.com/appium/appium/issues/13996 , please try:

    ```
    npm uninstall -g appium
    npm install -g appium@beta
    ```


