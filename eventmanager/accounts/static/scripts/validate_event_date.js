var now = new Date(),
    minDate = now.toISOString().substring(0,10);
    maxDate = new Date("December 31 9999 00:00");

var max_date_message = "Please use a date before December 31 9999 00:00",
    minDateMessage = "Please use a date in the future";

$("#starts_at").change(function() {
    startsAt = $('#starts_at').val()
    startsAt = new Date(starts_at);

    if(startsAt < minDate){
        $(".start_h").text(minDateMessage)
        $(".start_h").removeClass("hidden")
    } else if(startsAt == "Invalid Date"){
        console.log(3)
        $(".start_h").text(max_date_message)
        $(".start_h").removeClass("hidden")
    } else {
       $(".start_h").addClass("hidden")  
    }
});

$("#ends_at").change(function() {
    endsAt = $('#ends_at').val()
    endsAt = new Date(ends_at);

    if(endsAt < minDate){
        $(".end_h").text(minDateMessage)
        $(".end_h").removeClass("hidden")
    } else if(endsAt == "Invalid Date"){
        $(".end_h").text(max_date_message)
        $(".end_h").removeClass("hidden")
    } else{
       $(".end_h").addClass("hidden")  
    }
});

$('#starts_at').prop('min', minDate);
$('#ends_at').prop('min', minDate);