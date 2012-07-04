from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^profile/$',
        profile,
        name='profile'),

    url(r'^signup/$',
        signup,
        name='signup'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name='login'),

    url(r'^logout/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout'),

    url(r'^activate/(?P<activation_key>\w+)/$',
        activate,
        name='activate'),

    url(r'^register/$',
        register,
        name='register'),
)
