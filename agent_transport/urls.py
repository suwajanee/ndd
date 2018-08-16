from django.urls import path
from django.conf.urls import url
from .views.agent_transport_table_view import AgentTransportTableView
from .views.agent_transport_add_view import AgentTransportAddView
from .views.agent_transport_edit_table_view import AgentTransportEditTableView
from .views.agent_transport_print_view import AgentTransportPrintView


urlpatterns = [
    url(r'^$', AgentTransportTableView.get_table, name='agent-transport-table'),
    url(r'^print/(?P<pk>\d+)/(?P<template>\w+)/$', AgentTransportPrintView.as_view(), name='agent-transport-print'),

    url(r'^add/$', AgentTransportAddView.add_agent_transport, name='agent-transport-add'),
    url(r'^save/$', AgentTransportAddView.save_data, name='agent-transport-save'), 

    url(r'^delete/(?P<pk>\d+)/$', AgentTransportTableView.delete_data, name='agent-transport-delete'), #delete in table page
    url(r'^update/$', AgentTransportTableView.update_data, name='agent-transport-update'), #update in table page

    url(r'^edit/$', AgentTransportEditTableView.get_edit_table, name='agent-transport-edit'),
    url(r'^edit/save$', AgentTransportEditTableView.save_edit_table, name='agent-transport-edit-save'),
]


