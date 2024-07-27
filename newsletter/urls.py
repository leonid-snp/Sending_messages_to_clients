from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import (HomeTemplateView, MessageCreateView,
                              MessageDeleteView, MessageDetailView,
                              MessageListView, MessageUpdateView, ClientCreateView, ClientUpdateView, ClientDetailView,
                              ClientDeleteView, ClientListView)

app_name = NewsletterConfig.name

urlpatterns = [
    path('home/', HomeTemplateView.as_view(), name='home'),

    path('message/create/', MessageCreateView.as_view(), name='message-create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message-update'),
    path('message/detail/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message-delete'),
    path('message/list/', MessageListView.as_view(), name='message-list'),

    path('client/create/', ClientCreateView.as_view(), name='client-create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client-update'),
    path('client/detail/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client-delete'),
    path('client/list/', ClientListView.as_view(), name='client-list'),
]
