from django.conf.urls import url

from .views import truck_add_view
from .views import truck_data_view
from .views import truck_delete_view
from .views import truck_edit_view
from .views import truck_page_view


urlpatterns = [
    url(r'^$', truck_page_view.truck_page, name='truck-page'),
    url(r'^chassis/$', truck_page_view.chassis_page, name='chassis-page'),
    url(r'^manufacturer/$', truck_page_view.manufacturer_page, name='manufacturer-page'),
    url(r'^sold/$', truck_page_view.sold_page, name='sold-page'),

    url(r'^api/get-truck-chassis-count/$', truck_data_view.api_get_truck_chassis_count, name='api-get-truck-chassis-count'),

    url(r'^api/get-manufacturer/$', truck_data_view.api_get_manufacturer, name='api-get-manufacturer'),

    url(r'^api/get-truck/$', truck_data_view.api_get_truck, name='api-get-truck'),
    url(r'^api/get-chassis/$', truck_data_view.api_get_chassis, name='api-get-chassis'),
    url(r'^api/get-sold/$', truck_data_view.api_get_sold, name='api-get-sold'),

    url(r'^api/add-truck/$', truck_add_view.api_add_truck, name='api-add-truck'),
    url(r'^api/add-chassis/$', truck_add_view.api_add_chassis, name='api-add-chassis'),
    url(r'^api/add-manufacturer/$', truck_add_view.api_add_manufacturer, name='api-add-manufacturer'),

    url(r'^api/edit-truck/$', truck_edit_view.api_edit_truck, name='api-edit-truck'),
    url(r'^api/edit-chassis/$', truck_edit_view.api_edit_chassis, name='api-edit-chassis'),
    url(r'^api/edit-manufacturer/$', truck_edit_view.api_edit_manufacturer, name='api-edit-manufacturer'),
    url(r'^api/edit-expired-date/$', truck_edit_view.api_edit_expired_date, name='api-edit-expired-date'),

    url(r'^api/delete-manufacturer/$', truck_delete_view.api_delete_manufacturer, name='api-delete-manufacturer'),

    # Dashboard
    url(r'^api/get-daily-trucks/$', truck_data_view.api_get_daily_trucks, name='api-get-daily-trucks'),

    # Driver page
    # url(r'^api/get-truck-choices/$', truck_data_view.api_get_truck_choices, name='api-get-truck-choices'),

]
