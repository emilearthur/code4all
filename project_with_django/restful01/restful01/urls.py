"""restful01 URL Configuration

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
from drones.views import CompetitionDetails, CompetitionList, PilotDetails, PilotList
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from toys .views import toy_list, toy_details
from rest_framework import routers 

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    #url(r'^', include('toys.urls')), # not working
    url(r'^toys/$', toy_list),
    #path('toys/', toy_list,),
    url(r'^toys/(?P<pk>[0-9]+)/$', toy_details),
    #path('toys/<int:pk>/',ToyViews.toy_details),
    url(r'^v1/', include(('drones.urls', 'v1'), namespace='v1')),
    url(r'^v1/api-auth/', include(('rest_framework.urls','rest_framework_v1'), namespace='rest_framework_v1')),
    url(r'^v2/', include(('drones.v2.urls', 'v2'), namespace='v2')),
    url(r'^v2/api-auth/', include(('rest_framework.urls','rest_framework_v2'), namespace='rest_framework_v2')),
    url(r'^', include(('drones.urls', 'drones'), namespace='drones')),
    url(r'^api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
]