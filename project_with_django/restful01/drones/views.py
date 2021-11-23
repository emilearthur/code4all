from django.db.models import fields, query
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drones.models import DroneCategory, Drone, Pilot, Competition
from drones.serializers import DroneCategorySerializer, DroneSerializer, PilotSerializer, PilotCompetitionSerializer
from django_filters import FilterSet
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, FilterSet
from rest_framework import permissions
from drones import custompermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import ScopedRateThrottle
import django_filters.rest_framework


class DroneCategoryList(generics.ListCreateAPIView):
    # list Drones Cateogry or Post a Drone Category
    # http verbs that will be processed GET, POST, OPTIONS
    # endpoint /drone-categories/
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'
    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class DroneCategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    # veiw, update, or delete a Drones Category.
    # http verbs that will be processed GET, PUT, PATCH, DELETE and OPTIONS
    # endpoint /drone-categories/{id}/
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = "dronecategory-detail"


class DroneList(generics.ListCreateAPIView):
    # list or post drones.
    # http verbs that will be processed GET, POST, OPTIONS
    # endpoint /drone/
    throttle_scope = 'drones'  # reference to default_throttle_rates in settings.py
    throttle_classes = (ScopedRateThrottle,)  # accumulate the number of reqiest and limit the rate of request.
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'
    filter_fields = ('name', 'drone_category', 'manufacturing_date', 'has_it_competed',)
    search_fields = ('^name',)
    ordering_fields = ('name', 'manufacturing_date')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          custompermission.IsCurrentUserOwnerOrReadOnly,
        )

    # overwriting perform_create method to provide additional owner field to create method.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DroneDetails(generics.RetrieveUpdateDestroyAPIView):
    # veiw, update, or delete a Drone. 
    # http verbs that will be processed GET, PUT, PATCH, DELETE and OPTIONS
    # endpoint /drone/{id}/
    throttle_scope = 'drones'  # reference to default_throttle_rates in settings.py
    throttle_classes = (ScopedRateThrottle,)
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          custompermission.IsCurrentUserOwnerOrReadOnly,
        )


class PilotList(generics.ListCreateAPIView):
    # list or post pilots.
    # http verbs that will be processed GET, POST, OPTIONS
    # endpoint /pilot/
    throttle_scope = 'pilots'  # reference to default_throttle_rates in settings.py
    throttle_classes = (ScopedRateThrottle,)  # accumulate the number of reqiest and limit the rate of request.
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'
    filter_fields = ('name', 'gender', 'races_count',)
    search_fields = ('^name',)
    ordering_fields = ('name', 'races_count')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class PilotDetails(generics.RetrieveUpdateDestroyAPIView):
    # veiw, update, or delete a pilot. 
    # http verbs that will be processed GET, PUT, PATCH, DELETE and OPTIONS
    # endpoint /pilot/{id}/
    throttle_scope = 'pilots'  # reference to default_throttle_rates in settings.py
    throttle_classes = (ScopedRateThrottle,)  # accumulate the number of reqiest and limit the rate of request.
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class CompetitionFilter(FilterSet):
    from_achievement_date = DateTimeFilter(field_name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = DateTimeFilter(field_name='distance_achievement_date', lookup_expr='lte')
    min_distance_in_feet = NumberFilter(field_name='distance_in_feet', lookup_expr='gte')
    max_distance_in_feet = NumberFilter(field_name='distance_in_feet', lookup_expr='lte')
    drone_name = AllValuesFilter(field_name='drone__name')
    pilot_name = AllValuesFilter(field_name='pilot__name')


    class Meta:
        model = Competition
        fields = ('distance_in_feet', 'from_achievement_date', 'to_achievement_date',
                  'min_distance_in_feet', 'max_distance_in_feet', 'drone_name', 'pilot_name',)



class CompetitionList(generics.ListCreateAPIView):
    # list or post competitions.
    # http verbs that will be processed GET, POST, OPTIONS
    # endpoint /competition/
    queryset = Competition.objects.all().order_by('-distance_achievement_date')
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'
    filter_class = CompetitionFilter
    ordering_fields = ('distance_in_feet', 'distance_achievement_date',)


class CompetitionDetails(generics.RetrieveUpdateDestroyAPIView):
    # veiw, update, or delete a compeitition.
    # http verbs that will be processed GET, PUT, PATCH, DELETE and OPTIONS
    # endpoint /competition/{id}/
    queryset = Competition.objects.all().order_by('-distance_achievement_date')
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'


class ApiRoot(generics.GenericAPIView):
    # this declares a get method.
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'drones-categories': reverse(DroneCategoryList.name, request=request),
            'drones': reverse(DroneList.name, request=request),
            'pilots': reverse(PilotList.name, request=request),
            'competitions': reverse(CompetitionList.name, request=request),})
            
        