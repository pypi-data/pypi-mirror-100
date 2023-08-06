'use strict';


app.models.ContactModel = Backbone.Model.extend({
  idAttribute : 'pk',
  default : function(){
    // contact_id = '';
    contact_first_name = '',
    contact_last_name = '',
    contact_email = '',
    contact_phone_number = ''
  },
  url : function(){
    var url = '/api/contact/'
    var pk = this.attributes.pk;
    if (pk){
      url = url + pk + '/';
    }
    return url;
  },

});
