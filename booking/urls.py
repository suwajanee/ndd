from django.urls import path
from django.conf.urls import url
from .views.table_view import BookingTableView
from .views.print_view import BookingPrintView


urlpatterns = [
    url(r'^$', BookingTableView.get_table, name='booking-table'),
    url(r'^id/(?P<pk>\d+)/$', BookingPrintView.as_view(), name='booking-print'),

]


