---
layout: post
title:  "tidevice的魔法： 跨平台吊起webdriver agent runner源码学习"
date:   2022-04-22 19:40:41 +0800
categories: webdriver
---





根据[tidevice git](https://github.com/alibaba/taobao-iphone-device)文档 ,tidevice可以实现跨平台(windows/linux/mac)自动化测试。

在windows上，tidevice可以脱离Xcode唤起ios上已经安装好的webdriveragent runner app。

tidevice是怎么实现脱离Xcode吊起webdriver agent runner的呢？让我们来读一读源码。

由一条命令```tidevice wdaproxy -B com.facebook.wda.WebDriverAgent.Runner --port 8200```开始。


## 端口汇总和基本原理 ##

后续会有很多端口用到，这里拉出来前面说明下，避免后面看到的时候有点蒙：

***27015***：   usbmux（127.0.0.1:27015）

***62078***：   LOCKDOWN_PORT， ios 上的lockdown service，参见后者 lockdown

***32498***：   socket.htons(62078) = 32498   lockdown_port转换为网络字节端口的结果，[socket编程中的大端小端]({% post_url 2022-3-29-socket_little_endian_big_endian %})


***8200,8100***： 8200（relay: tcp server, listen 8200）<----->  8100 device(webdriveragent app: /screenshot)
            后续会看到tidevice启动了一个端口转发的server，将pc端的8200数据转发到了ios设备8100端口
            linux上有类似工具包[iproxy](https://linuxcommandlibrary.com/man/iproxy)

***42015***：    socket.htons(8100) = 42015    webdriveragent runner监听的端口8100转换为网络字节端口。

    

### webdriveragent runner
webdriveragent runner app是什么？由facebook提供的ios上可安装的webdriver server。该server启动后在iphone上监听一个端口（例如8100），接收指令来实现对ios设备的远程控制，如打开/安装/卸载其他app，截屏，通过settings设置手机，点击等等。

webdriveragent runner app: 本质是链接XCTest.framework调用苹果API直接执行命令，实现自动化测试的目的。Facebook的webdriver agent runner 已经停止维护，建议由appium的[webdriveragent in appium github](https://github.com/appium/WebDriverAgent)下载。
具体webdriver agent runner安装详细参见blog[appium mac config guide]({%post_url 2021-9-20-appium_mac_config_guide %})中的webdriver agent runner安装部分。

appium + webdriveragent_runner也是一种常见的移动端自动化测试方案。我们这里探讨tidevice+webdriveragent_runner。

### lockdown service 
[lockdown service介绍](https://gist.github.com/ddz/b6879ba86fc7ddc2e26f)

[lockdown service介绍2](https://www.theiphonewiki.com/wiki/Usbmux#lockdownd_protocol)

lockdown 服务是ios上的守护进程，提供ios系统信息以及使用一些services.例如app的安装，手机备份，重装等。它需要root权限运行.
使用lockdown service需要建立通过usb或者网络与ios设备建立一个SSL连接，连接过程中需要授权使用ios设备配对的一些keys。

### usbmux 
usbmux是啥？itunes和iPhone通过usbmux进行通信。
windows上iTunes能控制iPhone并且进行软件卸载，备份等就是通过的这个"usbmux"协议. about it, please see [usbmux intro ref](https://www.theiphonewiki.com/wiki/Usbmux)


### instruments  
源代码码中不乏instruments的身影.instruments 是什么?

根据dtxmsg格式
[dtx msg](https://github.com/troybowman/dtxmsg/blob/master/slides.pdf)

[中文版dtxmsg, dtx msg](https://bbs.pediy.com/thread-246139.htm)

![instrument](/images/ios/instrument.PNG){: width="713" }
图片来源于以上dtx msg博文

[wwdc关于instruments的介绍](https://developer.apple.com/videos/play/wwdc2019/411/)

我们了解到:

instruments是一个由Apple开发的一系列调试工具集,集合于Xcode:

时间耗时检测

泄露检测

跟踪文件 I/O

Apple实现了OSX上运行的一个用于提供iOS调试分析的server

### 前置知识总结
根据理解画了幅图如下
![tidevice通信](/images/ios/tidevice_communication.PNG){: width="713" }


step 1 .

tidevice 在pc上开启了一个tcp转发服务器，用于转发pc端8200数据到ios端8100数据。

tidevice和pc上（windows安装itunes获得， mac上自带）的usbmuxd进行通信，启动ios上lockdown/instrument相关服务,模拟xcode通信吊起webdriver agent runner



step 2.

tidevice发api命令（有统一的restful api标准定义）给（监听8200的）tcp server， server转发给ios上（监听8100的）webdriveragent runner， webdriveragent runner接受api，调用xctest框架实现自动化控制。


-----------------------------------

## 程序入口
setup.cfg中设定了入口为tidev中的__main__里的main函数
```
[entry_points]
console_scripts = 
    tidevice = tidevice.__main__:main
```

main()中本质是调用Usbmux生成了um对象，负责usbmux相关的通信。usbmux是啥？一个实现了usb连接的iPhone设备和pc端间，以类似tcp进行通信的系统。具体参见[usbmux study]({% post_url 2022-4-21-usbmux %})
```
    um = Usbmux(args.socket)
    actions[args.subparser](args) # actually called: def cmd_wdaproxy(args: argparse.Namespace)
```


cmd_wdaproxy在这里干了两件事: 
1. 启动一个tcpserver: 实现端口转发 8200 <---> 8100, like [iproxy](https://www.mankier.com/1/iproxy)，通过给pc端8200发数据，转发到ios上的8100，也就是webdriver agent runner所监听的端口
2. 启动 WDAService, 开启 webdriveragent runner
```
    if args.port:
        cmds = [
            sys.executable, '-m', 'tidevice', '-u', d.udid, 'relay',
            str(args.port), '8100'
        ]
        p = subprocess.Popen(cmds, stdout=sys.stdout, stderr=sys.stderr)
    
    ...
    
    serv = WDAService(d, args.bundle_id, env) # start webdriveragent runner
    ...
    serv.start()
```

WDAService实际调用子进程，执行tidevce xctest命令 ```subprocess.Popen("python -m tidevice -u {udid} xctest --bundle_id {bundle_id}")"

xctest里我理解就是对Xcode和iPhone的通信过程进行了逆向工程,模拟其Xcode通信的流程和数据，驱动xctest project start，可以看到核心代码如下:

```

    ## IDE 1st connection
    ##

    x1 = self._connect_testmanagerd_lockdown()    #通过usbmux连接 com.apple.testmanagerd.lockdown服务
    data = s.send_recv_packet({
                    "Request": "StartService",
                    "Service": name,
                    "Label": PROGRAM_NAME,
                })
    x1_daemon_chan = x1.make_channel(
        'dtxproxy:XCTestManager_IDEInterface:XCTestManager_DaemonConnectionInterface' #创建channel
    )
    identifier = '_IDE_initiateControlSessionWithProtocolVersion:'
    aux = AUXMessageBuffer()
    aux.append_obj(XCODE_VERSION)
    x1.call_message(x1_daemon_chan, identifier, aux) #对channel发送对应的二进制数据


    ##
    ## IDE 2nd connection
    x2 = self._connect_testmanagerd_lockdown()
    x2_deamon_chan = x2.make_channel(
        'dtxproxy:XCTestManager_IDEInterface:XCTestManager_DaemonConnectionInterface'
    )
    x2.register_callback(Event.FINISHED, lambda _: quit_event.set())
    #
    identifier = '_IDE_initiateSessionWithIdentifier:forClient:atPath:protocolVersion:'
    aux = AUXMessageBuffer()
    aux.append_obj(session_identifier)
    aux.append_obj(str(session_identifier) + '-6722-000247F15966B083')
    aux.append_obj(
        '/Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild')
    aux.append_obj(XCODE_VERSION)
    result = x2.call_message(x2_deamon_chan, identifier, aux)


    ###launch app
    xctest_path = f"/tmp/{target_name}-{str(session_identifier).upper()}.xctestconfiguration"  # yapf: disable
    xctest_content = bplist.objc_encode(bplist.XCTestConfiguration({
        "testBundleURL": bplist.NSURL(None, f"file://{app_info['Path']}/PlugIns/{target_name}.xctest"),
        "sessionIdentifier": session_identifier,
        "targetApplicationBundleID": target_app_bundle_id,
    }))  # yapf: disable

    # service: com.apple.instruments.remoteserver
    conn = self.connect_instruments() # start service "com.apple.instruments.remoteserver.DVTSecureSocketProxy"  # for iOS 14.0
    channel = conn.make_channel(InstrumentsService.ProcessControl)
    conn.call_message(channel, "processIdentifierForBundleIdentifier:",
                      [bundle_id])
    pid = conn.call_message(
        channel, identifier,
        [app_path, bundle_id, app_env, app_args, app_options])
```

流程总结：
  流程中我们看到#1 和#2 两次启动并且连接lockdown服务，创建channel，通过channel发送数据进行了初始化控制session的操作（_IDE_initiateControlSessionWithProtocolVersion 和 XCTestManager_IDEInterface:XCTestManager_DaemonConnectionInterface）。
  猜测是Xcode启动ios上对应的xcuitest framework的时候前置初始化操作。#3 吊起webdriver runner app，主要是启动instrument服务（InstrumentsRemoteServer = "com.apple.instruments.remoteserver"），创建channel然后发送DTXMessage启动app.

## 代码流程分步解析

下面来看下方法connect_testmanagerd_lockdown，通过查看代码发现本质是socket连接usbmuxd，通过该connection发送start service指令，启动lockdown service（ssl连接）.

分步骤看下最常见的start service并且连接到该service包含哪些内容。

1 其中启动一次service 完整流程包括

 usbmuxd connection1 ---> connection1 send info:connect---> querType---> GetValue---> StartSession---> StartService---> StopSession

2 开启service后，下次连接，根据返回的信息例如{'EnableServiceSSL': True, 'Port': 53190, 'Request': 'StartService', 'Service': 'com.apple.testmanagerd.lockdown.secure'}信息，connect返回的端口，即可连接该service




```
_connect_testmanagerd_lockdown:
	conn = start_service(LockdownService.TestmanagerdLockdownSecure=com.apple.testmanagerd.lockdown.secure)
		create_session as s:		
				create_inner_connection as s:
						conn = self._usbmux.create_connection()
						conn send ('MessageType': 'Connect', port=LOCKDOWN_PORT)
						return conn
						
					QueryType
					GetValue
					StartSession
					yield s
					StopSession
				
								
		    data = s.send_recv_packet({
                "Request": "StartService",
                "Service": name,
                "Label": PROGRAM_NAME,
            })
				
				
		conn = self.create_inner_connection(data['Port'], _ssl=_ssl, ssl_dial_only=ssl_dial_only)
		return conn
		 
	return DTXService(conn)	 

...
	
    make_channel:
	    result = self.call_message(0, '_requestChannelWithCode:identifier:', aux)
```


#### 一部分log步骤大致如下

As tested form code, follow steps happened during webdriveragent runner app started:
```text
    1. SEND(1): {'MessageType': 'ListDevices', 'ClientVersionString': 'libusbmuxd 1.1.0', 'ProgName': 'tidevice', 'kLibUSBMuxVersion': 3}
    2. send payload: {'DeviceID': 95, 'MessageType': 'Connect', 'PortNumber': 32498, 'ProgName': 'tidevice'} 
    connected to port: 32498    # why here is 32498 instead of 62078? socket.htons(62078) = 32498
    3. "Request": "QueryType"
    {'Request': 'QueryType', 'Type': 'com.apple.mobile.lockdown'}
    
    4. 'Request': 'GetValue'
       {'Key': 'ProductVersion', 'Request': 'GetValue', 'Value': '14.2'}
    
    5. {'MessageType': 'ReadPairRecord', 'PairRecordID': 'bac123dc8ed3a3cdd491ab4e4699f60b136e7bca', 'ClientVersionString': 'libusbmu
    xd 1.1.0', 'ProgName': 'tidevice', 'kLibUSBMuxVersion': 3} 
    
    6. {'Request': 'StartSession', 'HostID': '3096123013660573123119811848', 'SystemBUID': '30961229-7292436981136919796', 'ProgName'
    : 'tidevice'}
       {'EnableSessionSSL': True, 'Request': 'StartSession', 'SessionID': 'A56A6BFD-5D97-4083-8950-4228FA67E29C'}
    
    7. {'Request': 'StartService', 'Service': 'com.apple.mobile.installation_proxy', 'Label': 'tidevice'}
       {'Port': 53184, 'Request': 'StartService', 'Service': 'com.apple.mobile.installation_proxy'}
    
    8. {'Request': 'StopSession'}
       CLOSE
    
    9. {'DeviceID': 95, 'MessageType': 'Connect', 'PortNumber': 49359, 'ProgName': 'tidevice'}
       {'MessageType': 'Result', 'Number': 0}
       connected to port: 49359
    
    10. {'Command': 'Browse', 'ClientOptions': {'ApplicationType': 'User', 'ReturnAttributes': ['CFBundleIdentifier']}}
        {'CurrentIndex': 0, 'CurrentAmount': 10, 'Status': 'BrowsingApplications', 'CurrentList': [{'CFBundleIdentifier': 'x.x.x'}, {'CFBundleIdentifier': 'x.x.x'}, ..., {'CFBundleIdentifier': 'x.x.x'}]}
        RECV(5): {'Status': 'Complete'}
    
    11. {'DeviceID': 95, 'MessageType': 'Connect', 'PortNumber': 32498, 'ProgName': 'tidevice'}
        {'MessageType': 'Result', 'Number': 0}
        connected to port: 32498
    
    12. {'Request': 'QueryType'}
       {'Request': 'QueryType', 'Type': 'com.apple.mobile.lockdown'}
    
    13. {'Request': 'GetValue', 'Key': 'ProductVersion', 'Label': 'tidevice'}
       {'Key': 'ProductVersion', 'Request': 'GetValue', 'Value': '14.2'}
    
    14. {'Request': 'StartSession', 'HostID': '3096123013660573123119811848', 'SystemBUID': '30961229-7292436981136919796', 'ProgName': 'tidevice'}
       {'EnableSessionSSL': True, 'Request': 'StartSession', 'SessionID': '553E60ED-73B1-4E84-AF87-330E59E7B266'}
    
    15. {'Request': 'StopSession', 'ProtocolVersion': '2', 'Label': 'tidevice', 'SessionID': '553E60ED-73B1-4E84-AF87-330E59E7B266'}
       {'Request': 'StopSession'}
       CLOSE(7)
    
    16. {'DeviceID': 95, 'MessageType': 'Connect', 'PortNumber': 42015, 'ProgName': 'tidevice'}
       {'MessageType': 'Result', 'Number': 3}
    
    17. {'Request': 'StartService', 'Service': <LockdownService.TestmanagerdLockdownSecure: 'com.apple.testmanagerd.lockdown.secure'>,
    'Label': 'tidevice'}
       {'EnableServiceSSL': True, 'Port': 53190, 'Request': 'StartService', 'Service': 'com.apple.testmanagerd.lockdown.secure'} 
       备注：开启lockdown service，socket返回需要ssl连接，请连接端口号53190. socket.htons(53190)=50895
    18. {'DeviceID': 95, 'MessageType': 'Connect', 'PortNumber': 50895, 'ProgName': 'tidevice'}
       {'MessageType': 'Result', 'Number': 0}
       connected to port: 50895
       进行连接lockdown(50895),连接成功
    19. SEND DTXMessage: channel:0 expect_reply:0 data_length:619, data...
       SEND DTXMessage: channel:0 expect_reply:1 data_length:478, data...
       RECV DTXMessage: expects_reply:0 flags:2 conv:0 ('_notifyOfPublishedCapabilities:', [{'com.apple.private.DTXBlockCompression': 2, 'com.
    apple.private.DTXConnection': 1}])
       RECV DTXMessage: expects_reply:0 flags:0 conv:1 None
    ...
    20. {'Command': 'Lookup', 'ClientOptions': {'BundleIDs': ['com.facebook.WebDriverAgentRunner.xctrunner']}}
     {'Status': 'Complete', 'LookupResult': {'com.facebook.WebDriverAgentRunner.xctrunner': {'CFBundlePackageType': 'APPL', 'NSCon
    tactsUsageDescription': 'Access is necessary for automated testing.', 'NSBluetoothAlwaysUsageDescription': 'Access is necessary for automated testing.', 'DTPlatformVersion'
    : '14.2', 'DTSDKBuild': '18B58', 'NFCReaderUsageDescription': 'Access is necessary for automated testing.', 'NSSiriUsageDescription': 'Access is necessary for automated tes
    ting.', 'LSRequiresIPhoneOS': True, 'NSCameraUsageDescription': 'Access is necessary for automated testing.', 'ProfileValidated': True, 'CFBundleDisplayName': 'WebDriverAge
    ntRunner-Runner', 'SignerIdentity': 'Apple Development: ...', 'DTXcodeBuild': '12B42a', 'NSRemindersUsageDescription': 'Access is necessary for automat
    ed testing.', 'EnvironmentVariables': {'CFFIXED_USER_HOME': '/private/var/mobile/Containers/Data/Application/D01XX616-XXXX-XXXX-XXXX-7B2749AFC1E6', 'TMPDIR': '/private/var/
    mobile/Containers/Data/Application/D01XX616-XXXX-XXXX-XXXX-7B2749AFC1E6/tmp', 'HOME': '/private/var/mobile/Containers/Data/Application/D01AB616-XXXX-XXXX-XXXX-7B2749AFC1E6'
    }, 'CFBundleNumericVersion': 16809984, 'SequenceNumber': 3604, 'IsDemotedApp': False, 'Path': '/private/var/containers/Bundle/Application/A557E8E0-XXXX-XXXX-XXXX-49A9183F1B
    B3/WebDriverAgentRunner-Runner.app', 'CFBundleIdentifier': 'com.facebook.WebDriverAgentRunner.xctrunner', 'NSHealthClinicalHealthRecordsShareUsageDescription': 'Access is n
    ecessary for automated testing.', 'UIDeviceFamily': [1, 2], 'CFBundleSignature': '????', 'CFBundleInfoDictionaryVersion': '6.0', 'IsUpgradeable': True, 'CFBundleSupportedPl
    atforms': ['iPhoneOS'], 'NSHealthUpdateUsageDescription': 'Access is necessary for automated testing.', 'UIRequiresFullScreen': True, 'NSMotionUsageDescription': 'Access is
    necessary for automated testing.', 'MinimumOSVersion': '9.0', 'NSPhotoLibraryAddUsageDescription': 'Access is necessary for automated testing.', 'CFBundleName': 'WebDriver
    AgentRunner-Runner', 'CFBundleShortVersionString': '1.0', 'UIBackgroundModes': ['continuous'], 'UIRequiredDeviceCapabilities': ['armv7'], 'CFBundleExecutable': 'WebDriverAg
    entRunner-Runner', 'NSHealthShareUsageDescription': 'Access is necessary for automated testing.', 'ApplicationType': 'User', 'NSAppleMusicUsageDescription': 'Access is nece
    ssary for automated testing.', 'NSSpeechRecognitionUsageDescription': 'Access is necessary for automated testing.', 'Container': '/private/var/mobile/Containers/Data/Applic
    ation/D01AB616-FF64-43F1-B9E7-7B2749AFC1E6', 'NSLocationUsageDescription': 'Access is necessary for automated testing.', 'BuildMachineOSBuild': '20A2371', 'NSCalendarsUsage
    Description': 'Access is necessary for automated testing.', 'DTPlatformName': 'iphoneos', 'NSMicrophoneUsageDescription': 'Access is necessary for automated testing.', 'CFB
    undleAllowMixedLocalizations': True, 'NSLocationWhenInUseUsageDescription': 'Access is necessary for automated testing.', 'CFBundleVersion': '1', 'CFBundleDevelopmentRegion
    ': 'en', 'NSFaceIDUsageDescription': 'Access is necessary for automated testing.', 'DTCompiler': 'com.apple.compilers.llvm.clang.1_0', 'NSLocationAlwaysAndWhenInUseUsageDes
    cription': 'Access is necessary for automated testing.', 'NSHomeKitUsageDescription': 'Access is necessary for automated testing.', 'DTSDKName': 'iphoneos14.2.internal', 'N
    SAppTransportSecurity': {'NSAllowsArbitraryLoads': True}, 'Entitlements': {'keychain-access-groups': ['T3TLXX99XX.com.facebook.WebDriverAgentRunner.xctrunner'], 'applicatio
    n-identifier': 'T3TLXX99XX.com.facebook.WebDriverAgentRunner.xctrunner', 'get-task-allow': True, 'com.apple.developer.team-identifier': 'T3TLXX99XX'}, 'DTPlatformBuild': '1
    8B58', 'NSPhotoLibraryUsageDescription': 'Access is necessary for automated testing.', 'IsAppClip': False, 'UISupportedInterfaceOrientations': ['UIInterfaceOrientationPortr
    ait', 'UIInterfaceOrientationLandscapeLeft', 'UIInterfaceOrientationLandscapeRight'], 'DTXcode': '1220'}}}
  
```
 
   




## 参考
[understanding-usbmux-and-the-ios-lockdown-service](https://jon-gabilondo-angulo-7635.medium.com/understanding-usbmux-and-the-ios-lockdown-service-7f2a1dfd07ae)

[iphonewiki: Usbmux](https://www.theiphonewiki.com/wiki/Usbmux)

[tidevice intro](https://testerhome.com/topics/27159)
