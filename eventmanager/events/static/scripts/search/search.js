var base_url = "/events/search_json/";

$(function(){
	get_search_results();
});

function get_selected_category() {
	var e = document.getElementById("categories");
    return e.options[e.selectedIndex].value;
}

function get_search_string(){
	return $("#search_string").val();
}

function get_search_query(){
	if(get_search_string().length > 0){
		return base_url + get_selected_category() + "/" + get_search_string();
	}
	return base_url + get_selected_category();
}

function get_search_results(){
	var search = "<small> Search in progress.. </small>";
	$('.search_progress').append(search);
	var host = "http://0.0.0.0:8000",
		url = host + get_search_query(),
		xhttp = new XMLHttpRequest();

	$('.events').html("");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
			var obj = JSON.parse(this.responseText);

            $(".search_progress").html("");
            var res = "";
            $(".events").html("");
            $('.events').hide();

            Object.keys(obj).forEach(function(key) {
                var large = `<div class="card center-block">
								<div class="card-body">
									<h5 class="card-title"> ${obj[key].title} </h5>
									<p class="card-text"> ${obj[key].description}</p>
									<a href="/events/${obj[key].link}" class="btn btn-primary"> Open event </a>
								</div>
							</div>`;
				res += large;

            });
            $('.events').append(res);
            $('.events').show('slow');
        }
    };

    xhttp.open("GET", url, true);
    xhttp.send();
}

$('#categories').on('change', function() {
  get_search_results();
});

$('#search_string').on('keypress', function() {
	get_search_results();
});
