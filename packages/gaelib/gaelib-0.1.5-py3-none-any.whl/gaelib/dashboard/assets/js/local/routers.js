'use strict';


app.routers.SurveyRouter = Backbone.Router.extend({
  routes: {
    '': 'surveyops',
    '!/list/': 'list',
    '!/surveyops/': 'surveyops',
    '!/messages/': 'messageops',
    '!/workflow/' : 'workflow',
    '!/targetgroups/' : 'targetgroups',
    '!/targetgroup_survey_mapping/' : 'targetgroupsurveymap',
    '!/recipients/' : 'recipients',
    '!/targetgroup_contact_mapping/' : 'targetgroupcontactmap',
    '!/surveyresponse/' : 'surveyresponse',
    ':path': 'index'
  },

  initialize: function (options) {
    this.holder = options.holder;
    this.survey_model = options.survey_model;
    this.survey_collection = options.survey_collection;
    this.survey_list_template = options.survey_list_template;
    this.survey_list_view = options.survey_list_view;
    this.survey_detail_holder = options.survey_detail_holder;
    this.survey_detail_template = options.survey_detail_template;
    this.survey_detail_view = options.survey_detail_view;

    this.message_model = options.message_model;
    this.message_collection = options.message_collection;
    this.message_list_template = options.message_list_template;
    this.message_list_view = options.message_list_view;
    this.message_detail_holder = options.message_detail_holder;
    this.message_detail_template = options.message_detail_template;
    this.message_detail_view = options.message_detail_view;

    this.stepdata_model = options.stepdata_model;
    this.stepdata_collection = options.stepdata_collection;
    this.stepdata_list_template = options.stepdata_list_template;
    this.stepdata_list_view = options.stepdata_list_view;
    this.stepdata_detail_holder = options.stepdata_detail_holder;
    this.stepdata_detail_template = options.stepdata_detail_template;
    this.stepdata_detail_view = options.stepdata_detail_view;
    this.stepdata_response_collection = options.stepdata_response_collection ;
    this.stepdataMessagesCollection = options.stepdataMessagesCollection;

    this.targetgroup_model = options.targetgroup_model;
    this.targetgroup_collection = options.targetgroup_collection;
    this.targetgroup_list_template = options.targetgroup_list_template;
    this.targetgroup_list_view = options.targetgroup_list_view;
    this.targetgroup_detail_holder = options.targetgroup_detail_holder;
    this.targetgroup_detail_template = options.targetgroup_detail_template;
    this.targetgroup_detail_view = options.targetgroup_detail_view;

    this.targetgroupcontactmap_model = options.targetgroupcontactmap_model;
    this.targetgroupcontactmap_collection = options.targetgroupcontactmap_collection;
    this.targetgroupcontactmap_list_template = options.targetgroupcontactmap_list_template;
    this.targetgroupcontactmap_list_view = options.targetgroupcontactmap_list_view;
    this.targetgroupcontactmap_detail_holder = options.targetgroupcontactmap_detail_holder;
    this.targetgroupcontactmap_detail_template = options.targetgroupcontactmap_detail_template;
    this.targetgroupcontactmap_detail_view = options.targetgroupcontactmap_detail_view;

    this.targetgroupsurveymap_model = options.targetgroupsurveymap_model;
    this.targetgroupsurveymap_collection = options.targetgroupsurveymap_collection;
    this.targetgroupsurveymap_list_template = options.targetgroupsurveymap_list_template;
    this.targetgroupsurveymap_list_view = options.targetgroupsurveymap_list_view;
    this.targetgroupsurveymap_detail_holder = options.targetgroupsurveymap_detail_holder;
    this.targetgroupsurveymap_detail_template = options.targetgroupsurveymap_detail_template;
    this.targetgroupsurveymap_detail_view = options.targetgroupsurveymap_detail_view;

    this.contact_model = options.contact_model;
    this.contact_collection = options.contact_collection;
    this.contact_list_template = options.contact_list_template;
    this.contact_list_view = options.contact_list_view;
    this.contact_detail_holder = options.contact_detail_holder;
    this.contact_detail_template = options.contact_detail_template;
    this.contact_detail_view = options.contact_detail_view;

    this.surveyresponse_model = options.surveyresponse_model;
    this.surveyresponse_collection = options.surveyresponse_collection;
    this.surveyresponse_list_template = options.surveyresponse_list_template;
    this.surveyresponse_list_view = options.surveyresponse_list_view;
    this.surveyresponse_detail_holder = options.surveyresponse_detail_holder;
    this.surveyresponse_detail_template = options.surveyresponse_detail_template;
    this.surveyresponse_detail_view = options.surveyresponse_detail_view;
  },

  redirect: function (path) {
    this.navigate(path, {
      trigger: true,
      replace: false
    });
  },

  index: function (path) {
    this.redirect('!/surveyops/');
  },

  surveyops: function () {
    var survey_list_view = new this.survey_list_view({
      holder: this.holder,
      collection: this.survey_collection,
      model: this.survey_model,
      list_template: this.survey_list_template,
      detail_holder: this.survey_detail_holder,
      detail_template: this.survey_detail_template,
      detail_view: this.survey_detail_view,
      router: this
    });
  },
  messageops: function () {
    var message_list_view = new this.message_list_view({
      holder: this.holder,
      survey_collection: this.survey_collection,
      collection: this.message_collection,
      model: this.message_model,
      list_template: this.message_list_template,
      detail_holder: this.message_detail_holder,
      detail_template: this.message_detail_template,
      detail_view: this.message_detail_view,
      router: this
    });

  },
   workflow: function () {
    var stepdata_list_view = new this.stepdata_list_view({
      holder: this.holder,
      survey_collection: this.survey_collection,
      message_collection: this.message_collection,
      collection: this.stepdata_collection,
      model: this.stepdata_model,
      list_template: this.stepdata_list_template,
      detail_holder: this.stepdata_detail_holder,
      detail_template: this.stepdata_detail_template,
      detail_view: this.stepdata_detail_view,
      response_collection : this.stepdata_response_collection,
      stepdataMessagesCollection : this.stepdataMessagesCollection,
      router: this
    });
  },
  targetgroups: function(){
    var targetgroup_list_view = new this.targetgroup_list_view({
      holder: this.holder,
      survey_collection: this.survey_collection,
      collection: this.targetgroup_collection,
      model: this.targetgroup_model,
      list_template: this.targetgroup_list_template,
      detail_holder: this.targetgroup_detail_holder,
      detail_template: this.targetgroup_detail_template,
      detail_view: this.targetgroup_detail_view,
      router: this
    });
  },
  targetgroupcontactmap : function(){
    var targetgroupcontactmap_list_view = new this.targetgroupcontactmap_list_view({
      holder: this.holder,
      contact_collection: this.contact_collection,
      targetgroup_collection : this.targetgroup_collection,
      collection: this.targetgroupcontactmap_collection,
      model: this.targetgroupcontactmap_model,
      list_template: this.targetgroupcontactmap_list_template,
      detail_holder: this.targetgroupcontactmap_detail_holder,
      detail_template: this.targetgroupcontactmap_detail_template,
      detail_view: this.targetgroupcontactmap_detail_view,
      router: this
    });
  },

  targetgroupsurveymap: function(){
    var targetgroupsurveymap_list_view = new this.targetgroupsurveymap_list_view({
      holder: this.holder,
      survey_collection: this.survey_collection,
      targetgroup_collection : this.targetgroup_collection,
      collection: this.targetgroupsurveymap_collection,
      model: this.targetgroupsurveymap_model,
      list_template: this.targetgroupsurveymap_list_template,
      detail_holder: this.targetgroupsurveymap_detail_holder,
      detail_template: this.targetgroupsurveymap_detail_template,
      detail_view: this.targetgroupsurveymap_detail_view,
      router: this
    });
  },
  recipients : function(){
    var contact_list_view = new this.contact_list_view({
    holder: this.holder,
    collection: this.contact_collection,
    model: this.contact_model,
    list_template: this.contact_list_template,
    detail_holder: this.contact_detail_holder,
    detail_template: this.contact_detail_template,
    detail_view: this.contact_detail_view,
    router: this
    });
  },
  surveyresponse : function(){
    var surveyresponse_list_view = new this.surveyresponse_list_view({
    holder: this.holder,
    survey_collection : this.survey_collection,
    contact_collection : this.contact_collection,
    message_collection : this.message_collection,
    collection: this.surveyresponse_collection,
    model: this.surveyresponse_model,
    list_template: this.surveyresponse_list_template,
    detail_holder: this.surveyresponse_detail_holder,
    detail_template: this.surveyresponse_detail_template,
    detail_view: this.surveyresponse_detail_view,
    router: this
    });
  }
});
