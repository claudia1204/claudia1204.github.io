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


git credential-osxkeychain erase
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

3 HTTP/2 stream 1 was not closed cleanly before end of the underlying stream
fatal: unable to access 'https://github.com/claudia1204/claudia1204.github.io.git/': HTTP/2 stream 1 was not closed cleanly before end of the underlying stream

```
git config --global http.version HTTP/1.1
```

4  'github.com (140.82.112.3)' can't be established
The authenticity of host 'github.com (140.82.112.3)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
This key is not known by any other names


git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.


solution:
solution from [solution of permission denied](https://blog.csdn.net/YanceChen2013/article/details/82218356)
ssh -v git@github.com
....
debug1: No more authentication methods to try.
git@github.com: Permission denied (publickey).


ssh-agent -s
SSH_AUTH_SOCK=/var/folders/rm/qsy1smdx3ls7pn3cd3rkdj840000gn/T//ssh-89Ngxttynm2J/agent.98164; export SSH_AUTH_SOCK;
SSH_AGENT_PID=98165; export SSH_AGENT_PID;
echo Agent pid 98165;

ssh-add ~/.ssh/id_rsa.test
Identity added: /Users/xxxx/.ssh/id_rsa.test (xxxxx@gmail.com)

ssh -T git@github.com
Hi xxxx! You've successfully authenticated, but GitHub does not provide shell access.


## gitlab api commands
```
   curl --header "PRIVATE-TOKEN: xxxxxxxxxxxxxx" https://gitlab.xx.xxxxxx.com/api/v4/projects/111/repository/branches
```
