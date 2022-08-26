--- 
layout: post
title:  "ssh commands study"
date:   2020-5-1 22:00:41 +0800
categories: ssh proxy
tags: ssh

---


## ssh with proxy ##

```
ssh  -o 'ProxyCommand=ssh  username@jumpserver nc jumpserver 22' root@remoteserver

ssh -tt CNHZ5GRAN1133+tester@10.57.152.85 ssh -tt root@10.57.157.83
```

## useful links
[difference-between-ssh-proxycommand-w-nc-exec-nc](https://stackoverflow.com/questions/22635613/what-is-the-difference-between-ssh-proxycommand-w-nc-exec-nc)
![difference between ssh proxycomamnd ](/images/ssh_proxy.png){: width="450" style="margin-left:0"}

