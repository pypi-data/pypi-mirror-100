'use strict';


app.models.TargetGroupModel = Backbone.Model.extend({
  idAttribute: 'pk',

  defaults: function () {
    return {
      group_name: '',
      group_description: '',
    };
  },

  url: function () {
    var url = '/api/targetgroup/';

    var pk = this.attributes.pk;

    if (pk) {
      url = url + pk + '/';
    }

    return url;
  }
});



app.models.TargetGroupSurveyMapModel = Backbone.Model.extend({
  idAttribute : 'pk',
  SurveyId : 1,
  defaults : function(){
    return {
      survey : '',
      target_group : ''
    }
  },

  url : function(){
    var url = '/api/targetsurveymap/' +this.SurveyId+ '/survey/';

    var pk = this.attributes.pk;

    if (pk) {
      url = '/api/targetsurveymap/' + pk + '/';
    }

    return url;
  },
  setSurveyId : function(SurveyId){
    this.SurveyId = SurveyId;
  },
})

app.models.TargetGroupContactMapModel = Backbone.Model.extend({
  idAttribute : 'pk',
  TargetGroupId : 1,
  defaults : function(){
    return {
      contact : '',
      target_group : ''
    }
  },

  url : function(){
    var url = '/api/targetcontactmap/' +this.TargetGroupId+ '/targetgroup/';

    var pk = this.attributes.pk;

    if (pk) {
      url = '/api/targetcontactmap/' + pk + '/';
    }

    return url;
  },
  setTargetGroupId : function(TargetGroupId){
    this.TargetGroupId = TargetGroupId;
  },
})
