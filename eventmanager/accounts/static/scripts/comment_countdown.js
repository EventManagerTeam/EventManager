var textarea = document.querySelector("textarea");

textarea.addEventListener("input", function(){
    var maxlength = 500;
    var currentLength = this.value.length;

    if( currentLength >= maxlength ){
        document.getElementById("remainingCount1").innerHTML = "You have reached the maximum number of characters.";
    } else{
        document.getElementById("remainingCount1").innerHTML = maxlength - currentLength + " chars left";
    }

});