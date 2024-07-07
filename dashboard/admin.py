from django.contrib import admin
from .models import *

admin.site.register(Campaigns)
admin.site.register(Proxy)
admin.site.register(Tasks)
admin.site.register(User_agents)
admin.site.register(Chrome_versions)

admin.site.register(CookieFile)


# ----------Admin Customization------------
admin.site.site_header = "Traffic Buddy Admin"
admin.site.site_title = "Traffic Buddy Management"
admin.site.index_title = " | Admin"