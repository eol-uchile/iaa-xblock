function IterativeAssessedActivityInstructor(runtime, element, settings) {

    let buttonReport = $(element).find(".iaa-report-button");

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

    function generateDocument() {
        const { AlignmentType, Document, HeadingLevel, Packer, Paragraph, TextRun, UnderlineType } = docx;
        const doc = new Document({
            creator: "Clippy",
            title: "Sample Document",
            description: "A brief example of using docx",
            styles: {
                paragraphStyles: [
                    {
                        id: "Heading1",
                        name: "Heading 1",
                        basedOn: "Normal",
                        next: "Normal",
                        quickFormat: true,
                        run: {
                            size: 28,
                            bold: true,
                            italics: true,
                            color: "red",
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
                            size: 26,
                            bold: true,
                            underline: {
                                type: UnderlineType.DOUBLE,
                                color: "FF0000",
                            },
                        },
                        paragraph: {
                            spacing: {
                                before: 240,
                                after: 120,
                            },
                        },
                    },
                    {
                        id: "aside",
                        name: "Aside",
                        basedOn: "Normal",
                        next: "Normal",
                        run: {
                            color: "999999",
                            italics: true,
                        },
                        paragraph: {
                            indent: {
                                left: 720,
                            },
                            spacing: {
                                line: 276,
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
                children: [
                    new Paragraph({
                        text: "Test heading1, bold and italicized",
                        heading: HeadingLevel.HEADING_1,
                    }),
                    new Paragraph("Some simple content"),
                    new Paragraph({
                        text: "Test heading2 with double red underline",
                        heading: HeadingLevel.HEADING_2,
                    }),
                    new Paragraph({
                        text: "Option1",
                        numbering: {
                            reference: "my-crazy-numbering",
                            level: 0,
                        },
                    }),
                    new Paragraph({
                        text: "Option5 -- override 2 to 5",
                        numbering: {
                            reference: "my-crazy-numbering",
                            level: 0,
                        },
                    }),
                    new Paragraph({
                        text: "Option3",
                        numbering: {
                            reference: "my-crazy-numbering",
                            level: 0,
                        },
                    }),
                    new Paragraph({
                        children: [
                            new TextRun({
                                text: "Some monospaced content",
                                font: {
                                    name: "Monospace",
                                },
                            }),
                        ],
                    }),
                    new Paragraph({
                        text: "An aside, in light gray italics and indented",
                        style: "aside",
                    }),
                    new Paragraph({
                        text: "This is normal, but well-spaced text",
                        style: "wellSpaced",
                    }),
                    new Paragraph({
                        children: [
                            new TextRun({
                                text: "This is a bold run,",
                                bold: true,
                            }),
                            new TextRun(" switching to normal "),
                            new TextRun({
                                text: "and then underlined ",
                                underline: {},
                            }),
                            new TextRun({
                                text: "and back to normal.",
                            }),
                        ],
                    }),
                ],
            }],
        });

        docx.Packer.toBlob(doc).then(blob => {
            saveAs(blob, "example.docx");
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
