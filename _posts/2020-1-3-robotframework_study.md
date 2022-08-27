--- 
layout: post
title:  "robotframework study"
date:   2020-1-3 16:29:41 +0800
categories: robotframework
tags: robotframework
---

## ROBOT_LIBRARY_SCOPE


ROBOT_LIBRARY_SCOPE has tree types of values.

### TEST CASE ##
A new instance is created for every test case.
A possible suite setup and suite teardown share yet another instance.
This is the default.

### TEST SUITE ##
A new instance is created for every test suite.
The lowest-level test suites, created from test case files and containing test cases, have instances of their own, and higher-level suites all get their own instances for their possible setups and teardowns.

### GLOBAL ##
Only one instance is created during the whole test execution and it is shared by all test cases and test suites.
Libraries created from modules are always global.


## run case ##
<code>
 robot -V /env_path/ -L TRACE -b debug.log -d /log_path/ /case_path/demo.robot
</code>


## variables ##
demo:
```
    ${list} =    Create List    first    second    third
    Log Many    @{list}[1:]         # Logs 'second' and  'third'.

    &{dict_user} =    Create Dictionary    username=ladygaga    password=${string_pass}
    Log     ${dict_user}[username]
```

## Basic demo ##
```robotframework

*** Settings ***
Documentation   Example of different sections in robot case: settings, variables, test cases, keywords, tasks, comments
...             \n
...             ref link:[https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html]

Library         OperatingSystem
Library         ./resource.py
Test Setup       Setup Env
Test Teardown    Teardown Env

*** Variables ***
${pass}           password
${number_value}   ${10}
${path}           /

*** Test Cases ***
Define variables
    ${list} =    Create List    first    second    third
    Log Many    @{list}[1:]         # Logs 'second' and  'third'.

    &{dict_user} =    Create Dictionary    username=ladygaga    password=${pass}
    Log    ${dict_user}[username]

    ${number} =    Set Variable    ${-2}
    Log    ${number * 10}

    Log    ${33}

    ${bool_flag} = ${TRUE}
    Log    ${bool_flag}

Call keyword
    Check path exists    path1=/

Call Method form python file
    Check Path Is Folder    path=${path}

*** Keywords ***
Check path exists
     [Setup]    case setup
     [Arguments]    ${path1}
     ...       ${path2}='./'
     [Documentation]  keyword demo, check params path1 and path2 exists or not
     ...              path1 (str) - this is path1 from arguments, folder path1
     ...              path1 (str) - this is path2 from arguments, folder path2
     [Tags]    a kw demo
     Log    ${path1}
     Log    ${path1}
     Directory Should Exist    ${path1}
     Directory Should Exist    ${path2}
     [return]    ${True}
     [Teardown]    case teardown

Pass Variables
     [Arguments]    @{args}

Setup Env
     Log  preparing env

Teardown Env
     Log  cleaning env

Case setup
     Log  case setup

Case teardown
     Log  case teardown

```
