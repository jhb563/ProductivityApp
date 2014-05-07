from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from models import Project
from django.core.context_processors import csrf
from django.utils import timezone
from datetime import datetime, timedelta
from random import randrange
from collections import deque

from todolist.models import Project, Task, UserOptions


# User Profile Page
def profile(request, user_id):
    UList = User.objects.filter(id = user_id)

    if len(UList) < 1:
        return HttpResponseRedirect('/accounts/invalid')

    U = UList[0]
    if request.user.is_authenticated() and request.user == U:
        # Show the user's profile, including stats and a link
        # to their projects page

        # Query database to build user statistics

        thisUserTasks = Task.objects.filter(user = U)
        finishedTasks = thisUserTasks.filter(finished = 1)
        unfinishedTasks = thisUserTasks.filter(finished = 0)
        finishedTCount = finishedTasks.count()
        unfinishedTCount = unfinishedTasks.count()

        tFinRecentCount = 0
        for t in finishedTasks:
            if t.finishedRecently():
                tFinRecentCount += 1

        
        thisUserProjects = Project.objects.filter(user = U)
        finishedProjects = thisUserProjects.filter(finished = 1)
        unfinishedProjects = thisUserProjects.filter(finished = 0)
        finishedPCount = finishedProjects.count()
        unfinishedPCount = unfinishedProjects.count()
        options = UserOptions.objects.filter(user = U)[0]


        pFinRecentCount = 0
        for p in finishedProjects:
            if p.finishedRecently():
                pFinRecentCount += 1

        template = loader.get_template('todolist/profile.html')
        context = RequestContext(request, {
            'user' : U,
            'finishedTCount' : finishedTCount,
            'finishedPCount' : finishedPCount,
            'unfinishedTCount' : unfinishedTCount,
            'unfinishedPCount' : unfinishedPCount,
            'tFinRecentCount' : tFinRecentCount,
            'pFinRecentCount' : pFinRecentCount,
            'options' : options,

            })

        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('accounts/invalid')
        

def updateUserTimes(request):
    U = request.user
    if request.user.is_authenticated() and request.POST:
        # find the user and update their UserOptions object
        # with the new times submitted from the form
        # TODO This will error if the user doesn't have an options object
        opts = UserOptions.objects.filter(user = U)[0]
        opts.sundayTime = int(request.POST.get('sunday','300'))
        opts.mondayTime = int(request.POST.get('monday','300'))
        opts.tuesdayTime = int(request.POST.get('tuesday','300'))
        opts.wednesdayTime = int(request.POST.get('wednesday','300'))
        opts.thursdayTime = int(request.POST.get('thursday','300'))
        opts.fridayTime = int(request.POST.get('friday','300'))
        opts.saturdayTime = int(request.POST.get('saturday','300'))
        opts.save()
        return HttpResponseRedirect('/todolist/profile'+str(U.id))
    else:
        return HttpResponseRedirect('/accounts/invalid')


def assignDeadlinesToTasks(request):
    U = request.user
    if request.user.is_authenticated() and request.POST:
        # Do the algorithm
        # Get the "first deadline" (tonight just before midnight)
        today = datetime.now()
        deadline = datetime(today.year,today.month,today.day,23,59,59,0)

        # Create a task queue, consisting of a list of lists
        # Each inner list is the list of unassigned tasks in a given project
        # The lists themselves are ordered by the deadlines of their projects
        # initially. This needs to be a deque
        projectQ = deque()

        unfinishedProjects = Project.objects.filter(user = U, finished = 0).order_by("deadline")
        for p in unfinishedProjects:
            unassignedTasksForP = Task.objects.filter(parent_project = p,finished = 0,assigned = 0).order_by("priority")
            if unassignedTasksForP.count() > 0:
                tasksQueue = deque()
                for unassignedT in unassignedTasksForP:
                    tasksQueue.append(unassignedT)
                projectQ.append(tasksQueue)

        print(projectQ)
        


        # Loop until we have assigned deadlines to all of the tasks
        while(len(projectQ) > 0):
            # get today's day of week
            dayOfWeek = deadline.weekday();

            # Get tasks due today, that is the tasks that are due before
            # the current deadline variable, but after 24 hours before it
            oneDayEarlier = deadline - timedelta(days = 1)
            tasksToday = Task.objects.filter(user = U, finished = 0).exclude(assigned = 0).exclude(deadline__gte=deadline).filter(deadline__gte=oneDayEarlier)

            # Get the amount of time the user has allocated for this day,
            # keep track of the difference
            opts = UserOptions.objects.filter(user = U)[0]
            timeRemaing = opts.timeForDay(dayOfWeek)

            # Subtract from the time remaining the amount of time already
            # used by tasks
            for t in tasksToday:
                timeRemaing -= t.timeAllocation


            # While time is greater than 0
            while(timeRemaing > 0 and len(projectQ) > 0):
                # Get the first task in the first list of projects, remove
                # it from the list
                firstProjectList = projectQ.popleft()
                newTask = firstProjectList.popleft()

                # Set its deadline for the current deadline, subtract from
                # time remaining this task's allocated time
                newTask.deadline = deadline
                newTask.assigned = 1
                newTask.save()
                timeRemaing -= newTask.timeAllocation
                print(timeRemaing)

                # Pop the first list from our project queue and, if it
                # is not empty, append it to the back
                if len(firstProjectList) > 0:
                    projectQ.append(firstProjectList)

            # advance the deadline by 24 hours
            deadline += timedelta(days = 1)


        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('/accounts/invalid')


def projects(request, user_id):
    
    #render current projects
    UList = User.objects.filter(id = user_id)

    
    
    if len(UList) < 1:
        return HttpResponseRedirect('/accounts/invalid')
    
    U = UList[0]
    if request.user.is_authenticated() and request.user == U:

        # List projects that are due in the next 24 hours
        


        # Start with projects that have no parents
        root_projects = Project.objects.filter(user = U, parentid = -1, finished=0)
        # Also get tasks that have no prereqs
        # Get tasks that need to be done in the next day as well
        allTasks = Task.objects.filter(user = U, finished = 0).order_by("deadline")

        unassigned_tasks = allTasks.filter(assigned = 0)
        assigned_tasks = allTasks.filter(assigned = 1)

        next_tasks = []
        urgent_tasks = []
        for t in assigned_tasks:
            
            if t.requiredTasks.filter(finished = 0).count() <= 0:
                next_tasks.append(t)
            if t.isUrgent():
                urgent_tasks.append(t)

        template = loader.get_template('todolist/projects.html')
        context = RequestContext(request, {
        'user' : U,
        'project_list' : root_projects,
        'task_list' : next_tasks,
        'urgent_list' : urgent_tasks,
        'unassigned_list' : unassigned_tasks,
        })
        return HttpResponse(template.render(context))
    else :
        return HttpResponseRedirect('/accounts/invalid')

def genRandomColor():
    # Map from numbers to hex characters
    charMap = {0 : '0', 1 : '1', 2 : '2', 3 : '3', 4 : '4', 5 : '5', 6 : '6', 7 : '7', 8 : '8',
    9 : '9', 10 : 'A', 11 : 'B', 12 : 'C', 13 : 'D', 14 : 'E', 15 : 'F'}
    result = ['#']
    for i in range(6):
        j = randrange(16)
        result.append(charMap[j])
    result = ''.join(result)
    return result


def createTaskForUserFromList(taskname,user,parentProject,taskDeadline,taskPriority,timeRequired):
    # Create a placeholder value for times
    # If the user has submitted a valid deadline for this task, then
    # it is an assigned task. Otherwise, it is unassigned, so the
    # deadline will not matter, as it will be changed upon assignment
    t = timezone.now()
    if taskDeadline == "":
        deadline = t
        assignedValue = 0
    else:
        deadline = taskDeadline
        assignedValue = 1
    T = Task(user=user,name=taskname,date_started = t,deadline=deadline,date_finished=t,parent_project=parentProject,assigned = assignedValue,priority = taskPriority,timeAllocation=timeRequired)
    T.save()
    return



def addproject(request):
    # If a user is authenticated and this is a post request, then
    # we proceed. Otherwise return an invalid page
    U = request.user
    if request.user.is_authenticated() and request.POST:
        deadline = request.POST.get('deadline')
        pid = int(request.POST.get('parentid'))
        projectname = request.POST.get('projectname')
        projectColor = genRandomColor();


        P = Project(user=U,name=projectname,date_started=timezone.now(),deadline=deadline,date_finished=timezone.now(),parentid=pid,color=projectColor)
        P.save()

        # Loop through all the tasks posted with this project and create them as
        # unassigned tasks

        print(request.POST)

        index = 1;
        while not (request.POST.get(str(index)) is None):
            newTaskName = request.POST.get(str(index))
            taskDeadline = request.POST.get("time"+str(index))
            taskPriority = request.POST.get("priority"+str(index))
            timeRequired = request.POST.get("timeReq"+str(index))
            index = index + 1
            if newTaskName == "":
                continue
            else:
                createTaskForUserFromList(newTaskName,U,P,taskDeadline,taskPriority,timeRequired)

            
            

        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('/todolist/invalid_project_add')

def invalid_project_add(request):
    U = request.user
    if request.user.is_authenticated():
        userid = U.id
        template = loader.get_template('todolist/invalid_project_add.html')
        context = RequestContext(request, {
            'userid' : userid,
            })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/accounts/invalid')

def finishProject(request):
    U = request.user
    if request.user.is_authenticated() and request.POST:
        projectid = request.POST.get('projectid','')
        projectid = int(projectid)
        Ps = Project.objects.filter(id=projectid)
        P = Ps[0]
        subTasks = Task.objects.filter(parent_project=P,finished=0)

        if len(subTasks) > 0:
            print "Can't finish this project!"
        else:
            P.finished = 1
            P.date_finished = timezone.now()
            P.save()
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_project_add')


def removeProject(request):
    U = request.user
    if request.user.is_authenticated() and request.POST:
        projectid = request.POST.get('projectid','')
        projectid = int(projectid)
        Ps = Project.objects.filter(id=projectid)
        # TODO Handle empty case?
        P = Ps[0]
        subTasks = Task.objects.filter(parent_project=P,finished=0)
        if len(subTasks) > 0:
            print "Can't finish this project!"
        else :
            P.delete()
        
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_project_add')


def demoteProject(request):
    U = request.user
    if request.user.is_authenticated() and request.POST:
        projectid = request.POST.get('projectid','')
        projectid = int(projectid)
        print projectid
        Ps = Project.objects.filter(id = projectid)
        # TODO Handle empty case?
        P = Ps[0]
        subTasks = Task.objects.filter(parent_project=P,finished=0)
        if len(subTasks) > 0:
            print "Can't demote this project!"
        else :
            # Get parent project
            parentID = P.parentid
            # TODO Should be able to have tasks not attached to projects
            if parentID == -1:
                return HttpResponseRedirect('/todolist/projects'+str(U.id))

            parentProject = (Project.objects.filter(user = U,id = parentID))[0]
            # Get name
            pName = P.name
            # Get deadline
            pDeadline = P.deadline
            # Get date_started
            dateStarted = P.date_started
            # Get date_finished
            dateFinished = P.date_finished
            P.delete()
            T = Task(user = U,name = pName, date_started = dateStarted, deadline = pDeadline,parent_project = parentProject,date_finished=dateFinished)
            T.save()
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('/todolist/invalid_project_add')


def changeColor(request):
    U = request.user
    if request.user.is_authenticated() and request.POST:
        projectid = request.POST.get('projectid','')
        projectid = int(projectid)
        Ps = Project.objects.filter(id = projectid)
        # TODO Handle empty case?
        P = Ps[0]
        color = request.POST.get('color')
        P.color = "#" + color
        P.save()
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('/todolist/invalid_task_access')


def addtask(request):
    # If a user is authenticated and this is a post request, then we
    # proceed to add this task for this user. Otherwise we send them
    # to the invalid page.
    U = request.user
    if request.user.is_authenticated() and request.POST:
        taskname = request.POST.get('taskname')
        parent_id = request.POST.get('projectid')
        
        
        parent_project = (Project.objects.filter(user=U,id=int(parent_id)))[0]
        t = timezone.now()
        deadline = request.POST.get('deadline')
        T = Task(user=U,name=taskname,date_started = t,deadline=deadline,date_finished=t,parent_project=parent_project)
        T.save()
        

        for task_id in request.POST.getlist('checks'):
            tid = repr(task_id)
            tid = tid[2:-1]
            tid = int(tid)
            
            requiredT = Task.objects.filter(id = tid)[0]
            T.requiredTasks.add(requiredT)
        
        T.save()


        
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_task_access')
    
    
def finishTask(request):
    # If a user is authenticated and this is a post request, then we
    # proceed to finish this task for this user. Otherwise we send them
    # to the invalid page.
    U = request.user
    if request.user.is_authenticated() and request.POST:
        taskid = request.POST.get('taskid','')
        taskid = int(taskid)
        Ts = Task.objects.filter(user=U,id=taskid)
        T = Ts[0] # Will cause problems if none are available
        RequiredTasks = T.requiredTasks.filter(finished=0)
        if len(RequiredTasks) <= 0:
            T.finished = 1
            T.save()
        else :
            print "Cannot finish this task"

        
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_task_access')

def removeTask(request):
    # If a user is authenticated and this is a post request, then we
    # proceed to remove this task for this user. Otherwise we send them
    # to the invalid page.
    U = request.user
    if request.user.is_authenticated() and request.POST:
        taskid = request.POST.get('taskid','')
        taskid = int(taskid)
        Ts = Task.objects.filter(user=U,id=taskid)
        T = Ts[0] # TODO Will cause problems if none are available
        T.delete()
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_task_access')


def promoteTask(request):
    U = request.user
    if request.user.is_authenticated() and request.POST:
        # Get task, turn into projects
        taskID = request.POST.get('taskid','')
        taskID = int(taskID)
        Ts = Task.objects.filter(user = U, id = taskID)
        # TODO Handle Empty Case
        T = Ts[0]
        # Get name
        tName = T.name
        # Get deadline
        tDeadline = T.deadline
        # Get started, finished
        tStart = T.date_started
        tFinish = T.date_finished
        # Get parentID
        parentID = T.parent_project.id
        T.delete()
        projectColor = genRandomColor();
        P = Project(user = U, name = tName, deadline = tDeadline, date_started = tStart, date_finished = tFinish, parentid = parentID, color = projectColor)
        P.save()
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('todolist/invalid_task_access')

def delayTask(request):
    U = request.user
    if request.user.is_authenticated() and request.POST:
        # Get task, turn into projects
        taskID = request.POST.get('taskid','')
        taskID = int(taskID)
        Ts = Task.objects.filter(user = U, id = taskID)
        T = Ts[0]
        tDeadline = T.deadline
        newDeadline = tDeadline + timedelta(days = 1)
        T.deadline = newDeadline
        T.save()
        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('todolist/invalid_task_access')


def invalid_task_access(request):
    U = request.user
    if request.user.is_authenticated():
        userid = U.id
        template = loader.get_template('todolist/invalid_task_access.html')
        context = RequestContext(request, {
            'userid' : userid,
            })
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('/accounts/invalid')