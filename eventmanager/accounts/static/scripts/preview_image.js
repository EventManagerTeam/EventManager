function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#preview').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#id_cover_image").change(function() {
    readURL(this);
    $('#cover_button').text("Change cover photo");
});

$("#id_profile_picture").change(function() {
    readURL(this);
    $('#cover_button').text("Change profile photo");
});

$("#id_category_picture").change(function() {
    readURL(this);
    $('#cover_button').text("Change category photo");
});

var now = new Date(),
    minDate = now.toISOString().substring(0,10);

$('#starts_at').prop('min', minDate);
$('#ends_at').prop('min', minDate);

$("#starts_at").change(function() {
    starts_at = $('#starts_at').val()
    if(starts_at < minDate){
        $(".start_h").text("Please use a date in the future")
        $(".start_h").removeClass("hidden")
    } else{
       $(".start_h").addClass("hidden")  
    }
});

$("#ends_at").change(function() {
    ends_at = $('#ends_at').val()
    if(ends_at < minDate){
        $(".end_h").text("Please use a date in the future")
        $(".end_h").removeClass("hidden")
    } else{
       $(".end_h").addClass("hidden")  
    }
});
