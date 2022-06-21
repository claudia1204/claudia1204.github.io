---
layout: post
title:  "install cygwin and ssh service on windows record"
date:   2020-01-20 16:29:41 +0800
categories: cygwin
---



## 1. install ssh server(cygwin) on Windows
1) download **setup-x86_64.exe** on [cygwin.com](https://cygwin.com/install.html)

2) run  setup-x86_64.exe and setup as follow steps, click next until to select packages.

![install cygwin](/images/cygwin/open_file.PNG){: width="450"}

ps: if pc can not get access to internet, can chose local(you should download all instalation files to this pc)

ps: openssh default is not selected ,you should select version and bin/src file to be installed.
    if you want to use zip、unzip command in cygwin，you can select as same way as next:

3) finished installation

## 2. config ssh by cygwin on Windows

1) open cygwin terminal
   
2) input command: 
   <code>ssh-host-config</code>

3) type yes until CYGWIN value: input netsec tty
   
4) input a username according to your configuration. here we use 'cv5g1_2'
   
5) enter password
   
6) finish the configuration 


## 3. start service of ssh
1) open cygwin terminal
   
2) input command :
**<code>net start sshd</code>** 
   
3) wait for successful message


## 4. test
find a pc and input **<code>ssh  usernmame@ip</code>** ,test over

## problem solution
1) if there is some error made in ssh configuration , you can use the following commands:

   **<code>sc delete sshd</code>**

   **<code>ssh-host-config</code>**

2) net start sshd failed
check whether there is another ssh server running or check /etc/config_sshd, config "AllowUsers myusername" in the config_sshd file.
