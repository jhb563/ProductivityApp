var ipAddressAndPort = "127.0.0.1:8000";
var baseURL = "http://" + ipAddressAndPort + "/todolist/";
var baseProjectsURL = baseURL + "projects/";
var baseTasksURL = baseURL + "tasks/";
var finishProjectURL = baseURL + "finishProject/";
var deleteProjectURL = baseURL + "removeProject/";
var demoteProjectURL = baseURL + "demoteProject/";
var finishTaskURL = baseURL + "finishTask/";
var deleteTaskURL = baseURL + "removeTask/";
var promoteTaskURL = baseURL + "promoteTask/";

$(document).ready(function () {
	
	$("#projectIDs").children('input').each(function () {
		var projectID = $(this).val();
		var userID = $("#userID").val();
		// TODO Refactor this to
		// $(this).loadProject(baseProjectsURL + userID +"/" + projectID);
		$.get(baseProjectsURL + userID +"/" + projectID, function(data,status) {
			var newElement = $(data);

			newElement.click(function () {
				$(this).onProjectClick();
			});

			newElement.children(".finishProjectForm").submit(function() {
				$(this).finishProject();
				return false;
			});
			newElement.children(".demoteProjectForm").submit(function() {
				$(this).demoteProject();
				return false;
			});
			newElement.children(".deleteProjectForm").submit(function() {
				$(this).deleteProject();
				return false;
			});
			$("#projectsSection").append(newElement);
		});
	});

	$("#taskIDs").children('input').each(function () {
		var taskID = $(this).val();
		var userID = $("#userID").val();
		// TODO Refactor this to
		// $(this).loadTask(baseTasksURL + userID + "/" + taskID)
		$.get(baseTasksURL + userID + "/" + taskID, function(data,status) {
			
			var newElement = $(data);
			newElement.children(".finishTaskForm").submit(function() {
				$(this).finishTask();
				return false;
			});
			newElement.children(".demoteTaskForm").submit(function() {
				$(this).demoteTask();
				return false;
			});
			newElement.children(".deleteTaskForm").submit(function() {
				$(this).deleteTask();
				return false;
			});
			$("#tasksSection").append(newElement);
		});
	});

	

	$(".addProjectButton").click(function() {
		var projectID = $("#projectIDInput").val();
		var userID = $("#userID").val();
		$.get(baseProjectsURL + userID +"/" + projectID, function(data,status) {
			var newElement = $(data);
			$("#projects").append(newElement);
		});
	});

	$(".addTaskButton").click(function () {
		var taskID = $("#taskIDInput").val();
		var userID = $("#userID").val();
		$.get(baseTasksURL + userID + "/" + taskID, function(data,status) {
			
			var newElement = $(data);
			$("#tasks").append(newElement);
		});
	});
});

$.fn.onProjectClick = function() {
	$("#projectsSection").children().each(function () {
		$(this).remove();
	});
	$("#tasksSection").children().each(function () {
		$(this).remove();
	});

	var userID = $("#userID").val();
	var projectIDs = $(this).children(".subProjectIDs").first().children();
	projectIDs.each(function () {
		var thisID = $(this).val();
		var url = baseProjectsURL + userID +"/" + thisID;
		$(this).loadProject(url);
	});

	var taskIDs = $(this).children(".subTaskIDs").first().children();
	taskIDs.each(function() {
		var thisID = $(this).val();
		var url = baseTasksURL + userID + "/" + thisID;
		$(this).loadTask(url);
	});
}

$.fn.loadProject = function(url) {
	$.get(url, function(data,status) {
			var newElement = $(data);

			newElement.click(function () {
				$(this).onProjectClick();
			});

			newElement.children(".finishProjectForm").submit(function() {
				$(this).finishProject();
				return false;
			});
			newElement.children(".demoteProjectForm").submit(function() {
				$(this).demoteProject();
				return false;
			});
			newElement.children(".deleteProjectForm").submit(function() {
				$(this).deleteProject();
				return false;
			});
			$("#projectsSection").append(newElement);
		});
}

$.fn.loadTask = function(url) {
	$.get(url, function(data,status) {
			
			var newElement = $(data);
			newElement.children(".finishTaskForm").submit(function() {
				$(this).finishTask();
				return false;
			});
			newElement.children(".demoteTaskForm").submit(function() {
				$(this).demoteTask();
				return false;
			});
			newElement.children(".deleteTaskForm").submit(function() {
				$(this).deleteTask();
				return false;
			});
			$("#tasksSection").append(newElement);
		});
}

// TODO, refactor these methods? Pretty much the same.
$.fn.finishProject = function () {
	var form = $(this).parent();
	$.ajax({
		data: $(this).serialize(),
		type: $(this).attr("method"),
		url: $(this).attr("action"),
		success: function(data,status) {
			alert("Success");
		}
	});
}

$.fn.demoteProject = function () {
	var form = $(this).parent();
	$.ajax({
		data: $(this).serialize(),
		type: $(this).attr("method"),
		url: $(this).attr("action"),
		success: function(data,status) {
			alert("Success");
		}
	});
}

$.fn.deleteProject = function () {
	var form = $(this).parent();
	$.ajax({
		data: $(this).serialize(),
		type: $(this).attr("method"),
		url: $(this).attr("action"),
		success: function(data,status) {
			alert("Success");
		}
	});
}

$.fn.finishTask = function () {
	var form = $(this).parent();
	$.ajax({
		data: $(this).serialize(),
		type: $(this).attr("method"),
		url: $(this).attr("action"),
		success: function(data,status) {
			alert("Success");
		}
	});
}

$.fn.promoteTask = function () {
	var form = $(this).parent();
	$.ajax({
		data: $(this).serialize(),
		type: $(this).attr("method"),
		url: $(this).attr("action"),
		success: function(data,status) {
			alert("Success");
		}
	});
}

$.fn.deleteTask = function () {
	var form = $(this).parent();
	$.ajax({
		data: $(this).serialize(),
		type: $(this).attr("method"),
		url: $(this).attr("action"),
		success: function(data,status) {
			alert("Success");
		}
	});
}



