*NOTE* (02/23/2013) - I have not been actively maintaining this app (as anyone
can tell from my levels of participation these last few years).  I apologize
for that because I, myself, hate seeing open source solutions fade with time.
To that end, I would prefer to point people to an active fork of the project.
If you have a fork, or know of a good fork to use, please let me know and I
will post the links/recommendations here.  It's been fun sharing. -Damon

Django-HitCount
===============

Простое приложение для отслеживания просмотров объекта в Django.
Счетчик посещений для нужных объектов запоминает браузер, сессию, ip

Установка:
-------------
### Просто копи-пейст
    git clone git://github.com/Gasoid/django-hitcount.git
    sudo ln -s `pwd`/django-hitcount/hitcount `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`/hitcount

### Добавляем hitcount в настройки django
    INSTALLED_APPS = (
        ...
        'hitcount',
    )

### Добавляем параметры в settings.py
    HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 7 }
    HITCOUNT_HITS_PER_IP_LIMIT = 0
    HITCOUNT_EXCLUDE_USER_GROUP = ( 'Editor', )

HITCOUNT_KEEP_HIT_ACTIVE: это количество дней, недель, месяцев, часов и т.д. в течение которых просмотр считается активным, повторный просмотр не считается

HITCOUNT_HITS_PER_IP_LIMIT: ограничение на количество просмотров с одного IP адреса. 0 - нет ограничений

HITCOUNT_EXCLUDE_USER_GROUP: не считать определенные юзер-группы

### Изменения в urls.py
    from django.conf.urls.defaults import *
    from django.views.generic.list_detail import object_detail
    from hitcount.views import update_hit_count_ajax
    
    urlpatterns = patterns('',
        ...
        url(r'^ajax/hit/$', # можно изменить на нужный урл
            update_hit_count_ajax,
            name='hitcount_update_ajax'), # name не изменять
        ... 
    )

### Шаблоны
Считаем посещение объекта page

    <script src="/media/js/jquery-latest.js" type="text/javascript"></script>
    {% with object=page  %}
      {% include "hitcount.html" %}
    {% endwith %}


### Вывод хитов в шаблонах
    - Показать все хиты объекта:
    {% get_hit_count for [object] %}
    
    - Показать все хиты объекта использовав переменную:
    {% get_hit_count for [object] as [var] %}
    
    - Показать хиты объекта за определенный период:
    {% get_hit_count for [object] within ["days=1,minutes=30"] %}
    
    - Показать хиты объета за определенный период использовав переменную:
    {% get_hit_count for [object] within ["days=1,minutes=30"] as [var] %}
