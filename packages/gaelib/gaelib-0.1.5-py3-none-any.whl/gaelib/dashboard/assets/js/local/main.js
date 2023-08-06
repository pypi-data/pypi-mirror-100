'use strict';


(function () {
  (function ($) {
    $(document).ready(function () {
      var router = new app.routers.SurveyRouter({
        holder: '#holder',

        survey_model: app.models.SurveyModel,
        survey_collection: app.collections.SurveyCollection,
        survey_list_template: '#survey-list-template',
        survey_list_view: app.views.SurveyListView,
        survey_detail_holder: '#survey-detail-holder',
        survey_detail_template: '#survey-detail-template',
        survey_detail_view: app.views.SurveyDetailView,

        message_model: app.models.MessageModel,
        message_collection: app.collections.MessageCollection,
        message_list_template: '#message-list-template',
        message_list_view: app.views.MessageListView,
        message_detail_holder: '#message-detail-holder',
        message_detail_template: '#message-detail-template',
        message_detail_view: app.views.MessageDetailView,

        stepdata_model: app.models.stepdataModel,
        stepdata_collection: app.collections.stepdataCollection,
        stepdata_response_collection : app.collections.responseCollection,
        stepdata_list_view: app.views.stepdataListView,   //Lists all stepdata
        stepdataMessagesCollection: app.collections.stepdataMessagesCollection,
        stepdata_detail_view: app.views.stepdataDetailView,
        stepdata_list_template: '#stepdata-list-template',
        stepdata_detail_holder: '#stepdata-detail-holder',
        stepdata_detail_template: '#stepdata-detail-template',

        targetgroup_model: app.models.TargetGroupModel,
        targetgroup_collection: app.collections.TargetGroupCollection,
        targetgroup_list_template: '#targetgroup-list-template',
        targetgroup_list_view: app.views.TargetGroupListView,
        targetgroup_detail_holder: '#targetgroup-detail-holder',
        targetgroup_detail_template: '#targetgroup-detail-template',
        targetgroup_detail_view: app.views.TargetGroupDetailView,

        targetgroupcontactmap_model: app.models.TargetGroupContactMapModel,
        targetgroupcontactmap_collection: app.collections.TargetGroupContactMapCollection,
        targetgroupcontactmap_list_template: '#targetgroupcontactmap-list-template',
        targetgroupcontactmap_list_view: app.views.TargetGroupContactMapListView,
        targetgroupcontactmap_detail_holder: '#targetgroupcontactmap-detail-holder',
        targetgroupcontactmap_detail_template: '#targetgroupcontactmap-detail-template',
        targetgroupcontactmap_detail_view: app.views.TargetGroupContactMapDetailView,

        targetgroupsurveymap_model: app.models.TargetGroupSurveyMapModel,
        targetgroupsurveymap_collection: app.collections.TargetGroupSurveyMapCollection,
        targetgroupsurveymap_list_template: '#targetgroupsurveymap-list-template',
        targetgroupsurveymap_list_view: app.views.TargetGroupSurveyMapListView,
        targetgroupsurveymap_detail_holder: '#targetgroupsurveymap-detail-holder',
        targetgroupsurveymap_detail_template: '#targetgroupsurveymap-detail-template',
        targetgroupsurveymap_detail_view: app.views.TargetGroupSurveyMapDetailView,

        contact_model: app.models.ContactModel,
        contact_collection: app.collections.ContactCollection,
        contact_list_template: '#contact-list-template',
        contact_list_view: app.views.ContactListView,
        contact_detail_holder: '#contact-detail-holder',
        contact_detail_template: '#contact-detail-template',
        contact_detail_view: app.views.ContactDetailView,

        surveyresponse_model: app.models.SurveyResponseModel,
        surveyresponse_collection: app.collections.SurveyResponseCollection,
        surveyresponse_list_template: '#surveyresponse-list-template',
        surveyresponse_list_view: app.views.SurveyResponseListView,
        surveyresponse_detail_holder: '#surveyresponse-detail-holder',
        surveyresponse_detail_template: '#surveyresponse-detail-template',
        surveyresponse_detail_view: app.views.SurveyResponseDetailView,
      });

      Backbone.history.start();

    });
  }(jQuery));
}).call(this);
