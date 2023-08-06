'use strict';


app.collections.SurveyCollection = Backbone.Collection.extend({
  model: app.models.SurveyModel,

  url: function () {
    return API_ENDPOINT;
  },
  setSelected: function(selected){
    this.selectedId = selected;
  },
  getSelected: function(selected){
    return this.selectedId;
  },
  parse: function (response) {
    return response;
  }
});


app.collections.MessageCollection = Backbone.Collection.extend({
  model: app.models.MessageModel,
  surveyId: '',

  initialize: function (surveyId) {
    this.surveyId = surveyId;
  },
  url: function () {
    var url = API_ENDPOINT + this.surveyId + '/message/';
    return url;
  },

  parse: function (response) {
    return response;
  },
  set_survey_id: function(surveyId){
    this.surveyId = surveyId
  }
});

app.collections.stepdataCollection = Backbone.Collection.extend({
  model: app.models.stepdataModel,
  surveyId: '',
  messageId :'',

  initialize: function (surveyId,messageId) {
    this.surveyId = surveyId;
    this.messageId = messageId;
  },
  url: function () {
    var url = API_ENDPOINT + this.surveyId + '/stepdata/' + this.messageId + '/create/';
    return url;
  },
  set_messageId:function(messageId){
    this.messageId = messageId;
  },

  parse: function (response) {
    return response;
  },

});


app.collections.responseCollection = Backbone.Collection.extend({
  model: app.models.reponseModel,
  response_message_id: '',

  initialize: function (response_message_id) {
    this.response_message_id = response_message_id;
  },
  url: function () {

    var url = '/api/' + 'responsemessage/' + this.response_message_id + '/';
    return url;
  },

});


app.collections.stepdataMessagesCollection = Backbone.Collection.extend({
  model: app.models.reponseModel,
  stepdata_survey_id: '',

  initialize: function (stepdata_survey_id) {
    this.stepdata_survey_id = stepdata_survey_id;
  },
  url: function () {

    var url = '/api/' + 'responsemessage/' + this.stepdata_survey_id + '/';
    return url;
  },

});


app.collections.TargetGroupCollection = Backbone.Collection.extend({
  model: app.models.TargetGroupModel,

  url: function () {
    return '/api/targetgroup/';
  },
  setSelected: function(selected){
    this.selectedId = selected;
  },
  getSelected: function(selected){
    return this.selectedId;
  },
  parse: function (response) {
    return response;
  }
});



app.collections.TargetGroupSurveyMapCollection = Backbone.Collection.extend({
  model: app.models.TargetGroupSurveyMapModel,
  SurveyId : 1,
  initialize : function(SurveyId){
    this.SurveyId = SurveyId;
  },
  url: function () {
    return '/api/targetsurveymap/' +this.SurveyId+ '/survey/';
  },
  setSurveyId: function(SurveyId){
    this.SurveyId = SurveyId;
  },
  getSurveyId: function(SurveyId){
    return this.SurveyId;
  },
  parse: function (response) {
    return response;
  }
});

app.collections.ContactCollection = Backbone.Collection.extend({
  model : app.models.ContactModel,
  url : function(){
      return '/api/contact/';
    }
});

app.collections.TargetGroupContactMapCollection = Backbone.Collection.extend({
  model: app.models.TargetGroupContactMapModel,
  TargetGroupId : 1,
  initialize : function(TargetGroupId){
    this.TargetGroupId = TargetGroupId;
  },
  url: function () {
    return '/api/targetcontactmap/' +this.TargetGroupId+ '/targetgroup/';
  },
  setTargetGroupId: function(TargetGroupId){
    this.TargetGroupId = TargetGroupId;
  },
  getTargetGroupId: function(){
    return this.TargetGroupId;
  },
  parse: function (response) {
    return response;
  }
});


app.collections.SurveyResponseCollection = Backbone.Collection.extend({
  model : app.models.SurveyResponseModel,
  SurveyId : '' ,
  FilterStartDate : '',
  FilterEndDate : '',
  FilterParam : '',
  url : function(){
      if(this.FilterParam != ''){
        var url =  '/api/survey/response/' + this.SurveyId + '/' ;  
        url += this.FilterStartDate + '/';
        url +=  this.FilterEndDate + '/';
        url += this.FilterParam + '/';
        return url;
      }
      return '/api/survey/response/' + this.SurveyId + '/';
  },
  initialize : function(SurveyId){
    this.SurveyId = SurveyId;
    this.FilterParam = '';
  },
  filter_dates : function(param,startDate, endDate){
    this.FilterParam = param;
    this.FilterStartDate = startDate;
    this.FilterEndDate = endDate;
  } 
});