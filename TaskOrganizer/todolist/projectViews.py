from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from models import Task,Project
from django.utils import timezone
from datetime import datetime, timedelta
from random import randrange
from todolist import taskViews



def addproject(request):
    # If a user is authenticated and this is a post request, then
    # we proceed. Otherwise return an invalid page
    U = request.user
    if request.user.is_authenticated() and request.POST:
        deadline = request.POST.get('deadline')
        pid = int(request.POST.get('parentid'))
        projectname = request.POST.get('projectname')
        projectColor = taskViews.genRandomColor();


        P = Project(user=U,name=projectname,date_started=timezone.now(),deadline=deadline,date_finished=timezone.now(),parentid=pid,color=projectColor)
        P.save()

        # Loop through all the tasks posted with this project and create them as
        # unassigned tasks if they don't have deadlines

        index = 1;
        while not (request.POST.get(str(index)) is None):
            newTaskName = request.POST.get(str(index))
            taskDeadline = request.POST.get("time"+str(index))
            timeRequired = request.POST.get("timeReq"+str(index))
            index = index + 1
            if newTaskName == "":
                continue
            else:
                taskViews.createTaskForUserFromList(newTaskName,U,P,taskDeadline,timeRequired)

            
            

        return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else :
        return HttpResponseRedirect('/todolist/invalid_project_add')

def projectCardView(request, user_id, project_id):
    usersForID = User.objects.filter(id = user_id)
    

    if len(usersForID) == 1 and request.user.is_authenticated() and request.user == usersForID[0]:
        thisUser = usersForID[0]
        projectsWithID = Project.objects.filter(user = thisUser, id = project_id)
        if len(projectsWithID) != 1:
            # TODO
            return HttpResponseRedirect('/todolist/invalid_project_add')

        thisProject = projectsWithID[0]

        if thisProject.finished == 1:
            background_color = '#599c59'
        elif thisProject.isUrgent():
            background_color = '#FF3333'
        elif thisProject.deadlineIsGettingClose():
            background_color = '#FFFF33'
        else :
            background_color = '#599c59'

        d = thisProject.deadline
        deadline_date = str(d.month) + '/' + str(d.day) + '/' + str(d.year)

        taskAndProjectCount = thisProject.countSubprojectsAndTasks()
        subtask_count = taskAndProjectCount[0]
        subproject_count = taskAndProjectCount[1]

        subprojects = []
        for subProj in Project.objects.filter(user = thisUser, parentid = project_id):
            subprojects.append(subProj.id)

        subtasks = []
        for subTask in Task.objects.filter(user = thisUser, parent_project = thisProject):
            subtasks.append(subTask.id)

        template = loader.get_template('todolist/projectCard.html')
        contextDict = { 
            'project' : thisProject, 
            'background_color' : background_color, 
            'deadline_date' : deadline_date, 
            'subproject_count' : subproject_count,
            'subtask_count' : subtask_count,
            'subprojects' : subprojects,
            'subtasks' : subtasks
            }
        context = RequestContext(request, contextDict)
        return HttpResponse(template.render(context))
    else :
        return HttpResponseRedirect('accounts/invalid')


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
        if request.is_ajax():
            return HttpResponse('Success')
        else :
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
        
        if request.is_ajax():
            return HttpResponse('Success')
        else :
            return HttpResponseRedirect('/todolist/projects'+str(U.id))
    else:
        return HttpResponseRedirect('/todolist/invalid_project_add')


def demoteProject(request):
    # Have this project (which must have no subtasks or subprojects) be replaced by
    # a simple task
    U = request.user
    if request.user.is_authenticated() and request.POST:
        projectid = request.POST.get('projectid','')
        projectid = int(projectid)
        print projectid
        Ps = Project.objects.filter(id = projectid)
        # TODO Handle empty case?
        P = Ps[0]
        # TODO Wait am I checking for sub projects even?
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
        # TODO include task in this response
        if request.is_ajax():
            return HttpResponse('Success')
        else :
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
