from django.core.exceptions import PermissionDenied
from hitcount.models import BlacklistIP, BlacklistUserAgent

def blacklist_ips(modeladmin, request, queryset):
    for obj in queryset:
       ip, created = BlacklistIP.objects.get_or_create(ip=obj.ip)
       if created:
           ip.save()
    msg = "Successfully blacklisedt %d IPs." % queryset.count() 
    modeladmin.message_user(request, msg)
blacklist_ips.short_description = "BLACKLIST the selected IP ADDRESSES"

def blacklist_user_agents(modeladmin, request, queryset):
    for obj in queryset:
       ua, created = BlacklistUserAgent.objects.get_or_create(
                        user_agent=obj.user_agent)
       if created:
           ua.save()
    msg = "Successfully blacklisted %d User Agents." % queryset.count() 
    modeladmin.message_user(request, msg)
blacklist_user_agents.short_description = "BLACKLIST the selected USER AGENTS"

def delete_queryset(modeladmin, request, queryset):
    # TODO 
    #
    # Right now, when you delete a hit there is no warning or "turing back".
    # Consider adding a "are you sure you want to do this?" as is 
    # implemented in django's contrib.admin.actions file.

    if not modeladmin.has_delete_permission(request):
        raise PermissionDenied
    else:
        if queryset.count() == 1:
            msg = "1 hit was"
        else:
            msg = "%s hits were" % queryset.count()

        for obj in queryset.iterator():
            obj.delete() # calling it this way to get custom delete() method

        modeladmin.message_user(request, "%s successfully deleted." % msg)
delete_queryset.short_description = "DELETE selected hits"

def blacklist_delete_ips(modeladmin, request, queryset):
    blacklist_ips(modeladmin, request, queryset)
    delete_queryset(modeladmin, request, queryset)
blacklist_delete_ips.short_description = "DELETE the selected hits and " + \
                                         "BLACKLIST the IP ADDRESSES"

def blacklist_delete_user_agents(modeladmin, request, queryset):
    blacklist_user_agents(modeladmin, request, queryset)
    delete_queryset(modeladmin, request, queryset)
blacklist_delete_user_agents.short_description = "DELETE the selected hits " + \
                                            "and BLACKLIST the USER AGENTS"

