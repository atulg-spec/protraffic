from django.contrib import admin
from .models import *

@admin.register(Campaigns)
class Campaigns(admin.ModelAdmin):
    list_display = ('campaign_name','domain_name','created_at')
    list_filter = ('domain_name','created_at','time_zone')
    search_fields = ('campaign_name','domain_name','keywords','urls')
    fieldsets = (
        (None, {'fields': ('campaign_name', 'domain_name')}),
        ('Time Zones', {'fields': ('time_zone',)}),
        ('Browser Settings', {'fields': ('user_agents', 'extension_path')}),
        ('Campaign Info', {'fields': ('urls' ,'keywords', 'search_engines')}),
        ('Scroll Behaviour', {'fields': ('visit_count_from', 'visit_count_to', 'scroll_duration_from', 'scroll_duration_to','only_last_page_scroll_for_facebook')}),
        ('Extensions', {'fields': ('cookies_file','proxy_file')}),
    )

admin.site.register(SearchEngine)
@admin.register(Proxy)
class Proxy(admin.ModelAdmin):
    list_display = ('campaign','proxy')
    list_filter = ('campaign',)

@admin.register(Tasks)
class Tasks(admin.ModelAdmin):
    list_display = ('campaign','profile','profile_delay','repetition_count','repetition_done','created_at','schedule_at','status')
    list_filter = ('campaign','created_at','schedule_at','status')


@admin.register(User_agents)
class User_agents(admin.ModelAdmin):
    list_display = ('chrome_version','user_agent','width','height','isMobile')
    list_filter = ('chrome_version','isMobile')


@admin.register(Cookies)
class Cookies(admin.ModelAdmin):
    list_display = ('campaign','json_data')
    list_filter = ('campaign',)

@admin.register(CookieFile)
class CookieFile(admin.ModelAdmin):
    list_display = ('campaign','file')
    list_filter = ('campaign',)

@admin.register(Proxyfile)
class Proxyfile(admin.ModelAdmin):
    list_display = ('campaign','file')
    list_filter = ('campaign',)

@admin.register(UserAgentsFile)
class UserAgentsFile(admin.ModelAdmin):
    list_display = ('Chrome_version','file')
    list_filter = ('Chrome_version',)


# admin.site.register(SearchEngine)
admin.site.register(Chrome_versions)


# ----------Admin Customization------------
admin.site.site_header = "Traffic Buddy Admin"
admin.site.site_title = "Traffic Buddy Management"
admin.site.index_title = " | Admin"
