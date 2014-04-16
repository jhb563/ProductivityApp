from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Maybe relate to children projects?
# How to I get this type of relationship?
class Project(models.Model):
    user = models.ForeignKey(User)
    date_started = models.DateTimeField('Date Started')
    name = models.CharField(max_length=200)
    deadline = models.DateTimeField('Deadline')
    date_finished = models.DateTimeField('Date Finished')
    parentid = models.IntegerField(default=-1)
    finished = models.IntegerField(default=0)
    color = models.CharField(max_length=7,default="#0000FF")

    def __unicode__(self):
        return self.name

    def children(self):
        return Project.objects.filter(parentid=self.id,finished=0)

    def subtasks(self):
        return Task.objects.filter(parent_project=self,finished=0)

    def tasksForUser(self):
        User = self.user
        return Task.objects.filter(user=User,finished=0)

    def finishedRecently(self):
        if self.finished == 0:
            return false
        else :
            return self.date_finished <= timezone.now() - datetime.timedelta(days = 7)

    

    

class Task(models.Model):
    user = models.ForeignKey(User)
    date_started = models.DateTimeField('Date Started')
    name = models.CharField(max_length=200)
    deadline = models.DateTimeField('Deadline')
    date_finished = models.DateTimeField('Date Finished')
    parent_project = models.ForeignKey(Project)
    finished = models.IntegerField(default=0)
    requiredTasks = models.ManyToManyField('self',null=True,symmetrical=False)

    def __unicode__(self):
        return self.name

    def unfinished_siblings(self):
        User = self.user
        return Task.objects.filter(user=User,finished=0)

    def isUrgent(self):
        return self.deadline <= timezone.now() + datetime.timedelta(days = 1)


    def finishedRecently(self):
        if self.finished == 0:
            return false
        else :
            return self.date_finished <= timezone.now() - datetime.timedelta(days = 7)
