'use strict';

var SuperView = Backbone.View.extend({
  // Form Id maps to this.model elements
   form_to_model_json : {
      '#survey_edit_name' : 'survey_name',
      '#survey_edit_description' : 'survey_description',
      '#survey_edit_freq' : 'frequency',
      '#survey_edit_freq_units' : 'frequency_units',
      '#survey_edit_active' : 'active',

      '#message_edit_short_name' : 'short_name',
      '#message_edit_content' : 'content',
      '#message_edit_responses' : 'responses',
      '#message_any_edit_response' : 'any_response',

      // '#stepdata_edit_survey' : 'survey',
      '#stepdata_edit_step_number' : 'step_number',
      '#stepdata_edit_step_type' : 'step_type',
      '#stepdata_edit_inbound_message' : 'inbound_message',
      '#stepdata_edit_outbound_message' : 'outbound_message',
      '#stepdata_edit_message_expecting_reply' : 'message_expecting_reply',
      '#stepdata_edit_time_to_wait_for_reply' : 'time_to_wait_for_reply',
      '#stepdata_edit_time_to_wait_for_reply_units' : 'time_to_wait_for_reply_units',
      '#stepdata_edit_time_to_wait_to_send_message' : 'time_to_wait_to_send_message',
      '#stepdata_edit_time_to_wait_to_send_message_units' : 'time_to_wait_to_send_message_units',
      '#stepdata_edit_terminal' : 'terminal',

      '#targetgroup_edit_name' : 'group_name',
      '#targetgroup_edit_description' : 'group_description',

      '#contact_edit_first_name' : 'contact_first_name',
      '#contact_edit_last_name' : 'contact_last_name',
      '#contact_edit_email' : 'contact_email',
      '#contact_edit_phone_number': 'contact_phone_number'
  },
  // Resets form before editing ListView
  reset_form : function(form_id){
      $(form_id + " :input").each(function(){
         if ($(this).prop("tagName") == 'CHECKBOX'){
          $(this).prop("checked",false);
         }
         else if ($(this).prop("tagName") == 'SELECT'){
            $(this).val("Min");
          }
         else{
            $(this).val(''); };
      });
  },
  formToModelMapper : function(form,type,event){
    var form_fields = {}
      for(var i in this.form_to_model_json){
        var tag = i;
        var model = this.form_to_model_json[i];

        tag = tag.replace("edit",event);

        if (tag.indexOf(type) != -1 && !$(tag).is(":hidden")) {
          if ($(this).prop("tagName") == 'SELECT') {
            form_fields[model] =  $(tag + " :selected")[0].value;
          }
          else if( $(tag).attr("type") == "checkbox") {
            form_fields[model] =  $(tag).is(":checked" );
          }
          else {form_fields[model] = $(form).find(tag).val()};

          if(form_fields[model] == null){
            delete form_fields[model];
          }
      }
    };
    return form_fields;
  },
});

var DetailView = SuperView.extend({
    type : 'survey',
    tagName : 'tr',
    events : {},
    modal_id : '',
    form_id : '',
    validation_params : {},
    editForm : function(){
      for(var i in this.form_to_model_json){
        $(this.form_id).find(i).val( this.model.attributes[this.form_to_model_json[i]]);
        if ( $(i).attr('type') == "checkbox" ){
              $(i).prop('checked', this.model.attributes[this.form_to_model_json[i]]);
        }
      };
      this.add_form_validation();
    },
    add_form_validation : function(){
      $(this.form_id).formValidation('destroy');
      $(this.form_id).formValidation( this.validation_params ).on('success.form.fv', _.bind(function(e) {
              // Prevent form submission
              e.preventDefault();

              // Some instances you can use are
              var $form = $(e.target),        // The form instance
                  fv    = $(e.target).data('formValidation'); // FormValidation instance

              this.commitForm()
          }, this));
      $(this.modal_id).modal('show');
    },
    commitForm : function(){
      this.model.set( this.formToModelMapper(this.form_id,this.type,'edit') ); // calls mapper func to map form to models
      this.model.save({}, {
          success: _.bind(function () {
            $(this.modal_id).modal('hide');
          }, this)
        });
    },
    initialize : function(options){
      this.model = options.model;
      this.detail_template = $(options.detail_template);
      this.router = options.router;

      this.template = _.template(this.detail_template.html());

      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },
    destroyModal: function() {
        BootstrapDialog.show({
                type: BootstrapDialog.TYPE_WARNING,
                message: 'Are you sure about this?',
                buttons: [ {
                    label: 'Yes',
                    cssClass: 'btn-danger',
                    action: _.bind(function(dialogItself){
                        this.model.destroy();
                        dialogItself.close();
                    }, this)
                }, {
                    label: 'No',
                    cssClass: 'btn-default',
                    action: function(dialogItself){
                        dialogItself.close();
                    }
                }]
            });
      },

    render: function() {
      if ( 'responses' in this.model.attributes) {
        if (this.model.attributes.responses == "")
          var responses = []
        else
          var responses = this.model.attributes.responses.split(",")
        this.$el.html(this.template({
                                      short_name: this.model.attributes.short_name,
                                      content: this.model.attributes.content,
                                      responses: responses
                                    }));
        return this;
      } else{
      this.$el.html(this.template(this.model.attributes));
      return this;
      }
    }
});

var ListView = SuperView.extend({
  type : 'survey',
  tagName: 'div',
  className: 'table-responsive',
  events: {},
  modal_id : '',
  form_id : '',
  validation_params : {},
  surveyChange: function(event) {
    this.survey_collection.setSelected(event.target.value);
    this.collection = new this.viewOptions.collection(this.survey_collection.getSelected());
    this.collection.fetch({reset: true,
                           success: _.bind(function (){ this.render(); }, this)});

  },
  addForm: function(){
    this.reset_form(this.form_id);
    $(this.modal_id).modal('show');
    this.add_form_validation(this.form_id);
  },
  add_form_validation : function(form_id){
    $(form_id).formValidation('destroy');
    $(form_id).formValidation( this.validation_params ).on('success.form.fv', _.bind(function(e) {
            // Prevent form submission
            e.preventDefault();

            // Some instances you can use are
            var $form = $(e.target),        // The form instance
                fv    = $(e.target).data('formValidation'); // FormValidation instance

            this.commitForm();
        }, this));
  },

  commitForm: function(){
    this.model.set( this.formToModelMapper(this.form_id,this.type,'add') );
    this.model.save({}, {
        success: _.bind(function () {
          $(this.modal_id).modal('hide');
          this.collection.fetch({reset: true});
          this.render();
        }, this)
      });

  },

  initialize: function (options) {
    this.holder = $(options.holder);
    this.collection = new options.collection();
    this.modelMaker = options.model;
    this.list_template = $(options.list_template);
    this.detail_holder = options.detail_holder;
    this.detail_template = options.detail_template;
    this.detail_view = options.detail_view;
    this.router = options.router;

    this.template = _.template(this.list_template.html());

    this.construct();

    this.listenTo(this.collection, 'reset', this.render);

  },

  construct: function() {
      this.collection.fetch({reset: true});
      this.$el.html(this.template);
      this.holder.html(this.el);
      this.detail_holder = $(this.detail_holder);
    },

  render: function(){
    this.detail_holder.hide();
    this.detail_holder.html('');
    this.collection.each(this.render_model.bind(this));
    this.detail_holder.fadeIn();
  },

  render_model: function(model){
        var detail_view = new this.detail_view({
            model: model,
            detail_template: this.detail_template,
            router: this.router
          });
         this.detail_holder.append(detail_view.render().el);
      }
});
