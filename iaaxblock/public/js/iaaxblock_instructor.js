function IterativeAssessedActivityInstructor(runtime, element, settings) {

    function showErrorMessage(msg) {
        $(element).find('.iaa-istructor-error-msg').html(msg);
    }

    function showWarningMessage(msg) {
        $(element).find('#iaa-instructor-warning-msg').html(msg);
    }

    function showSuccessMessage(msg) {
        $(element).find('#iaa-instructor-success-msg').html(msg);
    }

    function lockButtons(lock) {
        let buttons = $(element).find('.iaa-feedback-button');
        for (let button of buttons) {
            if (lock) {
                button.setAttribute("disabled", true);
            } else {
                button.removeAttribute("disabled");
            }
        }
    }

    function validate(data) {
        if (data.feedback.length < 10) {
            return "El feedback debe tener como mínimo un largo de 10 caracteres."
        }
        return "";
    }


    function afterSubmission(result) {
        if (result["msg"] !== "error") {
            showSuccessMessage("Feedback enviado.");
        } else {
            showErrorMessage("Algo salió mal.");
        }
        lockButtons(false);
    }

    $(element).find('.iaa-feedback-button').on('click', function (eventObject) {
        lockButtons(true);
        var handlerUrl = runtime.handlerUrl(element, 'instructor_submit');
        let student_id = eventObject.target.parentNode.parentNode.querySelector('th').innerHTML;
        let feedback = eventObject.target.parentNode.parentNode.querySelectorAll('td')[3].querySelector("textarea").value;
        let previous_datetime = eventObject.target.parentNode.parentNode.querySelectorAll('td')[4].innerText;
        console.log(previous_datetime);
        var data = {
            "id_student": student_id,
            "feedback": feedback
        }
        var error_msg = validate(data);
        if (error_msg !== "") {
            showErrorMessage(error_msg);
        } else {
            $.post(handlerUrl, JSON.stringify(data)).done(function (response) {
                afterSubmission(response)
            });
        }
    });
}
