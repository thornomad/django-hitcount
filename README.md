*NOTE* (02/23/2013) - I have not been actively maintaining this app (as anyone
can tell from my levels of participation these last few years).  I apologize
for that because I, myself, hate seeing open source solutions fade with time.
To that end, I would prefer to point people to an active fork of the project.
If you have a fork, or know of a good fork to use, please let me know and I
will post the links/recommendations here.  It's been fun sharing. -Damon

Django-HitCount
===============

Basic app that allows you to track the number of hits/views for a particular
object.

For more information you can view comments in the source code or visit:

<http://damontimm.com/code/django-hitcount/>

What it is not
--------------

This is not meant to be a user tracking app (see: [django-tracking][1]) or a
comprehensive site traffic monitoring tool (see: Google Analytics).

It's meant to serve as a simple hit counter for chosen objects with a couple
useful features (user-agent, session, and IP tracking) and tools to help you
on your way.

Contribute
----------

I would love to make it better.  Please fork and push.  Some fun additions
might be [1] a nice graphing utility for the admin site, [2] another approach
to caputring a hit (other than jQuery), and [3] a cleanup tool that can remove
Hit objects after a certain period (cron job).

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

[1]:http://code.google.com/p/django-tracking/


