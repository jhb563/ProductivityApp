from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin, auth
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TaskOrganizer.views.home', name='home'),
    # url(r'^TaskOrganizer/', include('TaskOrganizer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^todolist/', include('todolist.urls')),
    url(r'^accounts/login/$', 'TaskOrganizer.views.login'),
    url(r'^accounts/auth/$', 'TaskOrganizer.views.auth_view'),
    url(r'^accounts/logout/$', 'TaskOrganizer.views.logout'),
    url(r'^accounts/loggedIn/$', 'TaskOrganizer.views.loggedIn'),
    url(r'^accounts/invalid/$', 'TaskOrganizer.views.invalid_login'),
    url(r'^accounts/createUser/$', 'TaskOrganizer.views.create_user'),
    url(r'^accounts/createUserAuth/$', 'TaskOrganizer.views.create_user_auth'),
                       
                       
)
