from django.conf.urls import url
from drones import views
from drones.v2 import views as views_v2

urlpatterns = [
    url(r'^drone-categories/$', views.DroneCategoryList.as_view(),
        name=views.DroneCategoryList.name),
    url(r'^drone-categories/(?P<pk>[0-9]+)/$', views.DroneCategoryDetails.as_view(),
        name=views.DroneCategoryDetails.name),
    url(r'^drones/$', views.DroneList.as_view(),
        name=views.DroneList.name),
    url(r'^drones/(?P<pk>[0-9]+)/$', views.DroneDetails.as_view(),
        name=views.DroneDetails.name),
    url(r'^pilots/$', views.PilotList.as_view(),
        name=views.PilotList.name),
    url(r'^pilots/(?P<pk>[0-9]+)/$', views.PilotDetails.as_view(),
        name=views.PilotDetails.name),
    url(r'^competitions/$', views.CompetitionList.as_view(),
        name=views.CompetitionList.name),
    url(r'^competitions/(?P<pk>[0-9]+)/$', views.CompetitionDetails.as_view(),
        name=views.CompetitionDetails.name),
    url(r'^$', views_v2.ApiRootVersion2.as_view(), name=views_v2.ApiRootVersion2.name),
    url(r'^vehicle-categories/$', views.DroneCategoryList.as_view(),
        name=views.DroneCategoryList.name),
    url(r'^vehicle-categories/(?P<pk>[0-9]+)$', views.DroneCategoryDetails.as_view(),
        name=views.DroneCategoryDetails.name),
    url(r'^vehicles/$', views.DroneList.as_view(),
        name=views.DroneList.name),
    url(r'^vehicles/(?P<pk>[0-9]+)$', views.DroneDetails.as_view(),
        name=views.DroneDetails.name) ]