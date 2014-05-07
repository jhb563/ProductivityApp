from django.conf.urls import patterns, url

from todolist import views

urlpatterns = patterns('',
                       url(r'^projects(?P<user_id>\d+)/$', views.projects, name = 'projects'),
                       url(r'^profile(?P<user_id>\d+)/$', views.profile, name = 'profile'),
                       url(r'^addproject/$', views.addproject),
                       url(r'^addtask/$', views.addtask),
                       url(r'^finishTask/$', views.finishTask),
                       url(r'^removeTask/$', views.removeTask),
                       url(r'^promoteTask/$', views.promoteTask),
                       url(r'^delayTask/$', views.delayTask),
                       url(r'^finishProject/$', views.finishProject),
                       url(r'^removeProject/$', views.removeProject),
                       url(r'^demoteProject/$', views.demoteProject),
                       url(r'^changeColor/$', views.changeColor),
                       url(r'^invalid_project_add/$',views.invalid_project_add),
                       url(r'^invalid_task_access/$',views.invalid_task_access),
                       url(r'^updateUserTimes/$',views.updateUserTimes),
                       url(r'^assignTasks/$',views.assignDeadlinesToTasks),


                       )

