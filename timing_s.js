function myMenuFunction() {
    var i = document.getElementById("navMenu");

    if(i.className === "nav-menu") {
        i.className += " responsive";
    } else {
        i.className = "nav-menu";
    }
   }

window.addEventListener('load', function(){
    var loader = document.getElementById('loader');
  
    
    setTimeout(function() {
        loader.style.display = 'none'; // Hide the loader
      
    }, 900); // Delay for 10 seconds (10000 milliseconds)
});

// Function to hide error message after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    var errorMessage = document.getElementById("error-message");
    if (errorMessage) {
        setTimeout(function() {
            errorMessage.style.display = "none";
        }, 5000); // 5 seconds
    }

    var errorMessageRegister = document.getElementById("error-message-register");
    if (errorMessageRegister) {
        setTimeout(function() {
            errorMessageRegister.style.display = "none";
        }, 5000); // 5 seconds
    }

    var errorMessageforgot = document.getElementById("error-message-forgot");
    if (errorMessageforgot) {
        setTimeout(function() {
            errorMessageforgot.style.display = "none";
        }, 5000); // 5 seconds
    }

    var valid_message = document.getElementById("valid_message");
    if (valid_message) {
        setTimeout(function() {
            valid_message.style.display = "none";
        }, 5000); // 5 seconds
    }
});
