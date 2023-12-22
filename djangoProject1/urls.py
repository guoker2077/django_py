"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app01 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('user/home/', views.user_home, name='user_home'),
    path('user/home/<int:user_id>', views.user_home_alreadyin, name='user_home_alreadyin'),
    path('user/add/', views.user_add, name='user_add'),
    path('user/news/<int:user_id>', views.latest_news_alreadyin, name='latest_news_alreadyin'),
    path('user/pricing/<int:user_id>', views.pricing_alreadyin, name='pricing_alreadyin'),
    path('user/docs/<int:user_id>', views.docs_alreadyin, name='docs_alreadyin'),
    path('user/news/', views.latest_news, name='latest_news'),
    path('user/pricing/', views.pricing,name='pricing'),
    path('user/docs/', views.docs, name='docs'),
    path('user/info/<int:user_id>/', views.user_info, name='user_info'),
    path('user/func/image/strengthen/<int:user_id>', views.user_func_image_strengthen,
         name='user_func_image_strengthen'),
    path('user/func/image/recognition/<int:user_id>', views.user_func_image_recognition,
         name='user_func_image_recognition'),

    path("admin/login/", views.admin_login),
    path("admin/home/", views.admin_home_page, name='admin_home_page'),
    path("admin/main/", views.admin_main, name='admin_main'),
    path("admin/chart/", views.admin_chart, name='admin_chart'),
    path("admin/user/delete/", views.admin_user_delete),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
