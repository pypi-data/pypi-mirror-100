'use strict';


var targetgroup_validation = {
      framework: 'bootstrap',
      fields: {
          group_name: {
              validators: {
                  notEmpty: {
                      message: 'The Targetgroup name is required'
                  },
                  stringLength: {
                      // min: 6,
                      max: 30,
                      message: 'The Targetgroup name must be more than 6 and less than 30 characters long'
                  },
              }
          },
          group_description: {
              validators: {
                  notEmpty: {
                      message: 'The Description is required'
                  },
              }
          },
      }
  };

app.views.TargetGroupDetailView = DetailView.extend({
  type : 'targetgroup',
  events : {
    'click #edit-targetgroup': 'editForm',
    'click #destroy': 'destroyModal',},

  modal_id : "#targetgroup-edit-modal",
  form_id : "#targetgroupEditForm",
  validation_params : targetgroup_validation

});

app.views.TargetGroupListView = ListView.extend({
  type : 'targetgroup',
  events :  { 'click #add-targetgroup': 'addForm' },
  modal_id : '#targetgroup-add-modal',
  form_id : "#targetgroupAddForm",
  validation_params : targetgroup_validation,
  commitForm: function(){
    this.model = new this.modelMaker();
    ListView.prototype.commitForm.call(this);
  }
});


app.views.TargetGroupSurveyMapDetailView = DetailView.extend({
  type : 'targetgroupsurveymap',
  events : {
    'click #edit-targetgroupsurveymap': 'editForm',
    'click #destroy': 'destroyModal',},

  modal_id : "#targetgroupsurveymap-edit-modal",
  form_id : "#targetgroupsurveymapEditForm",
  validation_params : targetgroup_validation
});

app.views.TargetGroupSurveyMapListView = ListView.extend({
  type : 'targetgroupsurveymap',
  events :  { 'click #add-targetgroupsurveymap': 'addForm',
               'change #survey-selector' : 'surveyChange',
                'click .targetgroup-add-map' : 'addTArget',
   },
  modal_id : '#targetgroupsurveymap-add-modal',
  form_id : "#targetgroupAddForm",
  validation_params : targetgroup_validation,
  commitForm: function(){
    this.model = new this.modelMaker();
    ListView.prototype.commitForm.call(this);
  },
  addTArget: function(event){
    var target = $(event.target).closest("tr");
    var survey = $("#survey-selector :selected")[0].value;
    var model_json = {};
    model_json['survey'] = survey;
    model_json['target_group'] = target.attr('value');
    this.model = new this.modelMaker();
    this.model.setSurveyId(survey);
    this.model.set( model_json );
    this.model.save({}, {
        success: _.bind(function () {
          // $(this.modal_id).modal('hide');
          this.collection.fetch({reset: true});
          this.render();
        }, this)
      });
    target.hide();
    // $(this.modal_id).modal('hide');
  },
  addForm: function(){
    var to_add = "<tr value='<value>'><th><text></th><th><button class='btn btn-primary targetgroup-add-map'>Add</button></th></tr>"
    $("#targetgroupsurveymap_modal_list").html(' ');
    var valid_list = [];
    this.collection.each(function(collection){
      valid_list.push(collection.attributes['target_group']);
    });
    this.targetgroup_collection.each(function(collection){
      if ( $.inArray(collection.attributes['pk'], valid_list) > -1 ){return true};
      $("#targetgroupsurveymap_modal_list").append(to_add.replace('<value>',collection.attributes['pk']).replace('<text>',collection.attributes['group_name']));
    });
    $(this.modal_id).modal('show');
  },
  updateList:function(){
    this.targetgroup_collection.fetch({async:false});
    this.targetgroup_collection.each(function(collection){
        $(".target_group_name").each(function(){
          var text = $(this).text().trim();
          if (collection.attributes['pk'] == text){
            $(this).text(collection.attributes['group_name']);
          };
        });
    });
  },
  surveyChange : function(evemt){
    // this.survey_collection.setSelected(event.target.value);
    this.collection.setSurveyId(event.target.value);
    this.collection.fetch({reset:true});
  },
  initialize: function (options) {
    this.holder = $(options.holder);
    this.collection = new options.collection();
    this.survey_collection = new options.survey_collection;
    this.targetgroup_collection = new options.targetgroup_collection;
    this.modelMaker = options.model;
    this.list_template = $(options.list_template);
    this.detail_holder = $(options.detail_holder);
    this.detail_template = options.detail_template;
    this.detail_view = options.detail_view;
    this.router = options.router;
    this.viewOptions = options;
    this.survey_collection.fetch({
      async:false,
      success:_.bind(function(collection,response,options){
        this.survey_collection.setSelected(this.survey_collection.models[0].attributes.pk);
        this.collection = new this.viewOptions.collection(this.survey_collection.getSelected());
        this.collection.fetch({async:false});
        this.template = _.template(this.list_template.html(), {surveys: this.survey_collection});
        this.render();
      }, this)
    });
    this.construct();

    this.listenTo(this.collection, 'reset', this.render);

  },
  render: function(){
    $("#targetgroupsurveymap-detail-holder").html('');
    this.collection.each(this.render_model.bind(this));
    this.updateList();
  },

  render_model: function(model){
        var detail_view = new this.detail_view({
            model: model,
            detail_template: this.detail_template,
            router: this.router
          });
         $("#targetgroupsurveymap-detail-holder").append(detail_view.render().el);
      }
});



app.views.TargetGroupContactMapDetailView = DetailView.extend({
  type : 'targetgroupsurveymap',
  events : {
    'click #edit-targetgroupsurveymap': 'editForm',
    'click #destroy': 'destroyModal',},

  modal_id : "#targetgroupsurveymap-edit-modal",
  form_id : "#targetgroupsurveymapEditForm",
  validation_params : targetgroup_validation
});

app.views.TargetGroupContactMapListView = ListView.extend({
  type : 'targetgroupsurveymap',
  events :  { 'click #add-targetgroupsurveymap': 'addForm',
               'change #survey-selector' : 'surveyChange',
                'click .targetgroup-add-map' : 'addTArget',
   },
  modal_id : '#targetgroupsurveymap-add-modal',
  form_id : "#targetgroupAddForm",
  validation_params : targetgroup_validation,
  commitForm: function(){
    this.model = new this.modelMaker();
    ListView.prototype.commitForm.call(this);
  },
  addTArget: function(event){
    var target = $(event.target).closest("tr");
    var survey = $("#survey-selector :selected")[0].value;
    var model_json = {};
    model_json['survey'] = survey;
    model_json['target_group'] = target.attr('value');
    this.model = new this.modelMaker();
    this.model.setSurveyId(survey);
    this.model.set( model_json );
    this.model.save({}, {
        success: _.bind(function () {
          // $(this.modal_id).modal('hide');
          this.collection.fetch({reset: true});
          this.render();
        }, this)
      });
    target.hide();
    // $(this.modal_id).modal('hide');
  },
  addForm: function(){
    var to_add = "<tr value='<value>'><th><text></th><th><button class='btn btn-primary targetgroup-add-map'>Add</button></th></tr>"
    $("#targetgroupsurveymap_modal_list").html(' ');
    var valid_list = [];
    this.collection.each(function(collection){
      valid_list.push(collection.attributes['target_group']);
    });
    this.targetgroup_collection.each(function(collection){
      if ( $.inArray(collection.attributes['pk'], valid_list) > -1 ){return true};
      $("#targetgroupsurveymap_modal_list").append(to_add.replace('<value>',collection.attributes['pk']).replace('<text>',collection.attributes['group_name']));
    });
    $(this.modal_id).modal('show');
  },
  updateList:function(){
    this.contact_collection.fetch({async:false});
    this.contact_collection.each(function(collection){
        $(".target_contact").each(function(){
          var text = $(this).text().trim();
          if (collection.attributes['pk'] == text){
            $(this).text(collection.attributes['contact_first_name']);
          };
        });
    });
  },
  surveyChange : function(evemt){
    // this.survey_collection.setSelected(event.target.value);
    this.collection.setSurveyId(event.target.value);
    this.collection.fetch({reset:true});
  },
  initialize: function (options) {
    this.holder = $(options.holder);
    this.collection = new options.collection();
    this.contact_collection = new options.contact_collection;
    this.targetgroup_collection = new options.targetgroup_collection;
    this.modelMaker = options.model;
    this.list_template = $(options.list_template);
    this.detail_holder = $(options.detail_holder);
    this.detail_template = options.detail_template;
    this.detail_view = options.detail_view;
    this.router = options.router;
    this.viewOptions = options;
    this.targetgroup_collection.fetch({
      async: false,
      success: _.bind(function(collection,response,options){
        // this.collection.setTargetGroupId(this.targetgroup_collection.models[0].attributes.pk);
        this.collection = new this.viewOptions.collection(this.targetgroup_collection.models[0].attributes.pk);
        this.collection.fetch({async:false});
        this.template = _.template(this.list_template.html(), {targetgroup: this.targetgroup_collection});
        this.render();
      },this)
    });
    this.construct();

    this.listenTo(this.collection, 'reset', this.render);

  },
  render: function(){
    $("#targetgroupcontactmap-detail-holder").html('');
    this.collection.each(this.render_model.bind(this));
    this.updateList();
  },

  render_model: function(model){
        var detail_view = new this.detail_view({
            model: model,
            detail_template: this.detail_template,
            router: this.router
          });
         $("#targetgroupcontactmap-detail-holder").append(detail_view.render().el);
      }
});
