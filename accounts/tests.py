from datetime import datetime

from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from locations.models import Municipality, Country
from models import Profile

class ProfileModelTest(TestCase):
    def test_creating_a_new_profile_and_saving_it_to_the_database(self):
        user = User.objects.create_user(username='foo',
                                        email='foo@fighters.com',
                                        password='foofighters')


        profile = user.get_profile()
        profile.gender = 'M'
        profile.birth_date = datetime.now()
        profile.home_phone = '1155555555'
        profile.work_phone = '1133333333'
        profile.cell_phone = '1199999999'
        profile.nationality = Country.objects.get(name__iexact='Brasil')
        profile.citizenship = Municipality.objects.get(name__iexact='Rio de Janeiro')
        profile.save()

        all_profiles_in_database = Profile.objects.all()
        self.assertEquals(len(all_profiles_in_database), 1)

        only_profile_in_database = all_profiles_in_database[0]
        self.assertEquals(only_profile_in_database, profile)

        self.assertEquals(only_profile_in_database.user, user)
        self.assertEquals(authenticate(username='foo', password='foofighters'), user)

        self.assertEquals(user.get_profile(), only_profile_in_database)
