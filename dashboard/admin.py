from django.contrib import admin
from .models import *
# Inline model for managing pages with sequence in Campaigns
class CampaignPageInline(admin.TabularInline):
    model = CampaignPage
    extra = 1  # Allows adding one extra page inline
    ordering = ('sequence',)  # Order by sequence

@admin.register(Campaigns)
class CampaignsAdmin(admin.ModelAdmin):
    list_display = ('campaign_name', 'domain_name', 'created_at', 'direct_traffic')
    list_filter = ('domain_name', 'created_at', 'time_zone')
    search_fields = ('campaign_name', 'domain_name', 'keywords', 'urls')
    
    fieldsets = (
        (None, {'fields': ('campaign_name', 'domain_name')}),
        ('Time Zones', {'fields': ('continent', 'time_zone')}),
        ('Browser Settings', {'fields': ('user_agents', 'facebook_post_div', 'extension_path')}),
        ('Campaign Info', {'fields': ('urls', 'keywords', 'search_engines')}),
        ('Scroll Behaviour', {'fields': ('visit_count_from', 'visit_count_to', 'direct_traffic','only_last_page_scroll_for_facebook')}),
        ('Extensions', {'fields': ('cookies_file', 'proxy_file')}),
    )
    
    inlines = [CampaignPageInline]  # Adding the inline model for pages

# Register PageBehaviour separately
admin.site.register(PageBehaviour)

# Optionally, register the through model CampaignPage if you need it in the admin panel
@admin.register(CampaignPage)
class CampaignPageAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'page', 'sequence')
    ordering = ('campaign', 'sequence')
admin.site.register(SearchEngine)

class ProxyAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'proxy', 'ip_address', 'city', 'region', 'country', 'timezone', 'latitude', 'longitude','status')
    search_fields = ('proxy', 'ip_address', 'city', 'region', 'country')
    list_filter = ('campaign', 'country', 'region', 'city','status')
    readonly_fields = ('ip_address', 'city', 'region', 'country', 'latitude', 'longitude', 'timezone','status')

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(Proxy, ProxyAdmin)


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
