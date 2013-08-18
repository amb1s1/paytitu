from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from clients.views import loginUser, createProfile, showProfile, main, updateProfile, followUsers
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
    (r'^$', loginUser.as_view()),
    (r'^main/', login_required(main.as_view())),
    (r'^accounts/', include('registration.urls')),
    url(r'^createProfile/', login_required(createProfile.as_view())),
    url(r'^showProfile/', login_required(showProfile.as_view())),
    url(r'^updateProfile/', login_required(updateProfile.as_view())),
    url(r'^followUsers/', login_required(followUsers.as_view())),
    url(r'^loginUser/', loginUser.as_view()),
    
)
