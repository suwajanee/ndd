from django.conf.urls import url

from .views import booking_add_view
from .views import booking_delete_view
from .views import booking_edit_view
from .views import booking_page_view
from .views import booking_time_view
from .views import booking_data_view
from .views import booking_time_export
from .views.booking_print_view import BookingPrintView


urlpatterns = [

    url(r'^$', booking_page_view.booking_page, name='booking-page'),
    url(r'^add/$', booking_add_view.booking_add_page, name='booking-add-page'),
    
    url(r'^api/filter-bookings/$', booking_page_view.api_filter_bookings, name='api-filter-bookings'),
    url(r'^api/save-add-bookings/$', booking_add_view.api_save_add_bookings, name='api-save-add-bookings'),
    url(r'^api/save-edit-bookings/$', booking_edit_view.api_save_edit_bookings, name='api-save-edit-bookings'),
    url(r'^api/delete-bookings/$', booking_delete_view.api_delete_bookings, name='api-delete-bookings'),

    url(r'^api/get-time-bookings/$', booking_time_view.api_get_time_bookings, name='api-get-time-bookings'),
    url(r'^api/save-time-bookings/$', booking_time_view.api_save_time_bookings, name='api-save-time-bookings'),

    url(r'^print/(?P<pk>\d+)/$', BookingPrintView.as_view(), name='booking-print'),
    url(r'^time/export/$', booking_time_export.export_time, name='booking-export-time'),

    # Summary
    url(r'^api/get-work-list/$', booking_data_view.api_get_work_list, name='api-get-booking-work-list'),

    
]
