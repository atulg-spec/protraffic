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
        ('Browser Settings', {'fields': ('user_agents', 'facebook_post_div', 'facebook_ads_div', 'is_iframe')}),
        ('Campaign Info', {'fields': ('urls', 'keywords','direct_urls' ,'search_engines')}),
        ('Scroll Behaviour', {'fields': ('visit_count_from', 'visit_count_to', 'direct_traffic', 'click_anywhere','selection_on_page')}),
        ('Extensions', {'fields': ('session_string_length','main_proxy','cookies_folder', 'proxy_file')}),
    )
    
    inlines = [CampaignPageInline]  # Adding the inline model for pages

# Register PageBehaviour separately
admin.site.register(PageBehaviour)
# admin.site.register(CampaignPage)

# Optionally, register the through model CampaignPage if you need it in the admin panel
@admin.register(CampaignPage)
class CampaignPageAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'page', 'sequence')
    ordering = ('campaign', 'sequence')
admin.site.register(SearchEngine)

class ProxyAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'proxy', 'ip_address', 'city', 'region', 'country', 'timezone','status','count')
    search_fields = ('proxy', 'count', 'ip_address', 'city', 'region', 'country')
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

    fieldsets = (
        (None, {'fields': ('user','status')}),
        ('Campaign Settings', {'fields': ('campaign','profile','profile_delay','repetition_count','repetition_done')}),
        ('Additional Settings', {'fields': ('facebook_campaign','schedule_at')}),
    )


class UserAgentsAdmin(admin.ModelAdmin):
    list_display = (
        'unmasked_vendor', 'unmasked_renderer', 'user_agent', 'width', 'height', 'visitor_id', 'canvas', 'WebGL'
    )
    search_fields = ('user_agent', 'visitor_id', 'chrome_version__version')
    list_filter = ('isMobile', 'chrome_version')

admin.site.register(User_agents, UserAgentsAdmin)

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
