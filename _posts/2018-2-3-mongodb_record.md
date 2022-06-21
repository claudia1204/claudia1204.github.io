---
layout: post
title:  "mongodb_test_record"
date:   2018-02-03 19:29:41 +0800
categories: mongodb
---

1.install:
```
brew services stop mongodb
brew uninstall mongodb

brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

2.add account
https://segmentfault.com/a/1190000011554055

```

> mongo
> use admin
switched to db admin
> db.createUser({user:"root",pwd:"123456",roles:['root']})
Successfully added user: { "user" : "root", "roles" : [ "root" ] }
> db.auth('root','123456')
1
> use osr_web
switched to db osr_web
> db.createUser({user:"root",pwd:"1234567",roles:[{role:"readWrite",db:"osr_web"}]})
Successfully added user: {
	"user" : "root",
	"roles" : [
		{
			"role" : "readWrite",
			"db" : "osr_web"
		}
	]
}
> use osr_user
switched to db osr_user
> db.createUser({user:"root",pwd:"1234567",roles:[{role:"readWrite",db:"osr_user"}]})
Successfully added user: {
	"user" : "root",
	"roles" : [
		{
			"role" : "readWrite",
			"db" : "osr_user"
		}
	]
}
> use osr_sys
switched to db osr_sys
> db.createUser({user:"root",pwd:"1234567",roles:[{role:"readWrite",db:"osr_sys"}]})
Successfully added user: {
	"user" : "root",
	"roles" : [
		{
			"role" : "readWrite",
			"db" : "osr_sys"
		}
	]
}
```

