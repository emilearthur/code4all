from django.http import response
from django.test import TestCase
from django.utils.http import urlencode
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from drones.models import DroneCategory, Pilot
from drones import views
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User



class DroneCategoryTests(APITestCase):
    def post_drone_category(self, name):
        url = reverse('drones:'+views.DroneCategoryList.name)
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def test_post_and_get_drone_category(self):
        """
        Ensure we can create a new DroneCategory and then retrieve it.
        """
        new_drone_category_name = "Hexacopter"
        response = self.post_drone_category(new_drone_category_name)
        print("PK {}".format(DroneCategory.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert DroneCategory.objects.count() == 1
        assert DroneCategory.objects.get().name == new_drone_category_name

    def test_post_existing_drone_category_name(self):
        """
        Ensure we cannot create a Drone Category with an existing name
        """
        url = reverse('drones:'+views.DroneCategoryList.name)
        new_drone_category_name = "Duplicated Copter"
        data = {"name": new_drone_category_name}
        response1 = self.post_drone_category(new_drone_category_name)
        assert response1.status_code == status.HTTP_201_CREATED
        response2 = self.post_drone_category(new_drone_category_name)
        print(response2)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST

    def test_filter_drone_category_by_name(self):
        """
        Ensure we can filter a drone category by name
        """
        drone_category_name1 = "Hexacopter"
        self.post_drone_category(drone_category_name1)
        drone_category_name2 = "Octocopter"
        self.post_drone_category(drone_category_name2)
        filter_by_name = {"name": drone_category_name1}
        url = '{0}?{1}'.format(reverse('drones:'+views.DroneCategoryList.name), urlencode(filter_by_name))
        print(url)
        response = self.client.get(url, format='json')
        print(response)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == drone_category_name1

    def test_get_drone_category_collection(self):
        """ 
        Ensure we can retrieve the drone categories collection 
        """
        new_drone_category = 'Super Copter'
        self.post_drone_category(new_drone_category)
        url = reverse('drones:'+views.DroneCategoryList.name)
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['name'] == new_drone_category

    def test_update_drone_category(self):
        """
        Ensure we can update a single field for a drone category
        """
        drone_category_name = 'Category Initial Name'
        response = self.post_drone_category(drone_category_name)
        url = reverse('drones:'+views.DroneCategoryDetails.name, None, {response.data['pk']})
        updated_drone_category_name = 'Updated Name'
        data = {'name': updated_drone_category_name}
        patch_response = self.client.patch(url, data, format='json')
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.data['name'] == updated_drone_category_name

    def test_get_drone_category(self):
        """
        Ensure we can get a single drone category by id
        """
        drone_category_name = 'Easy to retrieve'
        response = self.post_drone_category(drone_category_name)
        url = reverse('drones:'+views.DroneCategoryDetails.name, None, {response.data['pk']})
        get_response = self.client.get(url, format='json')
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.data['name'] == drone_category_name


class PilotTests(APITestCase):
    def post_pilot(self, name, gender, races_count):
        url = reverse('drones:'+views.PilotList.name)
        print(url)
        data = {'name': name, 'gender': gender, 'races_count':  races_count,}
        response = self.client.post(url, data, format='json')
        return response

    def create_user_and_set_token_credentials(self):
        user = User.objects.create_user('user01', 'user01@example.com', 'user01p4SSwOrD')
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(token.key))

    def test_post_and_get_pilot(self):
        """
        Ensure we can create a new Pilot and then retrieve it. 
        Ensure we cannot retrive the perisited pilot without a token.
        """
        self.create_user_and_set_token_credentials()
        new_pilot_name = "Json"
        new_pilot_gender = Pilot.MALE
        new_pilot_races_count = 5
        response = self.post_pilot(new_pilot_name, new_pilot_gender, new_pilot_races_count)
        print("nPk {0}n".format(Pilot.objects.get().pk))
        assert response.status_code == status.HTTP_201_CREATED
        assert Pilot.objects.count() == 1
        saved_pilot = Pilot.objects.get()
        assert saved_pilot.name == new_pilot_name
        assert saved_pilot.gender == new_pilot_gender
        assert saved_pilot.races_count == new_pilot_races_count
        url = reverse('drones:'+views.PilotDetails.name, None, {saved_pilot.pk})
        authorized_get_response = self.client.get(url, format='json')
        assert authorized_get_response.status_code == status.HTTP_200_OK
        assert authorized_get_response.data['name'] == new_pilot_name
        self.client.credentials()       # clean up credentials
        unauthorized_get_response = self.client.get(url, format='json')
        assert unauthorized_get_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_try_to_post_pilot_without_token(self):
        """
        Ensure we cannot create pilot without a token
        """
        new_pilot_name = "Unauthorized Pilot"
        new_pilot_gender = Pilot.FEMALE
        new_pilot_races_count = 5
        response = self.post_pilot(new_pilot_name, new_pilot_gender, new_pilot_races_count)
        print(response)
        print(Pilot.objects.count())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Pilot.objects.count() == 0