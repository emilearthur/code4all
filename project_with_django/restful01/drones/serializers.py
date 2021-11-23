from django.db.models import fields
from django.db.models.query import QuerySet
from rest_framework import serializers
from drones.models import DroneCategory, Drone, Pilot, Competition
from django.contrib.auth.models import User


class UserDroneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        models = Drone
        fields = ('url', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    drones = UserDroneSerializer(many=True, read_only=True)

    class Meta:
        models = User
        fields = ('url', 'pk', 'username', 'drone')


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    # Define one to many relationship that read-only.
    # drones is same as foriegn key used in Drone model.
    #The drone_category field will render the name field for the related DroneCategory.
    drones = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='drone-detail') # create a link of the drone via the view name 'drone-detial'.

    class Meta:
        model = DroneCategory
        fields = ('url', 'pk', 'name', 'drones')


class DroneSerializer(serializers.HyperlinkedModelSerializer):
    # SlugRelatedField is a readwrite filed that represents the target of relationship b/n unqiue slug variable
    drone_category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all(), slug_field='name')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Drone
        fields = ('url', 'name', 'drone_category', 'owner', 'manufacturing_date','has_it_competed','inserted_timestamp')


class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    # Display all detials for a related drone.
    drone = DroneSerializer()

    class Meta:
        model = Competition
        fields = ('url', 'pk','distance_in_feet', 'distance_achievement_date', 'drone')

class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
	# Display all the details for the related drone
	drone = DroneSerializer()

	class Meta:
		model = Competition
		fields = (
			'url',
			'pk',
			'distance_in_feet',
			'distance_achievement_date',
			'drone')


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    # We will use the PilotSerializer class to serialize Pilot instances and we will
    # use the perviously coded CompetitionSerializer class to serialize all the Competition instances
    # related to the Pilot.
    competitions = CompetitionSerializer(many=True, read_only=True) # one to many because pilot has many competitions.
    gender = serializers.ChoiceField(choices=Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Pilot
        fields = ('url', 'name', 'gender', 'gender_description', 'races_count','inserted_timestamp', 'competitions')


class PilotCompetitionSerializer(serializers.ModelSerializer):
    # display the pilots name 
    pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all(), slug_field='name')
    # display the drones name 
    drone = serializers.SlugRelatedField(queryset=Drone.objects.all(), slug_field='name')

    class Meta:
        model = Competition
        fields = ('url' ,'pk', 'distance_in_feet', 'distance_achievement_date', 'pilot', 'drone')