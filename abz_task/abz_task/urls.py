from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from abz_task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),

    path('', views.home, name='home'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
