var textarea = document.querySelector("textarea");
var maxlength = 500;

textarea.addEventListener("input", function(){
    var currentLength = this.value.length;

    if( currentLength >= maxlength ){
        document.getElementById("remainingCount1").innerHTML = "You have reached the maximum number of characters.";
    } else{
        document.getElementById("remainingCount1").innerHTML = maxlength - currentLength + " chars left";
    }
});

$(document).ready(function(){
	var currentLength = document.getElementById('id_content').value.length;
	document.getElementById("remainingCount1").innerHTML = maxlength - currentLength + " chars left";
})
