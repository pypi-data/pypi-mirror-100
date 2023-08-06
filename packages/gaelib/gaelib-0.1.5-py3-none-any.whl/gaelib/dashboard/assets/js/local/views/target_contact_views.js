'use strict';


app.views.TargetGroupContactMapDetailView = DetailView.extend({
  type : 'targetgroupcontactmap',
  events : {
    // 'click #edit-targetgroupcontactmap': 'editForm',
    'click #destroy': 'destroyModal',},

  modal_id : "#targetgroupcontactmap-edit-modal",
  form_id : "#targetgroupcontactmapEditForm",
  validation_params : targetgroup_validation
});

app.views.TargetGroupContactMapListView = ListView.extend({
  type : 'targetgroupcontactmap',
  events :  { 'click #add-targetgroupcontactmap': 'addForm',
               'change #target-selector' : 'targetChange',
                'click .targetgroup-add-map' : 'addTArget',
   },
  modal_id : '#targetgroupcontactmap-add-modal',
  form_id : "#targetgroupAddForm",
  validation_params : targetgroup_validation,
  commitForm: function(){
    this.model = new this.modelMaker();
    ListView.prototype.commitForm.call(this);
  },
  addTArget: function(event){
    var target = $(event.target).closest("tr");
    var targetgroup = $("#target-selector :selected")[0].value;
    var model_json = {};
    model_json['target_group'] = targetgroup;
    model_json['contact'] = target.attr('value');
    this.model = new this.modelMaker();
    this.model.setTargetGroupId(targetgroup);
    this.model.set( model_json );
    this.model.save({}, {
        success: _.bind(function () {
          // $(this.modal_id).modal('hide');
          this.collection.fetch({reset: true});
          this.render();
        }, this)
      });
    target.hide();
  },
  addForm: function(){
    var to_add = "<tr value='<value>'><th><text></th><th><button class='btn btn-primary targetgroup-add-map'>Add</button></th></tr>"
    $("#targetgroupcontactmap_modal_list").html(' ');
    var valid_list = [];
    this.collection.each(function(collection){
      valid_list.push(collection.attributes['contact']);
    });
    this.contact_collection.each(function(collection){
      if ( $.inArray(collection.attributes['pk'], valid_list) > -1 ){return true};
      var contact_details = collection.attributes['contact_phone_number'];
      $("#targetgroupcontactmap_modal_list").append(to_add.replace('<value>',collection.attributes['pk']).replace('<text>',contact_details));
    });
    $(this.modal_id).modal('show');
  },
  updateList:function(){
    this.contact_collection.fetch({async:false});
    this.contact_collection.each(function(collection){
        $(".target_contact").each(function(){
          var text = $(this).text().trim();
          if (collection.attributes['pk'] == text){
            var contact_details = collection.attributes['contact_phone_number'];
            $(this).text(contact_details);
          };
        });
    });
  },
  targetChange : function(event){
    this.collection.setTargetGroupId(event.target.value);
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
    $("#targetgroupcontactmap-detail-holder").hide();
    $("#targetgroupcontactmap-detail-holder").html('');
    this.collection.each(this.render_model.bind(this));
    this.updateList();
    $("#targetgroupcontactmap-detail-holder").fadeIn();
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
