---
layout: post
title:  "tcp三次握手连接+四次挥手断开"
date:   2022-04-23 20:20:41 +0800
categories: tcp network
---

学习tidevice启动webdriveragent的过程中正好想到用wireshark抓包看一下tcp三次握手四次断开流程。
## 三次握手

![3_times_handshake](/images/tcp/tcp_3_way_handshake.PNG)
备注：此图来源于https://segmentfault.com/a/1190000039165592

一些标志符意义：
SYN: 连接请求
ACK: 确认报文段
seq: 报文序号
ack： 期望收到的下一个字节号

![1](/images/tcp/tcp_0.PNG)
![2](/images/tcp/tcp_1.PNG)
![3](/images/tcp/tcp_2.PNG)

| 序列号     | client                | 数据流向     |  server                     | 备注                                                    |
|---------|-------------------------|------------|------------------------------|-------------------------------------------------------|
| step1   | SYN=1, seq=x            | ----->     |                              | client发起建立连接请求，server监听端口数据，接收到请求                     |
| step2   |                         | <-----     | SYN=1, ACK=1, seq=y, ack=x+1 | server发送报文给client，接收到连接请求，确认建立连接，期望client下一个x+1序列号的报文 |
| step3   | ACK=1, seq=x+1, ack=y+1 | ----->     |                              | client接收到报文后，回复确认连接，期望server端下一个y+1序列号的报文             |
备注：我们抓包的x和y此时都是为0

建立连接后tcp端发送数据如图：
PSH=1, client端发送显示所有设备信息

![data](/images/tcp/tcp_req_list_devices.PNG)

server返回设备信息

![data](/images/tcp/tcp_return_devices.PNG)

## 四次挥手

![4_times_close](/images/tcp/tcp_4_times_close.PNG){: width="713" }

备注：图片来源 [tcp 4 times close](https://wiki.wireshark.org/TCP-4-times-close.md)

| client |    arrow     |    server | 备注 |
| :-------------------------:| :----: | :----: | :---- |
|FIN=1, seq=x  | -----> |  | client发起断开连接请求，server监听端口数据，接收到请求 |
|&nbsp;  | <----- | ACK=1, seq=y, ack=x+1 <br/>FIN=1, ACK=1, seq=z, ack=x+1 | server发送报文给client，确认接收到请求，期望client下一个x+1序列号的报文 <br/>等待数据传输完毕，断开完成，返回断开FIN=1，确认断开. seq=z, 期待client下一个x+1序列号的报文|
|&nbsp;  | -----> |ACK=1, seq=x+1, ack=z+1|client接收到报文后，回复ACK确认断开完成

备注：我们抓包的x和y,z此时都是为0
![1](/images/tcp/tcp_close.PNG)

## ref

[TCP_3_way_handshaking](https://wiki.wireshark.org/TCP_3_way_handshaking.md)

[TCP-4-times-close](https://wiki.wireshark.org/TCP-4-times-close.md)

[三次握手](https://segmentfault.com/a/1190000039165592)
