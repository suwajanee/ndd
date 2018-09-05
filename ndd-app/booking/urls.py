from django.conf.urls import url
from django.urls import path

from .views.booking_add_view import BookingAddView
from .views.booking_delete_view import BookingDeleteView
from .views.booking_edit_table_view import BookingEditTableView
from .views.booking_print_view import BookingPrintView
from .views.booking_table_view import BookingTableView
from .views.booking_time_table_view import BookingTimeTableView
from .views.booking_update_view import BookingUpdateView


urlpatterns = [
    url(r'^$', BookingTableView.render_table_booking_page, name='booking-table'),
    url(r'^update/$', BookingUpdateView.update_data_booking, name='booking-update'), #update in table page

    url(r'^add/$', BookingAddView.render_add_booking_page, name='booking-add'),
    url(r'^save/$', BookingAddView.save_data_booking, name='booking-save'), 

    url(r'^delete/(?P<pk>\d+)/$', BookingDeleteView.delete_data_booking, name='booking-delete'), #delete in table page
    url(r'^delete/$', BookingDeleteView.delete_multiple_data_booking, name='booking-delete-multiple'),

    url(r'^edit/$', BookingEditTableView.render_edit_booking, name='booking-edit'),
    url(r'^edit/save/$', BookingEditTableView.save_edit_data_booking, name='booking-edit-save'),



    url(r'^print/(?P<pk>\d+)/(?P<template>\w+)/$', BookingPrintView.as_view(), name='booking-print'),



    

    url(r'^time/$', BookingTimeTableView.get_time_table, name='booking-time'),
    url(r'^time/save/$', BookingTimeTableView.save_time_table, name='booking-time-save'),

    url(r'^time/print/$', BookingPrintView.print_time, name='booking-print-time'),
]


