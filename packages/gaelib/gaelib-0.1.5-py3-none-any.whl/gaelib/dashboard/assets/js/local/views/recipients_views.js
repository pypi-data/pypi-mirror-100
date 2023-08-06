'use strict';


var contact_validation = {
      framework: 'bootstrap',
      fields: {
          contact_phone_number : {
              validators: {
                  notEmpty: {
                      message: 'Phone Number is required'
                  },
                  stringLength: {
                      min: 10,
                      // max: 13,
                      message: 'The phone number must be at least 10 characters long'
                  },
              }
          },
          contact_first_name : {
              validators: {
                  stringLength: {
                      max: 30,
                      message: 'First name must not be more than 30 characters'
                  },
              }
          },
          contact_last_name : {
              validators: {
                  stringLength: {
                      max: 30,
                      message: 'Last name must not be more than 30 characters'
                  },
              }
          },
      }
  };

app.views.ContactDetailView = DetailView.extend({
  type : 'contact',
  events : {
    'click #edit-contact': 'editForm',
    'click #destroy': 'destroyModal',},

  modal_id : "#contact-edit-modal",
  form_id : "#contactEditForm",
  validation_params : contact_validation,
  editForm : function(event){
    DetailView.prototype.editForm.call(this);
    $(this.modal_id + " input").each(function(){
      if ($(this).val() == 'Not Alloted'){
        $(this).val('');
      }
    });
  },
  commitForm : function(){
    $(this.modal_id + " input").each(function(){
      if( $(this).val() == "" ){
        $(this).val("Not Alloted");
      }
    });
    DetailView.prototype.commitForm.call(this);
  }

});

app.views.ContactListView = ListView.extend({
  type : 'contact',
  events :  { 'click #add-contact': 'addForm' },
  modal_id : '#contact-add-modal',
  form_id : "#contactAddForm",
  validation_params : contact_validation,
  initialize : function(options){
    this.holder = $(options.holder);
    this.collection = new options.collection();
    this.modelMaker = options.model;
    this.list_template = $(options.list_template);
    this.detail_holder = options.detail_holder;
    this.detail_template = options.detail_template;
    this.detail_view = options.detail_view;
    this.router = options.router;
    this.template = _.template(this.list_template.html());
    this.construct();
    this.listenTo(this.collection, 'reset', this.render);

  },
  commitForm: function(){
    this.model = new this.modelMaker();
    var newContact = this.formToModelMapper(this.form_id,this.type,'add')
    for(var i in newContact){
      if(newContact[i] == ''){
        delete newContact[i];
      };
    };
    if (newContact['contact_phone_number'].substring(0,2) != '+1'){
      newContact['contact_phone_number'] = '1' + newContact['contact_phone_number'];
    }
    this.model.set( newContact );
    this.model.save({}, {
        success: _.bind(function () {
          $(this.modal_id).modal('hide');
          this.collection.fetch({reset: true});
          this.render();
        }, this)
      });
  },
  construct: function() {
      this.collection.fetch({reset: true});
      this.$el.html(this.template);
      this.holder.html(this.el);
      this.detail_holder = $(this.detail_holder);
    },
  render_model: function(model){
        var detail_view = new this.detail_view({
            model: model,
            detail_template: this.detail_template,
            router: this.router
          });
         this.detail_holder.append(detail_view.render().el);
      }
});
