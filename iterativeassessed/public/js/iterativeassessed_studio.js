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
        let context = $("#context-iaa").data()["context"];
        let activities = JSON.parse(context["activities"]);
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

        // XBlock is being created for the first time
        if(context["activity_stage"] === "0"){

            input_block_type.removeAttr("hidden");
            input_block_type.removeAttr("disabled");
            let block_type_options = [["full", "Completo"], ["display", "Sólo respuesta anterior"], ["summary", "Resumen"], ["none", "Por favor seleccione una opción..."]];
            for (let option of block_type_options){
                let opt = document.createElement("option");
                opt.value = option[0];
                opt.text = option[1];
                block_type.append(opt);
                if (option[0] === "none"){
                    opt.setAttribute("disabled", true);
                    opt.setAttribute("selected", true);
                }
            }

            block_type.on("change", function(){

                // All inputs are hidden
                input_activity_name.attr("hidden", true);
                activity_name.empty();
                input_new_activity_name.attr("hidden", true);
                input_activity_stage.attr("hidden", true);
                input_stage_label.attr("hidden", true);
                input_activity_name_previous.attr("hidden", true);
                input_activity_stage_previous.attr("hidden", true);
                input_question.attr("hidden", true);
                input_summary_text.attr("hidden", true);

                // Load activity_name input
                if (block_type.val() !== "display"){
                    input_activity_name.removeAttr("hidden");
                    activity_name.removeAttr("disabled");
                    for(let activity of activities){
                        let opt = document.createElement("option");
                        opt.value = activity[0];
                        opt.text = activity[1];
                        activity_name.append(opt);
                    }
                    if (block_type.val() === "full"){
                        let opt00 = document.createElement("option");
                        opt00.value = "new";
                        opt00.text = "Crear nueva actividad...";
                        activity_name.append(opt00);
                    }
                    let opt0 = document.createElement("option");
                    opt0.value = "new";
                    opt0.text = "Por favor seleccione una opción...";
                    opt0.setAttribute("disabled", true);
                    opt0.setAttribute("selected", true);
                    activity_name.append(opt0);
                }

                // After an activity is chosen, the rest of the inputs are shown
                activity_name.on("change", function(){
                    // The new activity name input is shown if a new activity is going to be created
                    if (activity_name.val() == "new"){
                        input_new_activity_name.removeAttr("hidden");
                    } else {
                        input_new_activity_name.attr("hidden", true)
                    }

                    if (block_type.val() === "full"){

                        // The activity stage is set
                        input_activity_stage.removeAttr("hidden");
                        if(activity_name.val() === "new"){
                            activity_stage.val("1");
                        } else {
                            for(let activity of activities){
                                if (activity[0].toString() === activity_name.val()){
                                    activity_stage.val((parseInt(activity[2]) + 1).toString());
                                }
                            }
                        }
                        input_stage_label.removeAttr("hidden");
                        input_question.removeAttr("hidden");
                        input_activity_name_previous.removeAttr("hidden");
                        activity_name_previous.empty();
                        for (let activity of activities){
                            let opt = document.createElement("option");
                            opt.value = activity[0];
                            opt.text = activity[1];
                            activity_name_previous.append(opt);
                        }
                        let opt0 = document.createElement("option");
                        opt0.value = "none";
                        opt0.text = "Por favor seleccione una opción...";
                        opt0.setAttribute("disabled", true);
                        opt0.setAttribute("selected", true);
                        activity_name_previous.append(opt0);
                        activity_name_previous.on("change", function(){
                            for(let activity of activities){
                                if (activity[0].toString() === activity_name_previous.val()){
                                    activity_stage_previous.attr("max", parseInt(activity[2]));
                                    activity_stage_previous.val(parseInt(activity[2]).toString());
                                    input_activity_stage_previous.removeAttr("hidden");
                                }
                            }
                        });
                    } 
                    
                    if (block_type.val() === "summary"){
                        input_summary_text.removeAttr("hidden");
                    }
                });

                if (block_type.val() === "display"){
                    input_activity_name_previous.removeAttr("hidden");
                    activity_name_previous.empty();
                    for (let activity of activities){
                        let opt = document.createElement("option");
                        opt.value = activity[0];
                        opt.text = activity[1];
                        activity_name_previous.append(opt);
                    }
                    let opt0 = document.createElement("option");
                    opt0.value = "none";
                    opt0.text = "Por favor seleccione una opción...";
                    opt0.setAttribute("disabled", true);
                    opt0.setAttribute("selected", true);
                    activity_name_previous.append(opt0);
                    activity_name_previous.on("change", function(){
                        for(let activity of activities){
                            if (activity[0].toString() === activity_name_previous.val()){
                                activity_stage_previous.attr("max", parseInt(activity[2]));
                                activity_stage_previous.val(parseInt(activity[2]).toString());
                                input_activity_stage_previous.removeAttr("hidden");
                            }
                        }
                    });
                }

            });


        // XBlock is being edited
        } else {
            input_block_type.removeAttr("hidden");
            block_type.attr("disabled", true);
            // seleccionar todo
            if (block_type.val() === "full"){
                input_activity_name.removeAttr("hidden");
                activity_name.attr("disabled", true);
                input_activity_stage.removeAttr("hidden");
                activity_stage.attr("disabled", true);
                input_stage_label.removeAttr("hidden");
                input_question.removeAttr("hidden");
                input_summary_text.attr("hidden", true);
            } else if (block_type.val() === "display"){
                input_activity_name.attr("hidden", true);
                input_activity_stage.attr("hidden", true);
                activity_stage.attr("disabled", true);
                input_stage_label.attr("hidden", true);
                input_question.attr("hidden", true);
                input_summary_text.attr("hidden", true);
            } else if (block_type.val() === "summary") {
                input_activity_name.removeAttr("hidden");
                activity_name.attr("disabled", true);
                input_activity_stage.attr("hidden", true);
                input_stage_label.attr("hidden", true);
                input_activity_name_previous.attr("hidden", true);
                input_activity_stage_previous.attr("hidden", true);
                input_question.attr("hidden", true);
                input_summary_text.removeAttr("hidden");
            }
            if (block_type.val() !== "summary"){
                input_activity_name_previous.removeAttr("hidden");
                activity_name_previous.empty();
                for (let activity of activities){
                    let opt = document.createElement("option");
                    opt.value = activity[0];
                    opt.text = activity[1];
                    activity_name_previous.append(opt);
                }
                // seleccionar
                activity_name_previous.on("change", function(){
                    for(let activity of activities){
                        if (activity[0].toString() === activity_name_previous.val()){
                            activity_stage_previous.attr("max", parseInt(activity[2]));
                            activity_stage_previous.val(parseInt(activity[2]).toString());
                            input_activity_stage_previous.removeAttr("hidden");
                        }
                    }
                });
                //seleccionar
            }
        }
    }
    onLoad();

  }