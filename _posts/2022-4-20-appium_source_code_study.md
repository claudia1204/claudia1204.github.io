--- 
layout: post
title:  "appium source code study"
date:   2022-4-20 22:00:41 +0800
categories: appium
tags: appium

---


## Running Appium from Source
[appium link](https://github.com/appium/appium/blob/master/docs/en/contributing-to-appium/appium-from-source.md)
```javascript
npm install
npm run build
node .
```


## debug appium: 
[ref link](https://zhuanlan.zhihu.com/p/338287139)


 ``` javascript
 node --inspect-brk . --port 4723
 ```

in chrome, open:    **'chrome://inspect/#devices'**


## source code analysis
packages:
http://appium.io/docs/en/contributing-to-appium/appium-packages/index.html#appium-ios-driver

1. appium: main.js/appium.js

 1) main.js: start server
    ![appium main](/images/appium/appium_main.png){: width="800"}


 2) appium.js: extend basedriver, custom methods
 
2.  appium-basedriver
    appium-xcuitest-driver:
    
    1) start wda 
       
    2) communicate with wda  
