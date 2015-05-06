Django-HitCount
===============

Basic app that allows you to track the number of hits/views for a particular
object.

*Update 05/15/2015:* I've finally had some time to integrate some changes
and get it up to Django 1.8.x speed.  Unfortunately, when I first wrote this app
I didn't write any unnittests.  I would love to remedy that.  In the meantime
I do have an example_project that I have added to exhibit the basic functionality.

A pre-1.8 (much older!) version was tagges `0.2`; I've bumped the version to 1.0
in case we've introduced any backwards incompatible changes.

For more information you can view comments in the source code or visit:

<http://blog.damontimm.com/django-hitcount-app-count-hits-views/>

What it is not
--------------

This is not meant to be a user tracking app (see: [django-tracking][1]) or a
comprehensive site traffic monitoring tool (see: Google Analytics).

It's meant to serve as a simple hit counter for chosen objects with a couple
useful features (user-agent, session, and IP tracking) and tools to help you
on your way.

Installation:
-------------

Simplest way to formally install is to run:

    ./setup.py install

Or, you could do a PIP installation:

    pip install -e git://github.com/thornomad/django-hitcount.git#egg=django-hitcount

Or, you can link the source to your `site-packages` directory.  This is useful
if you plan on pulling future changes and don't want to keep running
`./setup.py install`.

    cd ~/src
    git clone git://github.com/thornomad/django-hitcount.git
    sudo ln -s `pwd`/django-hitcount/hitcount `python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`/hitcount

Special thanks to ariddell for putting the `setup.py` package together.

Example Project:
----------------

I have added an example project.  You can use that to test the functionality and
it should work out of the box with Django 1.8 and Python 2.7.x.

You can load some initial fixtures at:

    python manage.py migrate
    python manage.py loaddata initial_data.json
    python manage.py createsuperuser

Contribute
----------

I would love to make it better.  Please fork and push.  Some fun additions
might be [1] a nice graphing utility for the admin site, [2] another approach
to capturing a hit (other than jQuery).

[1]:http://code.google.com/p/django-tracking/


