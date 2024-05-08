// Retrieve the remember checkbox and password field
    var rememberCheckbox = document.getElementById("login-check");
    var passwordField = document.getElementById("password-field");

    // Check if there is a stored value for remember me
    var rememberMe = localStorage.getItem("rememberMe");
    var storedPassword = localStorage.getItem("storedPassword");

    // If rememberMe is true in localStorage and a password is stored, check the checkbox and fill the password field
    if (rememberMe === "true" && storedPassword) {
        rememberCheckbox.checked = true;
        passwordField.value = storedPassword;
    }

    // Add event listener to the checkbox
    rememberCheckbox.addEventListener('change', function() {
        // If the checkbox is checked, store the password in localStorage
        if (this.checked) {
            localStorage.setItem("rememberMe", "true");
            localStorage.setItem("storedPassword", passwordField.value);
        } else {
            // If the checkbox is unchecked, remove the stored password from localStorage
            localStorage.removeItem("rememberMe");
            localStorage.removeItem("storedPassword");
        }
    });