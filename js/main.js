function getResponseFromServer(data_to_send) {
  $.ajax({
  	type: 'GET',
  	url: "random?user="+user+"&"+"hash="+user_hash+"&"+data_to_send,
  	timeout: 15000,
  	success: function(data) {
      eval(data)
  	},
  	error: function(XMLHttpRequest, textStatus, errorThrown) {
    }
	})
}

user = "none"
user_hash = ""

function login(){
  user=$('#username').val()
  getResponseFromServer("contest=login&value="+$('#password').val())
}