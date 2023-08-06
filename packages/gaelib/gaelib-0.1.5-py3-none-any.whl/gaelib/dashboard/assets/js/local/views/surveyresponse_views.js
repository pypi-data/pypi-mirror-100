'use strict';



app.views.SurveyResponseDetailView = DetailView.extend({
  type : 'surveyresponse',
});

app.views.SurveyResponseListView = ListView.extend({
  type : 'surveyresponse',
  events :  { 'click #add-surveyresponse': 'addForm',
              'change #survey-selector' : 'surveyChange',
               'click #download-report' : 'downloadReport',
               'click #received_time_filter' : 'received_time_filter'
               // 'click #last_msg_filter' : 'last_msg_filter'
                },
  modal_id : '#surveyresponse-add-modal',
  form_id : "#surveyresponseAddForm",
  downloadReport : function(){
    window.location.href = window.location.href.replace('#!/surveyresponse/','getSurveyResponseResport/') +
                           $('#survey-selector :selected')[0].value  + '/';
  },
  received_time_filter : function(event){
    var start_date = $(event.target).closest('.form').find('.start_date')[0].value;
    var end_date = $(event.target).closest('.form').find('.end_date')[0].value;
    
    $("#filter-alert").hide();
    if( end_date < start_date){$("#filter-alert").show(); return true}
    if( start_date == '' || end_date == ''){$("#filter-alert").show(); return true}

    this.collection.filter_dates('time_received',start_date,end_date);
    $("#received_time_label").css('color','black');  
    this.collection.fetch({reset : true,success: _.bind(function(){
        $("#received_time_label").css('color','red');
        this.render(); // Render on reset doesn't work after scroll to second survey
    },this)});
    
  },
  updateContent : function(){
    function replace_values(collection, class_name, find, to_replace){
      collection.fetch({async:false});
      collection.each(function(collection){
        var find_value = collection.attributes[find];
        var to_replace_value = collection.attributes[to_replace];
        $(class_name).each(function(){
          var text = $(this).text().trim();
          if (text == find_value){
            $(this).text(to_replace_value);
          }
        });
      });
    };

      replace_values(this.survey_collection, '.survey_name', 'pk', 'survey_name');
      replace_values(this.contact_collection, '.phone_number', 'pk', 'contact_phone_number' );
      
      this.message_collection.set_survey_id(this.survey_collection.getSelected());
      replace_values(this.message_collection, '.last_message', 'pk', 'short_name');      
  },
  initialize : function(options){
    this.holder = $(options.holder);
    this.survey_collection = new options.survey_collection;
    this.contact_collection = new options.contact_collection;
    this.message_collection = new options.message_collection;
    this.collection = new options.collection();
    this.modelMaker = options.model;
    this.list_template = $(options.list_template);
    this.detail_holder = options.detail_holder;
    this.detail_template = options.detail_template;
    this.detail_view = options.detail_view;
    this.router = options.router;
    this.viewOptions = options;
    this.survey_collection.fetch({
      success: _.bind(function(collection, response, options){
        this.survey_collection.setSelected(this.survey_collection.models[0].attributes.pk);
        this.collection = new this.viewOptions.collection(this.survey_collection.getSelected());
        // this.collection.fetch({async:false});
        this.template = _.template(this.list_template.html(), {'surveys': this.survey_collection});
        this.construct();
        this.listenTo(this.collection, 'reset', this.render);
        // this.updateContent();
      },this)
    });
  },
  render : function(){
    $("#updating-data").show();
    ListView.prototype.render.call(this);
    this.updateContent();
    $(".date").datepicker({
       dateFormat: "yy-mm-dd",
       maxDate : '+0D'
    });
    $('#updating-data').hide();
    // $(".date").datepicker('setDate',new Date());
  }
});
