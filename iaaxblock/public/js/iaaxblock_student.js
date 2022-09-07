function IterativeAssessedActivityStudent(runtime, element, settings) {

    let buttonSubmit = $(element).find(".iaa-submit");
    let submission = $(element).find(".submission")
    var handlerUrl = runtime.handlerUrl(element, 'student_submit');

    function afterSubmission(result){
        console.log(result)
        if (result["msg"] !== "error"){
            submission.attr("disabled", true);
        } else {
            buttonSubmit.removeAttr("disabled");
        }
    }

    buttonSubmit.on("click", function(e) {
        e.preventDefault();
        buttonSubmit.attr("disabled", true);
        if ($.isFunction(runtime.notify)) {
            runtime.notify('submit', {
                message: 'Submitting...',
                state: 'start'
            });
        }
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"submission": submission.val()}),
            success: afterSubmission
        });
        if ($.isFunction(runtime.notify)) {
            runtime.notify('submit', {
                state: 'end'
            });
        }
    });


    $(function ($) {
        if( submission.val() !== "" ){
            submission.attr("disabled", true);
            buttonSubmit.attr("disabled", true);
        }
    });
}