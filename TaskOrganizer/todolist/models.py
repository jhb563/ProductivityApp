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
        timeDictionary = {6 : self.sundayTime,
        0 : self.mondayTime,
        1 : self.tuesdayTime,
        2 : self.wednesdayTime,
        3 : self.thursdayTime,
        4 : self.fridayTime,
        5 : self.saturdayTime}
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

    def containsMalleableTasks(self):
        return Task.objects.filter(parent_project=self,finished=0,deadlineIsHard = 0).count() > 0

    def isUrgent(self):
        return self.deadline <= timezone.now() + datetime.timedelta(days = 1)

    def deadlineIsGettingClose(self):
        return self.deadline <= timezone.now() + datetime.timedelta(days = 4)

    def countSubprojectsAndTasks(self):
        
        taskCount = Task.objects.filter(parent_project = self, finished = 0).count()
        immediateSubprojects = Project.objects.filter(parentid = self.id, finished = 0)
        projectCount = immediateSubprojects.count()

        for proj in immediateSubprojects:
            projectAndTaskCount = proj.countSubprojectsAndTasks()
            taskCount += projectAndTaskCount[0]
            projectCount += projectAndTaskCount[1]
        result = []
        result.append(taskCount)
        result.append(projectCount)
        return result

class Task(models.Model):
    user = models.ForeignKey(User)
    date_started = models.DateTimeField('Date Started')
    name = models.CharField(max_length=200)
    deadline = models.DateTimeField('Deadline')
    date_finished = models.DateTimeField('Date Finished')
    parent_project = models.ForeignKey(Project,null=True)
    finished = models.IntegerField(default=0)
    requiredTasks = models.ManyToManyField('self',null=True,symmetrical=False)
    timeAllocation = models.IntegerField(default = 60)
    assigned = models.IntegerField(default = 0)
    deadlineIsHard = models.IntegerField(default = 0)


    def __unicode__(self):
        return self.name

    def unfinished_siblings(self):
        User = self.user
        return Task.objects.filter(user=User,finished=0)

    def isUrgent(self):
        return self.deadline <= timezone.now() + datetime.timedelta(days = 1)

    def deadlineIsGettingClose(self):
        return self.deadline <= timezone.now() + datetime.timedelta(days = 4)

    def finishedRecently(self):
        if self.finished == 0:
            return false
        else :
            return self.date_finished <= timezone.now() - datetime.timedelta(days = 7)

    def hasUnfinishedPrereqs(self):
        return self.requiredTasks.filter(finished = 0, deadlineIsHard = 0).count() > 0

    # Weight tasks on how much time they take, and how long until their
    # parent's deadline
    def taskWeight(self):
        timeToDeadline = self.parent_project.deadline - timezone.now()
        days, seconds = timeToDeadline.days, timeToDeadline.seconds
        totalSeconds = days * 3600 * 24 + seconds
        return (totalSeconds * self.timeAllocation)

    # Used in heapifying the data while assigning deadlines
    def __cmp__(self,other):
        return cmp(self.taskWeight(),other.taskWeight())

