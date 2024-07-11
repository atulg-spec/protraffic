from django.contrib import admin
from .models import *

@admin.register(Campaigns)
class Campaigns(admin.ModelAdmin):
    list_display = ('user','campaign_name','domain_name','count','created_at')
    list_filter = ('user','domain_name','created_at','time_zone')
    search_fields = ('campaign_name','domain_name','keywords','urls')

@admin.register(Proxy)
class Proxy(admin.ModelAdmin):
    list_display = ('campaign','proxy')

@admin.register(Tasks)
class Tasks(admin.ModelAdmin):
    list_display = ('user','campaign','created_at','schedule_at','status')
    list_filter = ('user','campaign','created_at','schedule_at','status')


@admin.register(User_agents)
class User_agents(admin.ModelAdmin):
    list_display = ('chrome_version','user_agent')
    list_filter = ('chrome_version',)


@admin.register(Cookies)
class Cookies(admin.ModelAdmin):
    list_display = ('campaign','json_data')
    list_filter = ('campaign',)


admin.site.register(Chrome_versions)

admin.site.register(CookieFile)


# ----------Admin Customization------------
admin.site.site_header = "Traffic Buddy Admin"
admin.site.site_title = "Traffic Buddy Management"
admin.site.index_title = " | Admin"