# -*- coding: utf-8 -*-

from django.dispatch import Signal

delete_hit_count = Signal(providing_args=['save_hitcount'])
