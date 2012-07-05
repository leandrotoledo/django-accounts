import datetime

from django.test import TestCase
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from models import Profile

class ProfileModelTest(TestCase):
    def test_creating_a_new_profile_and_saving_it_to_the_database(self):
        user = User.objects.create_user(username='foo',
                                        email='foo@fighters.com',
                                        password='foofighters')


        profile = user.get_profile()
        profile.gender = 'M'
        profile.birth_date = datetime.now()
        profile.save()

        all_profiles_in_database = Profile.objects.all()
        self.assertEquals(len(all_profiles_in_database), 1)

        only_profile_in_database = all_profiles_in_database[0]
        self.assertEquals(only_profile_in_database, profile)

        self.assertEquals(only_profile_in_database.user, user)
        self.assertEquals(authenticate(username='foo', password='foofighters'), user)

        self.assertEquals(user.get_profile(), only_profile_in_database)
