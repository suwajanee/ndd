from django.conf.urls import url

from .views import customer_data_view
from .views import customer_page_view
from .views import customer_add_view
from .views import customer_edit_view
from .views import customer_cancel_view


urlpatterns = [

    url(r'^$', customer_page_view.customer_page, name='customer-page'),

    url(r'^api/shipper-address/$', customer_data_view.api_get_shipper_address, name='api-shipper-address'),

    url(r'^api/get-principals/$', customer_data_view.api_get_principals, name='api-get-principals'),
    url(r'^api/get-shippers/$', customer_data_view.api_get_shippers, name='api-get-shippers'),
    url(r'^api/get-customer-details/$', customer_data_view.api_get_customer_details, name='api-get-customer-details'),

    url(r'^api/save-add-customer/$', customer_add_view.api_save_add_customer, name='api-save-add-customer'),
    url(r'^api/save-edit-customer/$', customer_edit_view.api_save_edit_customer, name='api-save-edit-customer'),
    url(r'^api/cancel-customer/$', customer_cancel_view.api_cancel_customer, name='api-cancel-customer'),

    url(r'^api/save-add-shipper/$', customer_add_view.api_save_add_shipper, name='api-save-add-shipper'),
    url(r'^api/save-edit-shipper/$', customer_edit_view.api_save_edit_shipper, name='api-save-edit-shipper'),
    url(r'^api/cancel-shipper/$', customer_cancel_view.api_cancel_shipper, name='api-cancel-shipper'),

]
