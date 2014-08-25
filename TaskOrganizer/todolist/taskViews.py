from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from models import Task,Project
from django.utils import timezone
from datetime import datetime, timedelta
from random import randrange

# Generate a random color to attach to a project
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

def taskCardView(request, user_id, task_id):
    usersForID = User.objects.filter(id = user_id)
    

    if len(usersForID) == 1 and request.user.is_authenticated() and request.user == usersForID[0]:
        tasksWithID = Task.objects.filter(user = usersForID[0], id = task_id)
        if len(tasksWithID) != 1:
            # TODO Maybe a better error page?
            return HttpResponseRedirect('/accounts/invalid')

        thisTask = tasksWithID[0]

        if thisTask.finished == 1:
            background_color = '#599c59'
        elif thisTask.isUrgent():
            background_color = '#FF3333'
        elif thisTask.deadlineIsGettingClose():
            background_color = '#FFFF33'
        else :
            background_color = '#599c59'

        template = loader.get_template('todolist/taskCard.html')
        contextDict = { 'task' : thisTask, 'background_color' : background_color}

        if thisTask.deadline is not None:
            d = thisTask.deadline
            contextDict['deadline_date'] = str(d.month) + '/' + str(d.day) + '/' + str(d.year)
        context = RequestContext(request, contextDict)
        return HttpResponse(template.render(context))
    else :
        # TODO Better error page
        return HttpResponseRedirect('accounts/invalid')


def createTaskForUserFromList(taskname,user,parentProject,taskDeadline,timeRequired):
    # Create a placeholder value for times
    # If the user has submitted a valid deadline for this task, then
    # it is an assigned task. Otherwise, it is unassigned, so the
    # deadline will not matter, as it will be changed upon assignment
    t = timezone.now()
    if taskDeadline == "":
        deadline = t
        assignedValue = 0
        hardDeadline = 0
    else:
        deadline = taskDeadline
        assignedValue = 1
        hardDeadline = 0
    T = Task(user=user,name=taskname,date_started = t,deadline=deadline,date_finished=t,parent_project=parentProject,assigned = assignedValue, deadlineIsHard = hardDeadline,timeAllocation=timeRequired)
    T.save()
    return



def addtask(request):
    # If a user is authenticated and this is a post request, then we
    # proceed to add this task for this user. Otherwise we send them
    # to the invalid page.
    U = request.user
    if request.user.is_authenticated() and request.POST:
        index = 1;
        if ('projectid' in request.POST):
            projectid = request.POST.get('projectid')
            P = Project.objects.filter(id = projectid)[0]
        else :
            P = None

        # Loop through every added task, save its information, and add it
        while (str(index) in request.POST):
            newTaskName = request.POST.get(str(index))
            taskDeadline = request.POST.get("time"+str(index))
            timeRequired = request.POST.get("timeReq"+str(index))
            index = index + 1
            if newTaskName == "":
                continue
            else:
                createTaskForUserFromList(newTaskName,U,P,taskDeadline,timeRequired)

            

        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_task_access/')
    
    
def finishTask(request):
    # If a user is authenticated and this is a post request, then we
    # proceed to finish this task for this user. Otherwise we send them
    # to the invalid page.
    U = request.user
    if request.user.is_authenticated() and request.POST:
        taskid = request.POST.get('taskid','')
        taskid = int(taskid)
        Ts = Task.objects.filter(user=U,id=taskid)
        if len(Ts) <= 0:
            # TODO Should bring up a warning box, will be fixed
            # in new layout
            return HttpResponseRedirect('/todolist/invalid_task_access/')

        T = Ts[0]
        RequiredTasks = T.requiredTasks.filter(finished=0)
        if RequiredTasks.count() <= 0:
            T.finished = 1
            T.save()
        else :
            # TODO Should be a warning to user, will be fixed in updated layout
            print "Cannot finish this task"

        
        if request.is_ajax():
            return HttpResponse('Success')
        else :
            return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_task_access/')

def removeTask(request):
    # If a user is authenticated and this is a post request, then we
    # proceed to remove this task for this user. Otherwise we send them
    # to the invalid page.
    U = request.user
    if request.user.is_authenticated() and request.POST:
        taskid = request.POST.get('taskid','')
        taskid = int(taskid)
        Ts = Task.objects.filter(user=U,id=taskid)
        if len(Ts) <= 0:
            # TODO Should bring up a warning box, will be fixed
            # in new layout
            return HttpResponseRedirect('/todolist/invalid_task_access/')
        T = Ts[0]
        T.delete()
        if request.is_ajax():
            return HttpResponse('Success')
        else :
            return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_task_access/')


def promoteTask(request):
    # Deletes this task, and instead makes it into a project with the same deadline
    U = request.user
    if request.user.is_authenticated() and request.POST:
        # Get task, turn into projects
        taskID = request.POST.get('taskid','')
        taskID = int(taskID)
        Ts = Task.objects.filter(user = U, id = taskID)
        if len(Ts) <= 0:
            # TODO Should bring up a warning box, will be fixed
            # in new layout
            return HttpResponseRedirect('/todolist/invalid_task_access/')
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
        # TODO Should include new project stuff as well, at least ID
        if request.is_ajax():
            return HttpResponse('Success')
        else :
            return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('todolist/invalid_task_access/')

def delayTask(request):
    # Pushes the deadline for a task back by 24 hours
    U = request.user
    if request.user.is_authenticated() and request.POST:
        # Get task, turn into projects
        taskID = request.POST.get('taskid','')
        taskID = int(taskID)
        Ts = Task.objects.filter(user = U, id = taskID)
        if len(Ts) <= 0:
            # TODO Should bring up a warning box, will be fixed
            # in new layout
            return HttpResponseRedirect('/todolist/invalid_task_access/')
        T = Ts[0]
        tDeadline = T.deadline
        newDeadline = tDeadline + timedelta(days = 1)
        T.deadline = newDeadline
        T.save()
        if request.is_ajax():
            return HttpResponse('Success')
        else :
            return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('todolist/invalid_task_access/')

# TODO Fix with class-based view
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