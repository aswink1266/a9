"""student_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views import static
from accounts.views import Index
from django.conf import settings


urlpatterns = [
        path('admin/', admin.site.urls),

        path('accounts/', include('accounts.urls')),

        path('students/', include('students.urls')),

        path('media/<path:path>', static.serve, {'document_root': settings.MEDIA_ROOT}),

        path('', Index.as_view(template_name='accounts/index.html'), name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ]+urlpatterns
