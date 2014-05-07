$(document).ready(function() {
    $(".addTaskForm").hide();
    $(".hideTaskForm").hide();
    $(".addProjectForm").hide();
    $(".hideProjectForm").hide();
    $(".ExpandButton").hide();
    $(".colorChangeForm").hide();
    $(".hideColorForm").hide();

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

    $(".showColorForm").click(function () {
        $(this).siblings(".colorChangeForm").show();
        $(this).siblings(".hideColorForm").show();
        $(this).hide();
    });

    $(".hideColorForm").click(function () {
        $(this).siblings(".colorChangeForm").hide();
        $(this).siblings(".showColorForm").show();
        $(this).hide();
    })

    $(".MinimizeButton").click(function () {

        var project = $(this).parent();
        project.minimizeProject();

    });

    $(".ExpandButton").click(function () {

        var project = $(this).parent();
        project.expandProject();

    });

    $(".addDynamicTaskButton").click(function () {
        // Select the table containing the tasks
        // It should be the element two before
        // the button that was pressed
        var table = $(this).prev().prev();

        // Get the number of the last input by using the
        // size of the table. This is the next number
        // we will use for the input tracking
        var nextNumber = table.find("tr").length;




        // Create new inputs and wrap them in data cells
        // also add each cell to a row item
        var newRow = $("<tr></tr>");

        var nameCell = $("<td></td>");
        var nameInput = $("<input type='text' name='"+nextNumber+"'>");
        nameCell.append(nameInput);
        newRow.append(nameCell);

        var timeLengthCell = $("<td></td>");
        var timeLengthInput = $("<input type='number' name='timeReq"+nextNumber+"' min='0' max='90' step='15'>");
        timeLengthCell.append(timeLengthInput);
        newRow.append(timeLengthCell);

        var priorityCell = $("<td></td>");
        var priorityInput = $("<input type='number' class='priorityInput' name='priority"+nextNumber+"' min='0'>");
        priorityCell.append(priorityInput);
        newRow.append(priorityCell);

        var deadlineCell = $("<td></td>");
        var deadlineInput = $("<input type='datetime-local' name='time"+nextNumber+"'>");
        deadlineCell.append(deadlineInput);
        newRow.append(deadlineCell);


        // Add the new row item to the table

        table.append(newRow);
    });

    $(".removeDynamicTaskButton").click(function () {
        // Remove the last row of the table (unless there's only
        //one row)
        var table = $(this).prev().prev();
        var tableChildren = table.children();
        if (tableChildren.length() >= 2) {
            var lastRow = table.children().last();
            lastRow.remove();
        }


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
    $(this).children(".showColorForm").hide();
    $(this).children(".colorChangeForm").hide();
    $(this).children(".hideColorForm").hide();
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
    $(this).children(".showColorForm").show();
}