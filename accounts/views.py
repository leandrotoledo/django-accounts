from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from forms import UserForm, ProfileForm
from models import Profile

@csrf_protect
def signup(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect(reverse('admin:index'))

        return HttpResponseRedirect(reverse('profile'))

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()

            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])

            login(request, user)

            return HttpResponseRedirect(reverse('profile'))
    else:
        form = ProfileForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('admin:index'))

    return render(request, 'profile.html')

@login_required
@user_passes_test(lambda u: not u.get_profile().activation_key_expired)
def register(request):
    user = request.user
    site = Site.objects.get_current()
    profile = user.get_profile()

    subject = _(u'Signup Confirmation - %s') % site.name
    context = {'activation_key': profile.activation_key,
               'user': user,
               'site': site}
    message = render_to_string('register_email.txt', context)

    user.email_user(subject, message)

    return HttpResponseRedirect(reverse('profile'))

def activate(request, activation_key):
    profile = Profile.objects.activate_profile(activation_key)

    return HttpResponseRedirect(reverse('profile'))
