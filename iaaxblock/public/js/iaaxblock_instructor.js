function IterativeAssessedActivityInstructor(runtime, element, settings) {

    function validate(data){
        return "";
    }


    $(element).find('.feedback-button').on('click', function (eventObject) {
        eventObject.preventDefault();
        var handlerUrl = runtime.handlerUrl(element, 'instructor_submit');
        let student_id = parseInt(eventObject.target.parentNode.parentNode.querySelector('th').innerHTML);
        let feedback = eventObject.target.parentNode.parentNode.querySelectorAll('td')[3].querySelector("textarea").value;
        let previous_datetime = eventObject.target.parentNode.parentNode.querySelectorAll('td')[4].innerHTML;
        var error_msg = validate(data);
        if (error_msg !== "") {
            showMessage(error_msg);
        } else {
            var data = {
                "id_student": student_id,
                "feedback": feedback,
                "new": previous_datetime != "—"
            }
            console.log(data);
            // bloquear botones
            $.post(handlerUrl, JSON.stringify(data)).done(function (response) {
                // liberar botones
                // mensaje de exito
            });
        }
    });
}
