'use strict';

var message_validation = {
        framework: 'bootstrap',
        fields: {
            short_name: {
                validators: {
                    notEmpty: {
                        message: 'The short name is required'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: 'The short name must be more than 6 and less than 30 characters long'
                    },
                }
            },
            content : {
              validators: {
                  notEmpty: {
                      message: 'The message content is required'
                  }
                }
            }
        }
      };


app.views.MessageDetailView = DetailView.extend({
  type : 'message',
  events : {
    'click #edit-message': 'editForm',
    'click #destroy': 'destroyModal'},
   modal_id : '#message-edit-modal',
   form_id :   '#messageEditForm',
   validation_params : message_validation,
   remove_any_response : function(responses){
    var inResponses = responses.split(",");
    if ($.inArray("*", inResponses) > -1){
      $("#message_any_edit_response").click();
      inResponses.splice($.inArray("*", inResponses),1);
      return inResponses.toString();
    } 
    return responses;
   },
    set_token : function(){  //sets tokens in messages
      $("#message_edit_responses").tokenfield({minWidth:300,
                                 createTokensOnBlur: true,
                                 beautify: false,});
      $("#message_edit_responses").tokenfield('setTokens', this.remove_any_response(this.model.attributes.responses));
      $("#message_edit_responses").on('tokenfield:edittoken', function () { return false }); // Disable editing tokens
    },
   editForm : function(){
      $(this.form_id + " div .token").remove();
      if ($("#message_any_edit_response").is(":checked")) $("#message_any_edit_response").click();
   		this.set_token();
   		DetailView.prototype.editForm.call(this);
   },
   commitForm : function(){
    var new_message = this.formToModelMapper(this.form_id,this.type,'edit');          // get all form inputs
    var responsesList = new_message.responses.split(",");
    if ($.inArray("",responsesList) > -1){                                                    // remove [""] if any
      responsesList.splice($.inArray("",responsesList),1);
    }
    if (new_message['any_response'] == true && $.inArray('*',responsesList) == -1){           // * required and doesn't exist
        responsesList.push("*");
    } else if(new_message['any_response'] == false && $.inArray('*',responsesList) > -1){     // * not required and exists
      responsesList.splice($.inArray('*',responsesList),1);
    }
    new_message.responses = responsesList.toString();
    this.model.set( new_message );                                                    
    this.model.save({}, {
        success: _.bind(function () {
          $(this.modal_id).modal('hide');
        }, this)
      });
  },
});




app.views.MessageListView = ListView.extend({
  type : 'message',
  events :  { 'click #add-message': 'addForm',
            'change #survey-selector': 'surveyChange',},
  modal_id : '#message-add-modal',
  form_id : "#messageAddForm",
  validation_params : message_validation,
   initialize: function (options) {    // Pending Task : 
    this.holder = $(options.holder);
    this.survey_collection = new options.survey_collection;
    this.modelMaker = options.model;
    this.list_template = $(options.list_template);
    this.detail_holder = options.detail_holder;
    this.detail_template = options.detail_template;
    this.detail_view = options.detail_view;
    this.router = options.router;
    this.viewOptions = options
    this.survey_collection.fetch({
      success: _.bind(function (collection, response, options){
                  this.survey_collection.setSelected(this.survey_collection.models[0].attributes.pk);
                  this.collection = new this.viewOptions.collection(this.survey_collection.getSelected());
                  this.template = _.template(this.list_template.html(), {surveys: this.survey_collection});
                  this.construct();
                  this.listenTo(this.collection, 'reset', this.render);
          }, this)
      });

  },
  addForm : function(){
  	$('#message_add_responses').tokenfield({minWidth:300,
                                 createTokensOnBlur: true,
                                 beautify: false,})
    $("#message_add_responses").tokenfield('setTokens', {});
  	ListView.prototype.addForm.call(this);
  },
  commitForm: function(){
    var new_message = this.formToModelMapper(this.form_id,this.type,'add');  // get all form inputs

    var responsesList = new_message.responses.split(",");
    if ($.inArray("",responsesList) > -1){
      responsesList.splice($.inArray("",responsesList),1);
    }
    if (new_message['any_response'] == true && $.inArray('*',responsesList) == -1){
        responsesList.push("*");
    } else if(new_message['any_response'] == false && $.inArray('*',responsesList) > -1){
      responsesList.splice($.inArray('*',responsesList),1);
    }
    new_message.responses = responsesList.toString();

    this.model = new this.modelMaker(this.survey_collection.getSelected());
    this.model.set( new_message );
    this.model.save({}, {
        success: _.bind(function () {
          $(this.modal_id).modal('hide');
          this.collection.fetch({async:false});
          this.render();
        }, this)
      });

  }
});  
