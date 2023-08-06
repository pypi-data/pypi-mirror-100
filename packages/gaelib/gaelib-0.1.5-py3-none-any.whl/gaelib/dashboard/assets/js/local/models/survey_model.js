'use strict';


app.models.SurveyModel = Backbone.Model.extend({
  idAttribute: 'pk',

  defaults: function () {
    return {
      survey_name: '',
      survey_description: '',
      frequency: 0,
      frequency_units: '',
    };
  },

  url: function () {
    var url = API_ENDPOINT;

    var pk = this.attributes.pk;

    if (pk) {
      url = API_ENDPOINT + pk + '/';
    }

    return url;
  }
});
