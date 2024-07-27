from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newsletter.urls', namespace='newsletter')),
    path('users/', include('users.urls', namespace='users'))
]
