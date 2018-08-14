from django.urls import path
from django.conf.urls import url
from .views.agent_transport_table_view import AgentTransportTableView
from .views.agent_transport_add_view import AgentTransportAddView


urlpatterns = [
    url(r'^$', AgentTransportTableView.get_table, name='agent-transport-table'),
    # url(r'^print/(?P<pk>\d+)/(?P<template>\w+)/$', BookingPrintView.as_view(), name='booking-print'),

    url(r'^add/$', AgentTransportAddView.add_agent_transport, name='agent-transport-add'),
    url(r'^save/$', AgentTransportAddView.save_data, name='agent-transport-save'), 

    url(r'^delete/(?P<pk>\d+)/$', AgentTransportTableView.delete_data, name='agent-transport-delete'), #delete in table page
    url(r'^update/$', AgentTransportTableView.update_data, name='agent-transport-update'), #update in table page

    # url(r'^edit/$', BookingEditTableView.get_edit_table, name='booking-edit'),
    # url(r'^edit/save$', BookingEditTableView.save_edit_table, name='booking-edit-save'),
]


