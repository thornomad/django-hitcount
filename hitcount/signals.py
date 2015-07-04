# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.dispatch import Signal

delete_hit_count = Signal(providing_args=['save_hitcount'])
