'use strict';


app.models.SurveyResponseModel = Backbone.Model.extend({
  idAttribute : 'pk',
  default : function(){
    survey = '',
    contact = '',
    last_msg = '',
    response = '',
    step_number = '',
    time_received = '',
    time_of_sending_last_message = '',
    valid = ''
  },
  // url : function(){
  //   var url = '/api/survey/response'
  // },
});
