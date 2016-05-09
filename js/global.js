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

getResponseFromServer("contest=global&action=update");

function my_remove(i){
	if (confirm("vuoi davvero cancellare: "+$("#titolo"+i).val()+" ?")){
		getResponseFromServer("contest=global&action=remove&line="+i)
	}
}

function vai_a_tecnici(){
  window.location="tecnici.html"
}

function my_pers_add(i){

}

function my_change(i){
  getResponseFromServer("contest=global&action=change&id="+i+"&value="+$('#'+i).val())
}

function aggiungi_tecnico(i){
  getResponseFromServer("contest=global&action=aggiungi_tecnico&line="+i+"&value="+$('#aggiungi_tecnico'+i).val())
}

function aggiungi_data(){
  k=prompt("Nome Evento")
  getResponseFromServer("contest=global&action=new_event&value="+k)
}