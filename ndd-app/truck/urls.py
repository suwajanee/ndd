from django.conf.urls import url

from .views import truck_page_view
from .views import truck_data_view


urlpatterns = [
    url(r'^$', truck_page_view.truck_page, name='truck-page'),




    url(r'^api/get-daily-trucks/$', truck_data_view.api_get_daily_trucks, name='api-get-daily-trucks'),

]
