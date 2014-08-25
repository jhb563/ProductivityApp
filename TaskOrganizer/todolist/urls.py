from django.conf.urls import patterns, url

from todolist import views
from todolist import taskViews
from todolist import projectViews

urlpatterns = patterns('',
                       url(r'^projects(?P<user_id>\d+)/$', views.projects, name = 'projects'),
                       url(r'^projectsNew(?P<user_id>\d+)/$', views.projectsNew, name = 'projectsNew'),
                       url(r'^projectsTest(?P<user_id>\d+)/$', views.projectsTest, name = 'projects'),
                       url(r'^profile(?P<user_id>\d+)/$', views.profile, name = 'profile'),
                       url(r'^addproject/$', projectViews.addproject),
                       url(r'^projects/(?P<user_id>\d+)/(?P<project_id>\d+)/$', projectViews.projectCardView),
                       url(r'^addtask/$', taskViews.addtask),
                       url(r'^tasks/(?P<user_id>\d+)/(?P<task_id>\d+)/$', taskViews.taskCardView),
                       url(r'^finishTask/$', taskViews.finishTask),
                       url(r'^removeTask/$', taskViews.removeTask),
                       url(r'^promoteTask/$', taskViews.promoteTask),
                       url(r'^delayTask/$', taskViews.delayTask),
                       url(r'^finishProject/$', projectViews.finishProject),
                       url(r'^removeProject/$', projectViews.removeProject),
                       url(r'^demoteProject/$', projectViews.demoteProject),
                       url(r'^changeColor/$', projectViews.changeColor),
                       url(r'^invalid_project_add/$',projectViews.invalid_project_add),
                       url(r'^invalid_task_access/$',taskViews.invalid_task_access),
                       url(r'^updateUserTimes/$',views.updateUserTimes),
                       url(r'^assignTasks/$',views.assignDeadlinesToTasks),


                       )

