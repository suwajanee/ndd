from django.conf.urls import url

from .views import truck_data_view
from .views import truck_edit_view
from .views import truck_page_view


urlpatterns = [
    url(r'^$', truck_page_view.truck_page, name='truck-page'),
    url(r'^chassis/$', truck_page_view.chassis_page, name='chassis-page'),
    url(r'^sold/$', truck_page_view.sold_page, name='sold-page'),


    url(r'^api/get-truck-chassis-count/$', truck_data_view.api_get_truck_chassis_count, name='api-get-truck-chassis-count'),

    url(r'^api/get-manufacturer/$', truck_data_view.api_get_manufacturer, name='api-get-manufacturer'),
    
    url(r'^api/get-truck/$', truck_data_view.api_get_truck, name='api-get-truck'),
    url(r'^api/get-chassis/$', truck_data_view.api_get_chassis, name='api-get-chassis'),


    url(r'^api/edit-expired-date/$', truck_edit_view.api_edit_expired_date, name='api-edit-expired-date'),

    # Dashboard
    url(r'^api/get-daily-trucks/$', truck_data_view.api_get_daily_trucks, name='api-get-daily-trucks'),

    # Driver page
    url(r'^api/get-truck-choices/$', truck_data_view.api_get_truck_choices, name='api-get-truck-choices'),

]
