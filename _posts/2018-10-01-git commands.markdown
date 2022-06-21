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



ssh-keygen -t rsa -f ~/.ssh/id_rsa.test  #generate rsa file
```

## git problems
1  RPC failed

error msg:
error: RPC failed; curl 56 OpenSSL SSL_read: Connection was reset, errno 10054

solution:
``` linux
git config --global http.postBuffer 524288000
```

## gitlab api commands
```
   curl --header "PRIVATE-TOKEN: xxxxxxxxxxxxxx" https://gitlab.xx.xxxxxx.com/api/v4/projects/111/repository/branches
```
