function IterativeAssessedActivityStudent(runtime, element, settings) {

    let buttonSubmit = $(element).find(".iaa-submit");
    let buttonReport = $(element).find(".iaa-report-button");
    let submission = $(element).find(".iaa-submission");
    var handlerUrl = runtime.handlerUrl(element, 'student_submit');

    function showErrorMessage(msg) {
        $(element).find('#iaa-student-error-msg').html(msg);
    }

    function showWarningMessage(msg) {
        $(element).find('#iaa-student-warning-msg').html(msg);
    }

    function showSuccessMessage(msg) {
        $(element).find('#iaa-student-success-msg').html(msg);
    }

    function validate(data) {
        if (data.submission.length < 10) {
            return "La respuesta debe tener como mínimo un largo de 10 caracteres."
        }
        return "";
    }

    function generateDocument() {
        const doc = new docx.Document({
            sections: [{
                properties: {},
                children: [
                    new docx.Paragraph({
                        children: [
                            new docx.TextRun("Hello World"),
                            new docx.TextRun({
                                text: "Foo Bar",
                                bold: true,
                            }),
                            new docx.TextRun({
                                text: "\tGithub is the best",
                                bold: true,
                            }),
                        ],
                    }),
                ],
            }]
        });

        docx.Packer.toBlob(doc).then(blob => {
            console.log(blob);
            saveAs(blob, "example.docx");
            console.log("Document created successfully");
        });
    }

    buttonReport.on("click", function (e) {
        e.preventDefault()
        buttonReport.attr("disabled", true);
        generateDocument();
        buttonReport.removeAttr("disabled");
    })

    function afterSubmission(result) {
        if (result["msg"] !== "error") {
            showSuccessMessage("¡Respuesta enviada exitosamente!");
            submission.attr("disabled", true);
        } else {
            showErrorMessage("Algo salió mal.");
            buttonSubmit.removeAttr("disabled");
        }
    }

    buttonSubmit.on("click", function (e) {
        e.preventDefault();
        buttonSubmit.attr("disabled", true);
        if ($.isFunction(runtime.notify)) {
            runtime.notify('submit', {
                message: 'Submitting...',
                state: 'start'
            });
        }
        var data = { "submission": submission.val() }
        console.log(data);
        let error_msg = validate(data);
        if (error_msg !== "") {
            showErrorMessage(error_msg);
        } else {
            $.ajax({
                type: "POST",
                url: handlerUrl,
                data: JSON.stringify(data),
                success: afterSubmission
            });
            if ($.isFunction(runtime.notify)) {
                runtime.notify('submit', {
                    state: 'end'
                });
            }
        }
    });


    $(function ($) {
        if (submission.val() !== "") {
            submission.attr("disabled", true);
            buttonSubmit.attr("disabled", true);
        }
    });
}