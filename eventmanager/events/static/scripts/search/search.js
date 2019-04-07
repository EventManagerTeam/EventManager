var base_url = "/events/searchjson/";

$(document).ready(function(){console.log("HERE"); })
function get_selected_category() {
	var e = document.getElementById("categories");
	var value = e.options[e.selectedIndex].value;
    return value;
}

function get_search_string(){
	return document.getElementById("search_string").value;
}

function get_search_query(){
 	return base_url + get_selected_category() + "/" + get_search_string();
}

function get_search_results(){
	var host = "0.0.0.0:8000"
	var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    	console.log(host + get_search_query())
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText);
            console.log(obj + get_search_query())
        }
    };

    xhttp.open("GET", host + get_search_query(), true);
    xhttp.send();
}

$('#categories').on('change', function() {
  get_search_results();
});

$('#search_string').on('keydown', function() {
	get_search_results();
});
