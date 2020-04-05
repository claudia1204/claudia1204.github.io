---
layout: post
title:  "solve the Problems with X11 - Can't open display on MAC"
date:   2020-01-01 16:29:41 +0800
categories: mac
---

how to solve the Problems with X11 - Can't open display on MAC
=======

how to solve the Problems with X11 - Can't open display on MAC

1. do commands on  mac:
```
defaults write com.apple.x11 nolisten_tcp -boolean false
defaults write org.X.x11 nolisten_tcp -boolean false
```

2. install xquartz
download and install from https://www.xquartz.org/


3. open xterm in xquartz and ssh to your target pc
```
ssh -X root@x.x.x.x
firefox #do your commands to start a gui app
```

thanks solution from Robert Jansen's comments in https://discussions.apple.com/thread/2048176