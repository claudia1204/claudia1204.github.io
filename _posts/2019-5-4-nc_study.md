--- 
layout: post
title:  "nc study"
date:   2019-5-4 12:00:41 +0800
categories: linux command netcat
---


[ref link](https://blog.csdn.net/wang7dao/article/details/7684998)

[ref link2](https://cloud.tencent.com/developer/article/1493030)


## nc demo
assume: A(1.1.1.1) to B(2.2.2.2)


### nc demo1: nc copy file:
copy file(test.log) from A(1.1.1.1) to B(2.2.2.2)


step1: start nc to monitoring data on B
      nc -lp 1234 > test.log


step2: use nc make connection with B on A
      nc -w 1 2.2.2.2 1234 < test.log
      
### nc demo2:  chat with nc
1) A communicate with B, input command on B:
      nc -lp 1234

2) input command on A:
      nc 2.2.2.2 1234      

3) chat by nc, enjoy



##  flow of "<" and ">"

```
command < file  # file to command
command < file1 > file2  # file1 to command, the result of command to file2
echo "This is my data" > /dev/udp/127.0.0.1/3000
```

## ncat 
```
dpkg -l | egrep netcat
nc.traditional -h
/usr/bin/ncat
```
