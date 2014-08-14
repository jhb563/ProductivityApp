from models import Task

# Data structures for assigning deadlines to tasks
# Nodes keep track of how many tasks have to finish
# before they can be assigned. They also keep references
# to all nodes which require them, so that they can
# inform their "children" to take away a requirement
# when the parent completes
class Node():
    def __init__(self,taskForNode):
        self.task = taskForNode
        self.numberOfRequirements = 0
        self.childNodes = []

    def addRequirement(self):
        self.numberOfRequirements += 1

    def removeRequirement(self):
        self.numberOfRequirements -= 1

    def addChild(self,childNode):
        self.childNodes.append(childNode)

# Build a graph so we can keep track of what tasks have requirements and which
# do not
class Graph():
    def __init__(self, project):
        self.allNodes = {}
        self.reachableNodes = {}
        allTasks = Task.objects.filter(parent_project = project, finished = 0, deadlineIsHard = 0)
        # First initialize a node for all of our tasks
        for task in allTasks:
            self.allNodes[task.id] = Node(task)

        # Then loop through the tasks again and determine if the nodes should be "reachable"
        # meaning added to the heap immediately, or have requirements
        for task in allTasks:
            if task.hasUnfinishedPrereqs() :
                print task.name + " has unfinished prereqs"
                thisNode = self.allNodes[task.id]
                for higherLevelTask in task.requiredTasks.all():
                    thisNode.addRequirement()
                    self.allNodes[higherLevelTask.id].addChild(thisNode)
            else :
                print task.name + " is reachable"
                self.reachableNodes[task.id] = self.allNodes[task.id]


            

    def popTask(self,taskToPop):
        results = []
        if taskToPop.id in self.reachableNodes:
            nodeForTask = self.reachableNodes[taskToPop.id]
            for node in nodeForTask.childNodes:
                node.removeRequirement()
                if node.numberOfRequirements == 0 :
                    self.reachableNodes[node.task.id] = node
                    results.append(node.task)
            self.reachableNodes[taskToPop.id] = None
        return results
