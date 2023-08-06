'use strict';


var survey_validation = {
      framework: 'bootstrap',
      fields: {
          survey_name: {
              validators: {
                  notEmpty: {
                      message: 'The survey name is required'
                  },
                  stringLength: {
                      min: 6,
                      max: 30,
                      message: 'The survey name must be more than 6 and less than 30 characters long'
                  },
              }
          },
          survey_frequency: {
              validators: {
                  notEmpty: {
                      message: 'The survey frequency is required'
                  },
                  integer: {
                      message: 'The survey frequency must be a number'
                  },

              }
          },
      }
  };

app.views.SurveyDetailView = DetailView.extend({
  type : 'survey',
  events : {
    'click #edit-survey': 'editForm',
    'click #destroy': 'destroyModal',},

  modal_id : "#survey-edit-modal",
  form_id : "#surveyEditForm",
  validation_params : survey_validation

});

app.views.SurveyListView = ListView.extend({
  type : 'survey',
  events :  { 'click #add-survey': 'addForm' },
  modal_id : '#survey-add-modal',
  form_id : "#surveyAddForm",
  validation_params : survey_validation,
  commitForm: function(){
    this.model = new this.modelMaker();
    ListView.prototype.commitForm.call(this);
  }
});
