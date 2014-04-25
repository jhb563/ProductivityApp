from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils import timezone
import datetime


class UserOptions(models.Model):
    user = models.ForeignKey(User)
    sundayTime = models.IntegerField(default = 300)
    mondayTime = models.IntegerField(default = 300)
    tuesdayTime = models.IntegerField(default = 300)
    wednesdayTime = models.IntegerField(default = 300)
    thursdayTime = models.IntegerField(default = 300)
    fridayTime = models.IntegerField(default = 300)
    saturdayTime = models.IntegerField(default = 300)
    
    def timeForDay(self,dayOfWeek):
        timeDictionary = {0 : self.sundayTime,
        1 : self.mondayTime,
        2 : self.tuesdayTime,
        3 : self.wednesdayTime,
        4 : self.thursdayTime,
        5 : self.fridayTime,
        6 : self.saturdayTime}
        return timeDictionary[dayOfWeek]


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
        return Task.objects.filter(parent_project=self,finished=0,assigned=1)

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
    timeAllocation = models.IntegerField(default = 60)
    priority = models.IntegerField(default = 1)
    assigned = models.IntegerField(default = 0)


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
