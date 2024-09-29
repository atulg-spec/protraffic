from django.contrib import admin
from .models import EmailAccounts, EmailAccountDataUpload

# Customizing the EmailAccounts model display in the admin panel
class EmailAccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'tag', 'date_time')  # Display these fields in the admin list view
    search_fields = ('email', 'user__username', 'tag')  # Add search functionality for email, user, and tag
    list_filter = ('tag', 'date_time')  # Add filter options by tag and date_time
    ordering = ('-date_time',)  # Order by date_time, newest first

# Customizing the EmailAccountDataUpload model display in the admin panel
class EmailAccountDataUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'tag', 'date_time')  # Display these fields in the admin list view
    search_fields = ('user__username', 'tag')  # Add search functionality for user and tag
    list_filter = ('tag', 'date_time')  # Add filter options by tag and date_time
    ordering = ('-date_time',)  # Order by date_time, newest first

# Registering the models with their custom admin classes
admin.site.register(EmailAccounts, EmailAccountsAdmin)
admin.site.register(EmailAccountDataUpload, EmailAccountDataUploadAdmin)
