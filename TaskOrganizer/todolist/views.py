from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from models import Project
from django.core.context_processors import csrf
from django.utils import timezone
from random import randrange

from todolist.models import Project, Task

def profile(request, user_id):
    UList = User.objects.filter(id = user_id)

    if len(UList) < 1:
        return HttpResponseRedirect('/accounts/invalid')

    U = UList[0]
    if request.user.is_authenticated() and request.user == U:
        # Show the user's profile, including stats and a link
        # to their projects page

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

            })

        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('accounts/invalid')
        

# Compares two tasks and determines which is more urgent,
# returning true if the second is more urgent than the first
# Generally, a task is more urgent if its deadline comes
# before that of another task. However, for each task that
# depends on one of the given tasks, that one's deadline
# moves up by two hours
def compareTasks(t1,t2):
    time1 = t1.deadline
    time2 = t2.deadline
    


# Helper function for determining an ordering on the most
# urgent tasks

def orderTasksByUrgency(tasks):
    return tasks.order_by("deadline")



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

        next_tasks = []
        urgent_tasks = []
        for t in allTasks:
            
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
    print result
    return result


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
            # Should be able to have tasks not attached to projects
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
        T = Ts[0] # Will cause problems if none are available
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