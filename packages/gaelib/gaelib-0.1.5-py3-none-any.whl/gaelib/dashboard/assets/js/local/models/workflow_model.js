'use strict';

app.models.stepdataModel = Backbone.Model.extend({
  idAttribute: 'pk',
  surveyId: '',
  messageId : '',

  defaults: function () {
    return {
      'survey' : '',
      'step_number' : '',
      'step_type' : '',
      'inbound_message' : '',
      'outbound_message' : '',
      'message_expecting_reply' : '',
      'time_to_wait_reply' : '',
      'time_to_wait_to_send_message' : '',
      'terminal' : ''
    };
  },
  initialize: function (surveyId) 
  { 
      if (typeof surveyId === "object")
        this.surveyId = surveyId.survey
      else
        this.surveyId = surveyId;
    },
  set_items : function(surveyId,messageId){
    this.surveyId = surveyId;
    this.messageId = messageId;
  },
  url: function () {
    var pk = this.attributes.pk;
    if (pk){
      var url = '/api/survey/'+this.surveyId+'/stepdata/'+pk+'/update/'; return url;
    }
    var url = '/api/survey/'+this.surveyId+'/stepdata/'+this.messageId+'/create/';
    return url;
  }
});