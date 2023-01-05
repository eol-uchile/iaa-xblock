function IterativeAssessedActivityStudent(runtime, element, settings) {

    let statusDiv = $(element).find('.status');

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
            buttonSubmit.removeAttr("disabled");
            buttonSubmit.html("<span>Enviar</span>")
            return "La respuesta debe tener como mínimo un largo de 10 caracteres."
        }
        return "";
    }

    function generateDocument() {
        const { AlignmentType, Document, HeadingLevel, Packer, Paragraph, TextRun, UnderlineType } = docx;
        let last_children = [];
        last_children.push(new Paragraph({
            text: settings.title,
            heading: HeadingLevel.HEADING_1,
            alignment: AlignmentType.CENTER
        }))
        last_children.push(new Paragraph({
            text: settings.activity_name,
            heading: HeadingLevel.HEADING_2,
            alignment: AlignmentType.CENTER
        }))
        last_children.push(
            new Paragraph({
                text: settings.user_id,
                italic: true,
                alignment: AlignmentType.CENTER
            }));
        last_children.push(new Paragraph({
            text: "",
            heading: HeadingLevel.HEADING_2,
        }))
        last_children.push(new Paragraph({
            text: settings.summary_text,
            heading: HeadingLevel.HEADING_2,
            alignment: AlignmentType.LEFT
        }))
        last_children.push(new Paragraph({
            text: "",
            heading: HeadingLevel.HEADING_2,
        }))
        for (let stage of settings.summary) {
            console.log(stage)
            console.log(settings.summary_list)
            if (settings.summary_list.split("").includes(stage[0].toString())){
                last_children.push(
                    new Paragraph({
                        text: "Fase " + stage[0] + " (" + stage[1] + ")",
                        heading: HeadingLevel.HEADING_2,
                    }))
                last_children.push(
                    new Paragraph({
                        text: stage[3],
                        italic: true
                    }));
                last_children.push(
                    new Paragraph({
                        text: "",
                    }))
                last_children.push(
                    new Paragraph({
                        text: stage[2],
                        alignment: AlignmentType.CENTER,
                        heading: HeadingLevel.HEADING_2
                    }))
                last_children.push(
                    new Paragraph({
                        text: "",
                    }))
            }
        }
        const doc = new Document({
            creator: "REDFID",
            title: "Resumen",
            description: "IAA Summary",
            styles: {
                paragraphStyles: [
                    {
                        id: "Heading1",
                        name: "Heading 1",
                        basedOn: "Normal",
                        next: "Normal",
                        quickFormat: true,
                        run: {
                            color: "999999",
                            size: 28,
                            bold: true
                        },
                        paragraph: {
                            spacing: {
                                after: 120,
                            },
                        },
                    },
                    {
                        id: "Heading2",
                        name: "Heading 2",
                        basedOn: "Normal",
                        next: "Normal",
                        quickFormat: true,
                        run: {
                            size: 20,
                            bold: true,
                        },
                        paragraph: {
                            spacing: {
                                before: 240,
                                after: 120,
                            },
                        },
                    },
                    {
                        id: "wellSpaced",
                        name: "Well Spaced",
                        basedOn: "Normal",
                        quickFormat: true,
                        paragraph: {
                            spacing: { line: 276, before: 20 * 72 * 0.1, after: 20 * 72 * 0.05 },
                        },
                    },
                    {
                        id: "ListParagraph",
                        name: "List Paragraph",
                        basedOn: "Normal",
                        quickFormat: true,
                    },
                ],
            },
            numbering: {
                config: [
                    {
                        reference: "my-crazy-numbering",
                        levels: [
                            {
                                level: 0,
                                format: "lowerLetter",
                                text: "%1)",
                                alignment: AlignmentType.LEFT,
                            },
                        ],
                    },
                ],
            },
            sections: [{
                children: last_children
            }],
        });

        docx.Packer.toBlob(doc).then(blob => {
            saveAs(blob, "example.docx");
        });
    }

    if (buttonReport != null){
        buttonReport.on("click", function (e) {
            e.preventDefault()
            buttonReport.attr("disabled", true);
            generateDocument();
            buttonReport.removeAttr("disabled");
        })
    }

    function afterSubmission(result) {
        statusDiv.removeClass("unanswered");
        statusDiv.removeClass('correct');
        statusDiv.addClass(result.indicator_class);
        if (result["msg"] !== "error") {
            showSuccessMessage("¡Respuesta enviada exitosamente!");
            submission.attr("disabled", true);
            buttonSubmit.attr("disabled", true);
        } else {
            showErrorMessage("Algo salió mal.");
            buttonSubmit.removeAttr("disabled");
        }
        buttonSubmit.html("<span>" + buttonSubmit[0].dataset.value + "</span>");
    }

    buttonSubmit.click(function (e) {
        e.preventDefault();
        buttonSubmit.html("<span>" + buttonSubmit[0].dataset.checking + "</span>");
        buttonSubmit.attr("disabled", true);
        if ($.isFunction(runtime.notify)) {
            runtime.notify('submit', {
                message: 'Submitting...',
                state: 'start'
            });
        }
        var data = { "submission": submission.val() }
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