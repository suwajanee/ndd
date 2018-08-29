from django.urls import path
from django.conf.urls import url
from .views.customer_table_view import CustomerTableView
from .views.customer_add_view import CustomerAddView


urlpatterns = [
    url(r'^$', CustomerTableView.get_customer_table, name='customer-list'),
    url(r'^(?P<pk>\d+)/detail/$', CustomerTableView.customer_detail, name='customer-detail'),

    url(r'^add-customer/$', CustomerAddView.add_customer, name='customer-add-new'),
    url(r'^add-shipper/$', CustomerAddView.add_shipper, name='shipper-add-new'),
]


