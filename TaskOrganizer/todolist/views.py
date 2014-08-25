from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from models import Project
from django.core.context_processors import csrf
from django.utils import timezone
from datetime import datetime, timedelta
from random import randrange
from todolist import taskViews, projectViews, deadlineStructures

from todolist.models import Project, Task, UserOptions
import heapq

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

        # Find projects with malleable unfinished tasks
        graphs = {}
        
        projectsWithMalleableTasks = Project.objects.filter(user = U, finished = 0)
        for project in projectsWithMalleableTasks :
            if project.containsMalleableTasks :
                graphs[project.id] = deadlineStructures.Graph(project)

        
        # Put the tasks with no unfinished prereqs into the heap
        taskQueue = []
        for key,value in graphs.iteritems():
            for idNum,node in value.reachableNodes.iteritems():
                taskQueue.append(node.task)

        heapq.heapify(taskQueue)

        print "Length : " + str(len(taskQueue))
        print "\n\n Starting to pull tasks out"

        # Loop until we have assigned deadlines to all of the tasks
        while(len(taskQueue) > 0):
            # get today's day of week
            dayOfWeek = deadline.weekday();

            # Get tasks due today, that is the tasks that are due before
            # the current deadline variable, but after 24 hours before it
            oneDayEarlier = deadline - timedelta(days = 1)
            tasksToday = Task.objects.filter(user = U, finished = 0).exclude(assigned = 0).exclude(deadline__gte=deadline).exclude(deadlineIsHard = 0).filter(deadline__gte=oneDayEarlier)

            # Get the amount of time the user has allocated for this day,
            # keep track of the difference
            opts = UserOptions.objects.filter(user = U)[0]
            timeRemaing = opts.timeForDay(dayOfWeek)

            # Subtract from the time remaining the amount of time already
            # used by tasks
            for t in tasksToday:
                timeRemaing -= t.timeAllocation


            # While time is greater than 0
            while(timeRemaing > 0 and len(taskQueue) > 0):
                # Get the first task from the queue
                newTask = heapq.heappop(taskQueue)
                print newTask.name

                # Add any new tasks which have it as their last dependencies
                # to the heap
                thisGraph = graphs[newTask.parent_project.id]
                tasksToAdd = thisGraph.popTask(newTask)
                for t in tasksToAdd:
                    heapq.heappush(taskQueue,t)

                # Set its deadline for the current deadline, subtract from
                # time remaining this task's allocated time
                newTask.deadline = deadline
                newTask.assigned = 1
                newTask.save()
                timeRemaing -= newTask.timeAllocation

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
        random_tasks = allTasks.filter(parent_project = None)

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
        'random_tasks' : random_tasks
        })
        return HttpResponse(template.render(context))
    else :
        return HttpResponseRedirect('/accounts/invalid')

def projectsTest(request, user_id):
    UList = User.objects.filter(id = user_id)

    
    
    if len(UList) < 1:
        return HttpResponseRedirect('/accounts/invalid')
    
    U = UList[0]
    if request.user.is_authenticated() and request.user == U:
        template = loader.get_template('todolist/projectsTest.html')
        context = RequestContext(request,{
            'user_id' : U.id,
            })
        return HttpResponse(template.render(context))
    else :
        return HttpResponseRedirect('/accounts/invalid')

def projectsNew(request, user_id):
    UList = User.objects.filter(id = user_id)

    
    
    if len(UList) < 1:
        return HttpResponseRedirect('/accounts/invalid')

    U = UList[0]
    if request.user.is_authenticated() and request.user == U:
        template = loader.get_template('todolist/projectsNew.html')

        rootProjects = Project.objects.filter(user = U, parentid = -1, finished = 0)
        projectIDs = []
        for project in rootProjects:
            projectIDs.append(project.id)

        rootTasks = Task.objects.filter(user = U, parent_project = None, finished = 0)
        taskIDs = []
        for task in rootTasks:
            taskIDs.append(task.id)
        

        context = RequestContext(request, {
            'user_id' : U.id,
            'projectIDs' : projectIDs,
            'taskIDs' : taskIDs,
            })
        return HttpResponse(template.render(context))
    else :
        return HttpResponseRedirect('/accounts/invalid')
