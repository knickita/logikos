x=document.cookie;
user = x.split(";")[0].split("=")[1];
user_hash = x.split(";")[1].split("=")[1];

function getResponseFromServer(data_to_send) {
  $.ajax({
  	type: 'GET',
  	url:"random?user="+user+"&hash="+user_hash+"&"+data_to_send,
  	timeout: 15000,
  	success: function(data) {
      eval(data);
  	},
  	error: function(XMLHttpRequest, textStatus, errorThrown) {
    }
	})
}

function vai_a_global(){
  window.location="global.html"
}

getResponseFromServer("contest=tecnici&action=update");