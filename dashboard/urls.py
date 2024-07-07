from django.urls import path
from dashboard.views import *
# urls.py
urlpatterns = [
    # PAGES
    path("getcampaigns/<str:user>",getcampaigns,name='getcampaigns'),
    path("repetitiondone/<str:id>",repetitiondone,name='repetitiondone'),
]