# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.exceptions import PermissionDenied

from .models import Hit, HitCount, BlacklistIP, BlacklistUserAgent


class HitAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'ip', 'user_agent', 'hitcount')
    search_fields = ('ip', 'user_agent')
    date_hierarchy = 'created'
    actions = ['blacklist_ips',
               'blacklist_user_agents',
               'blacklist_delete_ips',
               'blacklist_delete_user_agents',
               'delete_queryset',
               ]

    def __init__(self, *args, **kwargs):
        super(HitAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None,)

    def get_actions(self, request):
        actions = super(HitAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def blacklist_ips(self, request, queryset):
        for obj in queryset:
           ip, created = BlacklistIP.objects.get_or_create(ip=obj.ip)
           if created:
               ip.save()
        msg = "Successfully blacklisedt %d IPs." % queryset.count()
        self.message_user(request, msg)
    blacklist_ips.short_description = "BLACKLIST the selected IP ADDRESSES"

    def blacklist_user_agents(self, request, queryset):
        for obj in queryset:
           ua, created = BlacklistUserAgent.objects.get_or_create(
                            user_agent=obj.user_agent)
           if created:
               ua.save()
        msg = "Successfully blacklisted %d User Agents." % queryset.count()
        self.message_user(request, msg)
    blacklist_user_agents.short_description = "BLACKLIST the selected USER AGENTS"

    def blacklist_delete_ips(self, request, queryset):
        self.blacklist_ips(request, queryset)
        self.delete_queryset(request, queryset)
    blacklist_delete_ips.short_description = "DELETE the selected hits and " + \
                                             "BLACKLIST the IP ADDRESSES"

    def blacklist_delete_user_agents(self, request, queryset):
        self.blacklist_user_agents(request, queryset)
        self.delete_queryset(request, queryset)
    blacklist_delete_user_agents.short_description = "DELETE the selected hits " + \
                                                "and BLACKLIST the USER AGENTS"

    def delete_queryset(self, request, queryset):
        if not self.has_delete_permission(request):
            raise PermissionDenied
        else:
            if queryset.count() == 1:
                msg = "1 hit was"
            else:
                msg = "%s hits were" % queryset.count()

            for obj in queryset.iterator():
                obj.delete() # calling it this way to get custom delete() method

            self.message_user(request, "%s successfully deleted." % msg)
    delete_queryset.short_description = "DELETE selected hits"

admin.site.register(Hit, HitAdmin)


class HitCountAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'hits', 'modified')
    fields = ('hits',)

admin.site.register(HitCount, HitCountAdmin)


class BlacklistIPAdmin(admin.ModelAdmin):
    pass

admin.site.register(BlacklistIP, BlacklistIPAdmin)


class BlacklistUserAgentAdmin(admin.ModelAdmin):
    pass

admin.site.register(BlacklistUserAgent, BlacklistUserAgentAdmin)
