---
layout: post
title:  "django quick start"
date:   2018-01-20 19:29:41 +0800
categories: css
---



1. install python
2. install django
   check django version:
   
```
pip install django
python -m django --version
```

3. create a project by django
   ```django-admin startproject mysite```

4. django project
   ![mysite](/images/django/mysite.png){:style="margin-left:1px"}

   mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py


5. run server :```python manage.py runserver```

6. python manage.py startapp polls
   ![polls](/images/django/polls.png){:style="margin-left:1px"}

7. create first view in polls/views.py:
```
    from django.http import HttpResponse
	def index(request):
	    return HttpResponse("Hello, world. You're at the polls index.")
```
8. polls/urls.py
```
	from django.urls import path
	from . import views
	urlpatterns = [
	    path('', views.index, name='index'),
	]
```
9. 	mysite/urls.py
```
	from django.contrib import admin
	from django.urls import include, path

	urlpatterns = [
	    path('polls/', include('polls.urls')),
	    path('admin/', admin.site.urls),
	]
```
10.  ```python manage.py runserver```

11.  If you want to use Django on a production site, use Apache with mod_wsgi.





