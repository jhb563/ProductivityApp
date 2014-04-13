$(document).ready(function() {
    $(".addTaskForm").hide();
    $(".hideTaskForm").hide();
    $(".addProjectForm").hide();
    $(".hideProjectForm").hide();
    $(".ExpandButton").hide();

    var d = new Date();
    var month = d.getMonth()+1;
    var day = d.getDate();
    var output = d.getFullYear() + '-' + ((''+month).length<2 ? '0' : '') + month + '-' + ((''+day).length<2 ? '0' : '') + day;

    $(".datetimepicker").val(output+"T00:00:00");

    // Display the form to add a task and the button
    // to hide that form, while hiding the button
    // clicked
    $(".addTaskFormButton").click(function() {
    	$(this).siblings(".addTaskForm").show();
    	$(this).siblings(".hideTaskForm").show();

	    $(this).hide();
    });

    // Hide the addTask form while displaying the
    // addTaskForm button.
    $(".hideTaskForm").click(function() {
    	$(this).siblings(".addTaskForm").hide();
    	$(this).siblings(".addTaskFormButton").show();
    	$(this).hide();
    });


    // Similarly for projects
    $(".addProjectFormButton").click(function() {
    	$(this).siblings(".addProjectForm").show();
    	$(this).siblings(".hideProjectForm").show();
    	$(this).hide();
    });

    $(".hideProjectForm").click(function () {
    	$(this).siblings(".addProjectForm").hide();
    	$(this).siblings(".addProjectFormButton").show();
    	$(this).hide();
    });

    $(".MinimizeButton").click(function () {

        var project = $(this).parent();
        project.minimizeProject();

    });

    $(".ExpandButton").click(function () {

        var project = $(this).parent();
        project.expandProject();

    });
});

$.fn.minimizeProject = function () {
    $(this).children("ul").hide();
    $(this).children(".MinimizeButton").hide();
    $(this).children(".ExpandButton").show();
    $(this).children(".addProjectFormButton").hide();
    $(this).children(".addProjectForm").hide();
    $(this).children(".hideProjectForm").hide();
    $(this).children(".addTaskFormButton").hide();
    $(this).children(".addTaskForm").hide();
    $(this).children(".hideTaskForm").hide();
};

$.fn.expandProject = function () {
    $(this).children("ul").show();
    $(this).children(".MinimizeButton").show();
    $(this).children(".ExpandButton").hide();
    $(this).children(".addProjectFormButton").show();
    $(this).children(".addProjectForm").show();
    $(this).children(".hideProjectForm").show();
    $(this).children(".addTaskFormButton").show();
    $(this).children(".addTaskForm").show();
    $(this).children(".hideTaskForm").show();
    $(this).children(".addTaskForm").hide();
    $(this).children(".hideTaskForm").hide();
    $(this).children(".addProjectForm").hide();
    $(this).children(".hideProjectForm").hide();
}