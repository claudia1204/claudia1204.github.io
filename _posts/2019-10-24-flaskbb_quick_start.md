---
layout: post
title:  "FlaskBB guide"
date:   2019-10-24 19:29:41 +0800
categories: flaskbb forum
---


## clone and start:

```
git clone https://github.com/sh4nks/flaskbb.git
cd flaskbb
git checkout 2.0.0
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
flaskbb makeconfig
flaskbb --config flaskbb.cfg install
flaskbb --config flaskbb.cfg run
```

##  celery start:

```
pip install celery
celery -A celery_worker.celery --loglevel=info worker -E -f celery.logs
```

## redis-server

```
brew install redis-server
redis-server
```

## db: sqlite3
gui: db browser for sqlite


## develop and deploy
develop:
```
flaskbb --config /home/ute/Documents/test_zyt/flaskbb/flaskbb.cfg run --port=8088
```
deploy:
```
gunicorn --bind 0.0.0.0:8088 wsgi:flaskbb --log-file logs/gunicorn.log --pid gunicorn.pid -w 4
```

## ref link
[flaskbb installation](https://flaskbb.org/installation/)

[flask](http://docs.jinkan.org/docs/flask/quickstart.html)

[celery](http://docs.jinkan.org/docs/celery/getting-started/first-steps-with-celery.html#id23)

[redis](https://zhuanlan.zhihu.com/p/37982685)
