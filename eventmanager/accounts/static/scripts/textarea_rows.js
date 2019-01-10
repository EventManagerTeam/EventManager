$(document).ready(function(){
    $("textarea").attr({"rows": "1"});
});

jQuery(function($){
  $('#id_description')
    .focus(function(){ this.rows=4 });
});