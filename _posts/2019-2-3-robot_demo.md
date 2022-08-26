--- 
layout: post
title:  "robot demo record"
date:   2019-2-3 16:29:41 +0800
categories: robotframework
tags: robotframework
---
```robotframework

*** Settings ***
Documentation   ref: [robotframwork user guide link](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#variables)

Library         SeleniumLibrary
Library         String

*** Variables ***
${string_pass}    helloworld
${web_url}    https://www.baidu.com
${login_btn_xpath}    //*[@id="s-top-loginbtn"]

*** Test Cases ***
Define variables
    ${list} =    Create List    first    second    third
    Log Many    @{list}[1:]         # Logs 'second' and  'third'.

    &{dict_user} =    Create Dictionary    username=ladygaga    password=${string_pass}
    Log     ${dict_user}[username]

#Login web test
#    Login Web    username=ladygaga    password=${string_pass}    weburl=${web_url}

Open Browser To Login Page
    Open Browser    ${web_url}
    Title Should Be    Login Page

#User status is stored in database
#    [Tags]    variables    database
#    Create Valid User    ${USERNAME}    ${PASSWORD}
#    Database Should Contain    ${USERNAME}    ${PASSWORD}    Inactive
#    Login    ${USERNAME}    ${PASSWORD}
#    +
#    Database Should Contain    ${USERNAME}    ${PASSWORD}    Active
#

test click login btn and login baidu


*** Keywords ***
Login Web
     [Tags]    a demo robot case for login baidu
     [Arguments]    ${username}    ${password}    ${weburl}
     selenium.webdriver.Firefox



Database Should Contain
    [Arguments]    ${username}    ${password}    ${status}
    ${database} =     Get File    ${DATABASE FILE}
    Should Contain    ${database}    ${username}\t${password}\t${status}\n

```
