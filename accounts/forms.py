from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from django.utils.timezone import now

from models import Profile

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label=_(u'First name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last name'), max_length=30)
    email = forms.EmailField(label=_(u'E-mail address'), max_length=75)
    password = forms.CharField(label=_(u'Pasword'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username__iexact=username)
        except:
            return username
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_(u'A user with that e-mail already exists.'))

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user

class ProfileForm(UserForm):
    sex = forms.CharField(label=_(u'Sex'), widget=forms.Select(choices=Profile.SEX_CHOICES))
    birth_date = forms.DateField(label=_(u'Birthday'), widget=SelectDateWidget(years=range(now().year-100, now().year)))

    def clean_sex(self):
        sex = self.cleaned_data['sex']
        if sex in set(x[0] for x in Profile.SEX_CHOICES):
            return sex
        raise forms.ValidationError(_(u'Please select a valid sex.'))

    def save(self):
        user = super(ProfileForm, self).save(self)

        profile = user.get_profile()
        profile.sex = self.cleaned_data['sex']
        profile.birth_date = self.cleaned_data['birth_date']
        profile.save()

        return user
