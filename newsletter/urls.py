from django.urls import path

from newsletter.apps import NewsletterConfig
from . import views


app_name = NewsletterConfig.name

urlpatterns = [
    path('home/', views.HomeTemplateView.as_view(), name='home'),

    path('message/create/', views.MessageCreateView.as_view(), name='message-create'),
    path('message/update/<int:pk>/', views.MessageUpdateView.as_view(), name='message-update'),
    path('message/detail/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
    path('message/delete/<int:pk>/', views.MessageDeleteView.as_view(), name='message-delete'),
    path('message/list/', views.MessageListView.as_view(), name='message-list'),

    path('client/create/', views.ClientCreateView.as_view(), name='client-create'),
    path('client/update/<int:pk>/', views.ClientUpdateView.as_view(), name='client-update'),
    path('client/detail/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('client/delete/<int:pk>/', views.ClientDeleteView.as_view(), name='client-delete'),
    path('client/list/', views.ClientListView.as_view(), name='client-list'),

    path('newsletter/create/', views.NewsLetterCreateView.as_view(), name='newsletter-create'),
    path('newsletter/update/<int:pk>/', views.NewsletterUpdateView.as_view(), name='newsletter-update'),
    path('newsletter/detail/<int:pk>/', views.NewsletterDetailView.as_view(), name='newsletter-detail'),
    path('newsletter/delete/<int:pk>/', views.NewsletterDeleteView.as_view(), name='newsletter-delete'),
    path('newsletter/list/', views.NewsletterListView.as_view(), name='newsletter-list'),

    path('newsletter/history/', views.newsletter_history, name='newsletter-history'),
]
