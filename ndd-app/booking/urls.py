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
    
    url(r'^api/get-bookings/$', booking_page_view.api_get_bookings, name='api-get-bookings'),
    url(r'^api/filter-bookings/$', booking_page_view.api_filter_bookings, name='api-filter-bookings'),

    url(r'^api/check-work-id/$', booking_data_view.api_check_work_id, name='api-check-work-id'),

    url(r'^api/save-add-bookings/$', booking_add_view.api_save_add_bookings, name='api-save-add-bookings'),
    url(r'^api/save-edit-bookings/$', booking_edit_view.api_save_edit_bookings, name='api-save-edit-bookings'),
    url(r'^api/delete-bookings/$', booking_delete_view.api_delete_bookings, name='api-delete-bookings'),

    url(r'^api/change-state-booking/$', booking_edit_view.api_change_state_booking, name='api-change-state-booking'),
    url(r'^api/change-color/$', booking_edit_view.api_change_color_field, name='api-change-color-booking'),

    url(r'^api/get-time-bookings/$', booking_time_view.api_get_time_bookings, name='api-get-time-bookings'),
    url(r'^api/save-time-bookings/$', booking_time_view.api_save_time_bookings, name='api-save-time-bookings'),

    url(r'^print/(?P<pk>\d+)/$', BookingPrintView.as_view(), name='booking-print'),
    url(r'^time/export/$', booking_time_export.export_time, name='booking-export-time'),

    # Summary
    url(r'^api/get-work-list/$', booking_data_view.api_get_work_list, name='api-get-booking-work-list'),

    # Dashboard
    url(r'^api/get-booking-daily-works/$', booking_data_view.api_get_booking_daily_works, name='api-get-booking-daily-works'),

    # Container Size
    url(r'^api/get-container-size/$', booking_data_view.api_get_container_size, name='api-get-container-size'),

    # Transport Report
    url(r'^api/get-normal-work-by-work-id/$', booking_data_view.api_get_normal_work_by_work_id, name='api-get-normal-work-by-work-id')

]
