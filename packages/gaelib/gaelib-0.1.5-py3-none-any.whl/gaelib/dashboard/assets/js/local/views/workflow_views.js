'use strict';

var message_validation = {
        framework: 'bootstrap',
        fields: {
            step_data_time: {
                validators: {
                    notEmpty: {
                        message: 'The Time is required'
                    },
                    stringLength: {
                        min: 0,
                        max: 4,
                        message: 'Enter a valid Time limit'
                    },
                }
            },
            inbound_message: {
                validators: {
                    notEmpty: {
                        message: 'Important! Select any one response'
                    },
                }
            },
            time: {
                validators: {
                    notEmpty: {
                        message: 'Important! Select any one'
                    },
                }
            },
            outbound_message: {
                validators: {
                    notEmpty: {
                        message: 'Important! Select any one message to send'
                    },
                }
            },
        }
      };

// Time calculation
function wait_time_calculation(key,new_stepdata){
  if (new_stepdata[key] == '0') return new_stepdata;

	var units = new_stepdata[key + "_units"];
	var time_value = new_stepdata[key];
	if (units == 0){
		time_value = Number(time_value) * 3600 ;
	} else if (units == 1){
		time_value = Number(time_value) * 60 ;
	} else if (units == 2){
		time_value = Number(time_value)  * 24 * 3600 ;
	};
	new_stepdata[key] = time_value;
  delete new_stepdata[key+"_units"];
	return new_stepdata;
};

// Time Reverse Calculation for Edit in modal
// function 


function step_type_calc(new_stepdata,form_id){
	// Step_Type Calulation
	if ($("#stepdata-message-selector :selected")[0].value == 0){
		delete new_stepdata['message_expecting_reply'];
		delete new_stepdata['inbound_message'];
		new_stepdata['step_type'] = '0';
	}
	else if(new_stepdata['inbound_message'] == '0'){
		new_stepdata['inbound_message'] = '';
		new_stepdata['step_type'] = '2';
		}
	else if($(form_id).find("[name='inbound_message'] :selected").attr('reponse_id') == '01'){
		// new_stepdata['inbound_message'] = '';
		new_stepdata['step_type'] = '3';
		}
	else{
		new_stepdata['step_type'] = '1';
	}
  // Terminal
  new_stepdata['terminal'] = true;
  if (new_stepdata['time_to_wait_for_reply'] > 0 ){
    new_stepdata['terminal'] = false;
  }
  // h/m/d to seconds
	new_stepdata =  wait_time_calculation('time_to_wait_for_reply',new_stepdata);
	new_stepdata =  wait_time_calculation('time_to_wait_to_send_message',new_stepdata);
	
	return new_stepdata;
};

var sample_option_element = '<option value="<value>"><text></option>';
app.views.stepdataDetailView = DetailView.extend({
  type : 'stepdata',
  events : {
    'click #edit-stepdata': 'editForm',
    'click #destroy': 'destroyModal'},
  modal_id : '#stepdata-edit-modal',
  form_id :   '#stepdataEditForm',
  validation_params : message_validation,

  waitForTimeEditFields: function(key){
  	var time_value = this.model.attributes[key];
  	var hour = time_value / 3600;
  	var minutes = time_value / 60;
  	var day = time_value / (24*3600);
  	if ( day >= 1){ // more than a day
  		$("#stepdata_edit_"+key).val(day);
  		$("#stepdata_edit_"+key+'_units').val('2');
  	}
  	else if ( hour >= 1 && hour <= 24 ){ // less than a day
  		$("#stepdata_edit_"+key).val(hour);
  		$("#stepdata_edit_"+key+'_units').val('0');
  	}
  	else if ( minutes <= 60 ){ // minutes
  		$("#stepdata_edit_"+key).val(minutes);
  		$("#stepdata_edit_"+key+'_units').val('1');
  	}
	},
   editForm : function(){
   		stepDataListViewproto.updateResponseMessage(this.model.attributes['message_expecting_reply']);

   		$("#stepdata_edit_message_expecting_reply").html(' ');
   		// when step_number == 0; hides irrelevant forms
   		var selected_message = $('#stepdata-message-selector :selected')[0];

   		if (this.model.attributes['step_number'] == '0'){
   			$("#inbound-edit-panel").hide();
   			$("#reply-edit-panel").hide();
   		} else {
   			$("#inbound-edit-panel").show();
   			$("#reply-edit-panel").show();
   			var editReplyOptions = sample_option_element.replace("<value>",selected_message.value);
	   		editReplyOptions = editReplyOptions.replace('<text>',selected_message.text.substring(20,1000));
	  		$("#stepdata_edit_message_expecting_reply").append(editReplyOptions);
   		}
   		if (this.model.attributes['terminal'] != true){
   			$(this.form_id).find(".stepdata-time-to-wait-reponse").show();
   			$(this.form_id).find(".stepdata-wait-response").click();
   		} else{
   			$(this.form_id).find(".stepdata-time-to-wait-reponse").hide();
   			$(this.form_id).find(".stepdata-no-wait-response").click();
   		}

   		//check for children to disable reseting waiting for response
   	// 	if(this.check_for_child(this.model.attributes['outbound_message']) > 0){
    //       $(this.form_id).find(".stepdata-no-wait-response").prop('disabled',true);
		  // } else{
			 //    $(this.form_id).find(".stepdata-no-wait-response").prop('disabled',false);
		  // }

      DetailView.prototype.editForm.call(this);
      
      this.waitForTimeEditFields('time_to_wait_for_reply');
      this.waitForTimeEditFields('time_to_wait_to_send_message');
      $("#stepdata_edit_inbound_message [value='"+this.model.attributes['inbound_message']+"']").prop('disabled',false);
      if( this.model.attributes['step_type'] == '2'){
        $("#stepdata_edit_inbound_message").val('0');
        $("#stepdata_edit_inbound_message [value='0']").prop('disabled',false);
      }
      if( this.model.attributes['step_type'] == '3'){ // when step data = 3, any reponse accepted 
        var anyResponseId = $(this.form_id).find("[name='inbound_message'] [value='"+ this.model.attributes['inbound_message'] +"']").val();
        $("#stepdata_edit_inbound_message").val(anyResponseId);
      };

    },
    commitForm : function(){
      var new_stepdata = this.formToModelMapper(this.form_id,this.type,'edit');

      new_stepdata['survey'] = $('#stepdata-survey-selector :selected')[0].value;
      new_stepdata = step_type_calc(new_stepdata,this.form_id);
      this.model.set( new_stepdata ); // calls mapper func to map form to models
      this.model.save({}, {
          success: _.bind(function () {
            $(this.modal_id).modal('hide');
            this.render();
            var value = $("#stepdata-message-selector :selected")[0].value;
            stepDataListViewproto.updateMessage(value);
            // $("#stepdata-message-selector").val(value);
          }, this)
        });
    },
    render: function() {
      this.$el.html(this.template(this.model.attributes));
      return this;
    },
    destroyModal: function() {
		if(this.check_for_child(this.model.attributes['outbound_message']) > 0){
			var message = $("#stepdata-message-selector [value='"+this.model.attributes['outbound_message'] +"']").text().trim();
			BootstrapDialog.show({
                type: BootstrapDialog.TYPE_WARNING,
                message: 'Delete Connected Workflow Steps for this message!<br>' + 'Select <b>'+ message + '</b> to delete connected item',
                buttons: [{
                    label : 'Force Delete',
                    cssClass : 'btn-danger',
                    action : _.bind(function(dialogItself){
                        this.model.destroy();
                        this.render();
                        var value = $("#stepdata-message-selector :selected")[0].value;
                        stepDataListViewproto.updateMessage(value);
                        // $("#stepdata-message-selector").val(value);
                        dialogItself.close();
                    }, this)
                  },{
                    label: 'Ok',
                    action: function(dialogItself){
                        dialogItself.close();
                    }
                }]
            });
            return true;
      	};
        BootstrapDialog.show({
                type: BootstrapDialog.TYPE_WARNING,
                message: 'Are you sure about this?',
                buttons: [ {
                    label: 'Yes',
                    cssClass: 'btn-danger',
                    action: _.bind(function(dialogItself){
                        this.model.destroy();
                        this.render();
                        var value = $("#stepdata-message-selector :selected")[0].value;
						            stepDataListViewproto.updateMessage(value);
						            // $("#stepdata-message-selector").val(value);
                        dialogItself.close();
                    }, this)
                }, {
                    label: 'No',
                    action: function(dialogItself){
                        dialogItself.close();
                    }
                }]
            });
      },
    check_for_child : function(message_id){
	var collection_message_id = stepDataListViewproto.collection.messageId;
	stepDataListViewproto.collection.set_messageId(message_id);
	stepDataListViewproto.collection.fetch({async:false});
	stepDataListViewproto.collection.set_messageId(collection_message_id); stepDataListViewproto.collection.fetch();
	if (stepDataListViewproto.collection.length == 1){
		if(stepDataListViewproto.collection.models[0].attributes['outbound_message'] == message_id){
			return 0;
		}
	}
	return stepDataListViewproto.collection.length;
	}

});

var stepDataListViewproto = '';

app.views.stepdataListView = ListView.extend({
  type : 'stepdata',
  events :  { 'click #add-stepdata': 'addForm',
              'change #stepdata-survey-selector': 'surveyChange',
              'change #stepdata-message-selector': 'messageChange',
              // 'change #stepdata_edit_message_expecting_reply' : 'updateFormResponseMessage',
              // 'change #stepdata_add_message_expecting_reply' : 'updateFormResponseMessage',
              'click .stepdata-wait-response' : 'stepdata_wait_response',
              'click .stepdata-no-wait-response' : 'stepdata_no_wait_response',
          	},
  modal_id : '#stepdata-add-modal',
  form_id : "#stepdataAddForm",
  validation_params : message_validation,
  step_number: 0,
  stepdata_wait_response: function(event){
  	$("#stepdata_add_time_to_wait_for_reply").val('0');
  	$("#stepdata_edit_time_to_wait_for_reply").val('0');
  	$(event.target).closest('form').find(".stepdata-time-to-wait-reponse").fadeIn();
  },
  stepdata_no_wait_response: function(event){
  	$("#stepdata_add_time_to_wait_for_reply").val('0');
  	$("#stepdata_edit_time_to_wait_for_reply").val('0');
  	$(event.target).closest('form').find(".stepdata-time-to-wait-reponse").fadeOut();
  },
  addForm: function(){
    // if ($("#stepdata-message-selector :selected")[0].value == '0' && $(".stepdata_detail_list").size() > 0){
    //   alert("Only One 'KICK OFF Message' is allowed");
    //   return true;
    // }

    $(this.form_id).find('input').each(function(){$(this).val(' ')});  //cleaning up form
    // this.updateResponseMessage($("#stepdata-message-selector :selected")[0].value); // Reset Response messages
    $("#stepdata_add_time_to_wait_for_reply").val('0');
  	$("#stepdata_add_message_expecting_reply").html(' ');
  	var selected_message = $('#stepdata-message-selector :selected')[0];
  	if(selected_message.value == 0){
  		$('#inbound-panel').hide();
  		$('#reply-panel').hide();
  	}
  	else{
  		$('#inbound-panel').show();
		  $('#reply-panel').show();	

		var editReplyOptions = sample_option_element.replace("<value>",selected_message.value).replace('<text>',selected_message.text.substring(20,1000));
  	$("#stepdata_add_message_expecting_reply").append(editReplyOptions);
  		// $("#stepdata_add_outbound_message [value = '"+selected_message+"']").prop('disabled',true);
  	}
  	$(".stepdata-time-to-wait-reponse").hide();
    $(this.modal_id).modal('show');
    this.add_form_validation(this.modal_id);
    $(this.form_id).find(".stepdata-no-wait-response").click();
  },
   commitForm: function(){
 		var new_stepdata = this.formToModelMapper(this.modal_id,this.type,'add');
    new_stepdata = step_type_calc(new_stepdata,this.form_id);

   	new_stepdata['step_number'] = '0';
		new_stepdata['survey'] = $('#stepdata-survey-selector :selected')[0].value;
		this.model = new this.modelMaker();
		this.model.set_items(new_stepdata['survey'],new_stepdata['outbound_message']);
		this.model.set( new_stepdata ); // calls mapper func to map form to models
	    this.model.save({}, {
	        success: _.bind(function () {
	          $(this.modal_id).modal('hide');
	          this.collection.fetch({async:false}); this.render();
	          var value = $("#stepdata-message-selector :selected")[0].value;
            this.updateMessage(value);
              // $("#stepdata-message-selector").val(value);
	        }, this)
	      });
	    
  },
  // fires when message drop down is changed
  messageChange:function(event){
  	this.collection.set_messageId(event.target.value);
  	this.collection.fetch({reset:true,async:false}); this.render();
  	this.message_collection.each(function(message){
    	$(".sent_message_list").each(function(){
    		var text = $(this).text().trim();
	    	if (text == message.get('pk')){
	    		$(this).text(message.get('short_name') + " : " + message.get('content').substring(0,20));
	    	}
	    });

	    $(".message_expecting_reply_list").each(function(){
			var text = $(this).text().trim();
	    	if (text == message.get('pk')){
	    		$(this).text(message.get('short_name') + " : " + message.get('content').substring(0,20));
	    	}
    	});
    });
    // this.updateMessage(event.target.value);
    this.updateResponseMessage(event.target.value);

  },
  // updateFormResponseMessage: function(event){
  // 	var target = event.target.value;
  // 	this.updateResponseMessage(target);
  // },
  updateResponseMessage:function(message_id){
  	this.response_collection.initialize(message_id);
    this.response_collection.fetch({async:false});
    $("#stepdata_add_inbound_message").html(' '); $("#stepdata_edit_inbound_message").html(' ');
    if (message_id != '0'){
    	this.response_collection.each(function(message){
	    	var temp = "<option value="+message.get('id')+">the response is "+ message.get('content') +"</option>";
	    	$("#stepdata_edit_inbound_message").append(temp);
	    	$("#stepdata_add_inbound_message").append(temp);

    		$(".inbound_message_list").each(function(){
	    		var text = $(this).text().trim();
	    		if (text == message.get('content')){  // would fail if message content is Number. Not tested
	    			$("#stepdata_edit_inbound_message [value='"+ message.get('id') +"']").prop('disabled',true);
		    		$("#stepdata_add_inbound_message [value='"+ message.get('id') +"']").prop('disabled',true);
	    		}
	    		if (text == message.get('id')){ // editOutboundMessages not getting updated
	    			$(this).text(message.get('content'));
		    		$("#stepdata_edit_inbound_message [value='"+ message.get('id') + "']").prop('disabled',true);
		    		$("#stepdata_add_inbound_message [value='"+ message.get('id') + "']").prop('disabled',true);
		    	}
    		});
	    });    	
    }
    
    $("#stepdata_add_inbound_message").append("<option value='0'>there is no response</option>");
    var anyResponse = $("#stepdata_add_inbound_message option:contains('*')");
    anyResponse.text('any response comes in');
    anyResponse.attr('reponse_id', '01');

    $("#stepdata_edit_inbound_message").append("<option value='0'>there is no response</option>");
    var anyResponse = $("#stepdata_edit_inbound_message option:contains('*')");
    anyResponse.text('any response comes in');
    anyResponse.attr('reponse_id', '01');
    // $("#stepdata_edit_inbound_message option:contains('*')").text('any response comes in');

    // disable no/any response
    if( $(".no_response_list").length > 0 ) {
    	$("#stepdata_add_inbound_message [value='0']").prop('disabled',true);
    	$("#stepdata_edit_inbound_message [value='0']").prop('disabled',true);	
    };
    if( $(".any_response_list").length > 0 ){
    	$("#stepdata_add_inbound_message [reponse_id='01']").prop('disabled',true);
    	$("#stepdata_edit_inbound_message [reponse_id='01']").prop('disabled',true);
    };

  },
  check_messages_for_survey:function(){  // Returns all messages with terminal == False
  	var message_id = this.collection.messageId;
  	this.collection.set_messageId('01');
    this.collection.fetch({async:false});
    this.collection.set_messageId(message_id);
    var valid_messages = [];
    
    this.collection.each(function(collection){
    	var outbound_message = collection.get('outbound_message');
    	var terminal = collection.get('terminal');
    	if (outbound_message != null && terminal == false )
    		valid_messages.push(outbound_message);
    });
    valid_messages.sort();
    if (valid_messages.length == 0){
    	valid_messages.push('0');
    }
    return valid_messages;
  },
  // updates dropdown values.
  updateMessage : function(message_selector){
  	var list_of_drop_downs = [
  		'#stepdata_edit_outbound_message',
  		'#stepdata_add_outbound_message',
  		'#stepdata_add_message_expecting_reply',
  		'#stepdata_edit_message_expecting_reply',
  		'#stepdata-message-selector'
  	];
  	for(var item in list_of_drop_downs){
    		$(list_of_drop_downs[item]).html(' ');
    	}
    this.message_collection.each(function(message){
    	var text = "<option value='"+message.get('pk')+"'>"+message.get('short_name')+" : "+ message.get('content').substring(0,20) +"</option>";
		$("#stepdata_edit_outbound_message").append(text);
		$("#stepdata_add_outbound_message").append(text);
    });
	
	var valid_messages = this.check_messages_for_survey();
	// this.collection.set_messageId(valid_messages[0]);
	// this.collection.fetch({async:false});

	this.message_collection.each(function(message){
		$(".sent_message_list").each(function(){
			var text = $(this).text().trim();
	    	if (text == message.get('pk')){
	    		$(this).text(message.get('short_name') + " : " + message.get('content').substring(0,20));
	    	}
    	});
		$(".message_expecting_reply_list").each(function(){
			var text = $(this).text().trim();
	    	if (text == message.get('pk')){
	    		$(this).text(message.get('short_name') + " : " + message.get('content').substring(0,20));
	    	}
    	});
		if( $.inArray(message.get('pk'), valid_messages) == -1 ) return true;
		var text = "<option value='"+message.get('pk')+"'>  Handle responses to "+message.get('short_name')+" : "+ message.get('content').substring(0,20) +"</option>";
		$("#stepdata-message-selector").append(text);
		// to test if correct survey+message stepdata is visible
	});	

	var text = "<option value='0'>Kick Off Message</option>";
	$("#stepdata-message-selector").append(text);
  $("#stepdata-message-selector").val(message_selector);

  this.updateResponseMessage($("#stepdata-message-selector :selected")[0].value);

  },
  // fires when survey dropdown is changed
  surveyChange: function(event) {
    this.survey_collection.setSelected(event.target.value);
    this.collection.initialize(event.target.value,0);
    this.message_collection.set_survey_id(event.target.value);
    this.message_collection.fetch({async:false});
    if (this.message_collection.length > 0){
    	$("#message_selector").show();
    	this.collection.fetch({reset:true,async:false}); this.render();
	    this.updateMessage(0);
    }
    else{
    	$("#stepdata-message-selector").html(' ');
    	$("#stepdata_add_outbound_message").html(' ');
    	$("#stepdata_edit_outbound_message").html(' ');
    	$("#message_selector").hide();
    	this.collection.fetch({async:false});
    	this.render();
    }    
    
  },
   initialize: function (options) {    // Pending Task : 
    this.holder = $(options.holder);
    this.survey_collection = new options.survey_collection;
    this.message_collection = new options.message_collection;
    this.modelMaker = options.model;
    this.list_template = $(options.list_template);
    this.detail_holder = options.detail_holder;
    this.detail_template = options.detail_template;
    this.detail_view = options.detail_view;
    this.router = options.router;
    this.viewOptions = options;
    this.response_collection = new options.response_collection;
    this.survey_collection.fetch({
    	async:false,
      success: _.bind(function (collection, response, options){
                  this.survey_collection.setSelected(this.survey_collection.models[0].attributes.pk);
                  this.collection = new this.viewOptions.collection(this.survey_collection.getSelected());
                  this.message_collection.initialize(this.survey_collection.getSelected());
                  this.message_collection.fetch({async:false});
                  this.collection.set_messageId(0);
                  this.template = _.template(this.list_template.html(),
                  				 {surveys: this.survey_collection
                  				  });
                  this.construct();
                  stepDataListViewproto = this;
                  // this.listenTo(this.collection, 'reset', this.render);  // Makes an async call when assigning listenTo
                  this.collection.fetch({async:false});
                  this.render(); 
                  this.updateMessage(0);
          }, this)
      });
  },
});  