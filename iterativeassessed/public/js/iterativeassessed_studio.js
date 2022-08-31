function IterativeAssessedActivityStudio(runtime, element) {

    // falta un onChange del activity name que solo se active cuando ya sea distinto de null
    // esto se encargaría de cuando se quiera "editar" el bloque.

    // esconder activity_stage si es que es bloque summary


    // on load:

    // si stage es distinto de 0, inhabilitar los primeros 3 inputs (y esconder el extra). renderizar el resto. (EDICION)
    // si el stage es 0, solo renderizar activity name (CREACION)

    // activity_name : onchange:  (SOLO EN CREACION)
    // Al seleccionarse una existente, mostrar selector de tipos de bloques disponibles (full, display, summary)
    // Al seleccionarse nuevo, mostrar input adicional de nombre de actividad y selector de tipos de bloques disponibles
    // Queda cargado el bloque full por default

    // block_type : onchange: (SOLO EN CREACION)
    // Al seleccionarse summary, se muestra de input el texto de resumen (summary_text)
    // Al seleccionarse display, se muestran un selector de activity_name y uno de stage bloqueado.
        // al seleccionar actividad, se carga el selector de stage
    // Al seleccionar full, se muestran los selectores de display, y además el enunciado (question), stage_label, y el activity_stage siempre locked


    // EDICION
    // summary: summary_text
    // display: se muestran selector de activity_name y stage cargados. Al cambiar el stage no pasa nada, al cambiar activity_name, se vacía stage.
    // full: se muestran los selectores de display, y además el enunciado (question), stage_label, y el activity_stage siempre locked

    function validate(data){
        if(data.activity_name === null){
            return "Invalid activity name."
        }
        return "";
    }

    function showMessage(msg){
        $(element).find('.iaa-studio-error-msg').html(msg);
    }


    $(element).find('.save-button').bind('click', function(eventObject) {
      eventObject.preventDefault();
      var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

      var data = {
        activity_name: $(element).find('select.activity_name').val(),
      };
      var error_msg = validate(data);
      if (error_msg !== ""){
        showMessage(error_msg);
      } else {
        if ($.isFunction(runtime.notify)) {
            runtime.notify('save', {state: 'start'});
          }
          $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if ($.isFunction(runtime.notify)) {
              runtime.notify('save', {state: 'end'});
            }
          });
      }
    });
  
    $(element).find('.cancel-button').bind('click', function(eventObject) {
      eventObject.preventDefault();
      runtime.notify('cancel', {});
    });

    function onLoad() {
        let input_activity_name = $(element).find('#input_activity_name');
        let activity_name = $(element).find("#activity_name");
        let input_new_activity_name = $(element).find("#input_new_activity_name");
        let input_block_type = $(element).find("#input_block_type");
        let block_type = $(element).find("#block_type");
        let input_activity_stage = $(element).find("#input_activity_stage");
        let activity_stage = $(element).find("#activity_stage");
        let input_stage_label = $(element).find("#input_stage_label");
        let input_activity_name_previous = $(element).find("#input_activity_name_previous");
        let activity_name_previous = $(element).find("#activity_name_previous");
        let input_activity_stage_previous = $(element).find("#input_activity_stage_previous");
        let activity_stage_previous = $(element).find("#activity_stage_previous");
        let input_question = $(element).find("#input_question");
        let input_summary_text = $(element).find("#input_summary_text");
        if(parseInt(activity_stage.val()) == 0){
            input_activity_name.removeAttr("hidden");
            activity_name.on("change", function(){
                input_block_type.removeAttr("hidden");
                if (activity_name.val() == "new"){
                    input_new_activity_name.removeAttr("hidden");
                } else {
                    input_new_activity_name.attr("hidden", true)
                }
                block_type.on("change", function(){
                    if (block_type.val() === "full"){
                        input_activity_stage.removeAttr("hidden");
                        input_stage_label.removeAttr("hidden");
                        input_activity_name_previous.removeAttr("hidden");
                        input_activity_stage_previous.removeAttr("hidden");
                        input_question.removeAttr("hidden");
                        input_summary_text.attr("hidden", true);
                    } else if (block_type.val() === "display"){
                        input_activity_stage.attr("hidden", true);
                        input_stage_label.attr("hidden", true);
                        input_activity_name_previous.removeAttr("hidden");
                        input_activity_stage_previous.removeAttr("hidden");
                        input_question.attr("hidden", true);
                        input_summary_text.attr("hidden", true);
                    } else if (block_type.val() === "summary") {
                        input_activity_stage.attr("hidden", true);
                        input_stage_label.attr("hidden", true);
                        input_activity_name_previous.attr("hidden", true);
                        input_activity_stage_previous.attr("hidden", true);
                        input_question.attr("hidden", true);
                        input_summary_text.removeAttr("hidden");
                    }
                    if (block_type.val() !== "summary"){
                        activity_name_previous.on("change", function(){
                            // necesitamos las actividades y stages
                            // el selector de stages depende de la actividad
                        });
                    }
                });
                block_type.val("full").change();
            });
        } else {
            input_activity_name.removeAttr("hidden");
            activity_name.attr("disabled", true);
            input_block_type.removeAttr("hidden");
            block_type.attr("disabled", true);
            if (block_type.val() === "full"){
                input_activity_stage.removeAttr("hidden");
                input_stage_label.removeAttr("hidden");
                input_activity_name_previous.removeAttr("hidden");
                input_activity_stage_previous.removeAttr("hidden");
                input_question.removeAttr("hidden");
                input_summary_text.attr("hidden", true);
            } else if (block_type.val() === "display"){
                input_activity_stage.attr("hidden", true);
                input_stage_label.attr("hidden", true);
                input_activity_name_previous.removeAttr("hidden");
                input_activity_stage_previous.removeAttr("hidden");
                input_question.attr("hidden", true);
                input_summary_text.attr("hidden", true);
            } else if (block_type.val() === "summary") {
                input_activity_stage.attr("hidden", true);
                input_stage_label.attr("hidden", true);
                input_activity_name_previous.attr("hidden", true);
                input_activity_stage_previous.attr("hidden", true);
                input_question.attr("hidden", true);
                input_summary_text.removeAttr("hidden");
            }
            if (block_type.val() !== "summary"){
                activity_name_previous.on("change", function(){
                    // necesitamos las actividades y stages
                    // el selector de stages depende de la actividad
                });
            }
        }
    }
    onLoad();

  }