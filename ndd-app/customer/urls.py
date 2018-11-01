from django.conf.urls import url

from .views.customer_add_view import CustomerAddView
from .views.customer_cancel_view import CustomerCancelView
from .views.customer_edit_view import CustomerEditView
from .views.customer_table_view import CustomerListView

from .views import customer_data_view


urlpatterns = [
    url(r'^$', CustomerListView.render_customer_list, name='customer-list'),
    url(r'^(?P<pk>\d+)/detail/$', CustomerListView.render_customer_detail, name='customer-detail'),

    url(r'^add-customer/$', CustomerAddView.add_customer, name='customer-add-new'),
    url(r'^add-shipper/$', CustomerAddView.add_shipper, name='shipper-add-new'),

    url(r'^edit-customer/$', CustomerEditView.edit_customer, name='customer-edit'),
    url(r'^edit-shipper/$', CustomerEditView.edit_shipper, name='shipper-edit'),

    url(r'^cancel-customer/$', CustomerCancelView.cancel_customer, name='customer-cancel'),
    url(r'^cancel-shipper/$', CustomerCancelView.cancel_shipper, name='shipper-cancel'),


    url(r'^api/shipper-address/$', customer_data_view.api_get_shipper_address, name='api-shipper-address'),
    url(r'^api/get-principals/$', customer_data_view.api_get_principals, name='api-get-principals'),
    url(r'^api/get-shippers/$', customer_data_view.api_get_shippers, name='api-get-shippers'),

]


