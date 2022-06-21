---
layout: post
title:  "libimobiledevice guide to control iphone"
date:   2021-09-22 20:01:11 +0800
categories: appium
---



[libimobiledevice github doc](https://github.com/libimobiledevice/libimobiledevice)


## step1 install libimobiledevice


```
    brew update
    brew uninstall --ignore-dependencies libimobiledevice
    brew uninstall --ignore-dependencies usbmuxd
    brew install --HEAD usbmuxd
    brew unlink usbmuxd
    brew link usbmuxd
    brew install --HEAD libimobiledevice
    git clone https://github.com/JonGabilondoAngulo/idevicelocation.git
    cd idevicelocation
    ./autogen.sh
    make
    sudo make install
```


## step2 commands test
connect iphone to mac with usb, use commands from libimobiledevice api.
```
ideviceinfo -k ProductVersion
12.2.3
```

2) copy dmg from xcode(DeveloperDiskImage.dmg          and DeveloperDiskImage.dmg.signature) to your folder(e.g. ~/Documents/xxx/ios/).
folder path: ```Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/DeviceSup‌​port/7.1/```

3) ideviceimagemounter ~/Documents/xxx/ios/DeveloperDiskImage.dmg
```
base) zhaoting@M-C02Q90LGFVH6:~/test/ideviceactivate/libideviceactivation$ ideviceimagemounter ~/Documents/xxx/ios/DeveloperDiskImage.dmg
Uploading /Users/zhaoting/Documents/xxx/ios/DeveloperDiskImage.dmg
done.
Mounting...
Done.
Status: Complete
```

4) get app installed: ```ideviceinstaller -l```
```
(base) zhaoting@M-C02Q90LGFVH6:~/test/ideviceactivate/libideviceactivation$ ideviceinstaller -l
CFBundleIdentifier, CFBundleVersion, CFBundleDisplayName
com.skyjos.ftpmanagerfree, "6201", "FTPManager"
com.xxx.ultracaller, "13", "ultracaller"
```

5) run app 
```
(base) zhaoting@M-C02Q90LGFVH6:~/test/ideviceactivate/libideviceactivation$ idevicedebug run com.xx.xxx
ERROR: Unspecified
```


6) observing notifications

https://github.com/libimobiledevice/libimobiledevice/issues/464

notification list:http://iphonedevwiki.net/index.php/SpringBoard.app/Notifications


command: ```idevicenotificationproxy observe "com.apple.springboard.lockcomplete"```
```
(base) zhaoting@M-C02Q90LGFVH6:~/test/ideviceactivate/libideviceactivation$ idevicenotificationproxy observe "com.apple.springboard.lockcomplete"
! observing "com.apple.springboard.lockcomplete"
> com.apple.springboard.lockcomplete
> com.apple.springboard.lockcomplete
^CExiting...
```

7) restart iphone
```
idevicediagnostics restart
```

8）airplane mode

seems can not set airplane with libmobiledevice command, but we can set it by ios automation test framework like appium. pls ref [appium mac config guide]({% post_url 2021-9-20-appium_mac_config_guide %})
