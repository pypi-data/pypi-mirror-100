'use strict';


app.models.MessageModel = Backbone.Model.extend({
  idAttribute: 'pk',
  surveyId: '',

  defaults: function () {
    return {
      survey_name: '',
      survey_description: ''
    };
  },
  initialize: function (surveyId) 
  { 
      if (typeof surveyId === "object")
        this.surveyId = surveyId.survey
      else
        this.surveyId = surveyId;
    },

  url: function () {
    var url = API_ENDPOINT + this.surveyId + '/message/';

    var pk = this.attributes.pk;

    if (pk) {
      url = url + pk + '/';
    }

    return url;
  }
});




app.models.reponseModel = Backbone.Model.extend({
  idAttribute: 'pk',

  defaults: function () {
    return {
      id: '',
      content: '',
    };
  },

  url: function () {
    var url = API_ENDPOINT;

    var pk = this.attributes.pk;

    if (pk) {
      url = '/api/repsonsemessage/' + pk + '/';
    }

    return url;
  }
});