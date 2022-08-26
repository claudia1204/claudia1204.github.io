---
layout: post
title:  "socket 编程：大小端数据"
date:   2022-03-29 20:40:41 +0800
categories: socket
tags: socket

---




# 大小端
数据：0X12345678

内存地址从低到高

     0x0001    0x0002   0x0003  0x0004

大端: 0x12      0x34     0x56    0x78                                高位数据在低位地址

小端: 0x78      0x56     0x34    0x12                                低位数据在低位地址


由于发送端接送端主机可能存在主机序列模式不同，故发送出去数据时，统一转换为大端发送，接收端可统一按照大端解析。网络字节序统一为大端序。

常见的网络字节转换函数有：

```
htons()  #host to network short，将short类型数据从主机字节序转换为网络字节序。

ntohs()  #network to host short，将short类型数据从网络字节序转换为主机字节序。

htonl()  #host to network long，将long类型数据从主机字节序转换为网络字节序。

ntohl()  #network to host long，将long类型数据从网络字节序转换为主机字节序。
```

ref:
[大小端](ttps://www.cnblogs.com/cyx-b/p/12454495.html)
