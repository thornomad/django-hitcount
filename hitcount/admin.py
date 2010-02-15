from django.contrib import admin

from hitcount.models import Hit, HitCount, BlacklistIP, BlacklistUserAgent
from hitcount import actions

def created_format(obj):
    '''
    Format the created time for the admin. PS: I am not happy with this.
    '''
    return "%s" % obj.created.strftime("%m/%d/%y<br />%H:%M:%S")
created_format.short_description = "Date (UTC)"
created_format.allow_tags = True
created_format.admin_order_field = 'created'


class HitAdmin(admin.ModelAdmin):
    list_display = (created_format,'user','ip','user_agent','hitcount')
    search_fields = ('ip','user_agent')
    date_hierarchy = 'created'
    actions = [ actions.blacklist_ips,
                actions.blacklist_user_agents,
                actions.blacklist_delete_ips,
                actions.blacklist_delete_user_agents,
                actions.delete_queryset,
                ]
    #list_display_links = (None,)

    def get_actions(self, request):
        # Override the default `get_actions` to ensure that our model's
        # `delete()` method is called.
        actions = super(HitAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class HitCountAdmin(admin.ModelAdmin):
    list_display = ('content_object','hits','modified')
    fields = ('hits',)


class BlacklistIPAdmin(admin.ModelAdmin):
    pass


class BlacklistUserAgentAdmin(admin.ModelAdmin):
    pass
 
admin.site.register(Hit, HitAdmin)
admin.site.register(HitCount, HitCountAdmin) 
admin.site.register(BlacklistIP, BlacklistIPAdmin)
admin.site.register(BlacklistUserAgent, BlacklistUserAgentAdmin)
