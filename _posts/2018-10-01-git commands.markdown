---
layout: post
title:  "git commands record"
date:   2018-10-01 16:29:41 +0800
categories: git
---


```
git config user.name "username"
git config user.email "mail"

git remote -v       #show remote git repository
git remote add origin git://github.com/username/test.git
git pull --allow-unrelated-histories   #solve allow-unrelated-histories problems

git remote set-url origin https://github.com/user/repo2.git



ssh-keygen -t rsa -f ~/.ssh/id_rsa.test  -C "your_email@example.com"  #generate rsa file
```

## git problems
1  RPC failed

error msg:
error: RPC failed; curl 56 OpenSSL SSL_read: Connection was reset, errno 10054

solution:
``` linux
git config --global http.postBuffer 524288000
```

2 Error in the HTTP2 framing layer

fatal: unable to access 'https://github.com/claudia1204/claudia1204.github.io.git/': Error in the HTTP2 framing layer

```
git config --global --unset http.proxy
git config --global --unset https.proxy
```

3 TTP/2 stream 1 was not closed cleanly before end of the underlying stream
fatal: unable to access 'https://github.com/claudia1204/claudia1204.github.io.git/': HTTP/2 stream 1 was not closed cleanly before end of the underlying stream

```
git config --global http.version HTTP/1.1
```

## gitlab api commands
```
   curl --header "PRIVATE-TOKEN: xxxxxxxxxxxxxx" https://gitlab.xx.xxxxxx.com/api/v4/projects/111/repository/branches
```
