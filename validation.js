/*password validation script*/
var password = document.getElementById("pw");
var confirmPassword = document.getElementById("cpw");
function validatePassword() {
    var passwordValue = password.value;
    var characterRegex = /[a-zA-Z]/; // At least one character
    var numberRegex = /\d/; // At least one number
    var specialCharRegex = /[!@#$%^&*(),.?":{}|<>]/; // At least one special character
    var maxLength = 12; // Maximum length
    var minLength = 12;
    if (!characterRegex.test(passwordValue) || !numberRegex.test(passwordValue) || !specialCharRegex.test(passwordValue) || passwordValue.length > maxLength || passwordValue.length > minLength) {
        password.setCustomValidity("one special character,one number,one character requied maximum length(12) and minimum length(5)");
    } else {
        password.setCustomValidity('');
    }
}

function cpass() {
    if (password.value !== confirmPassword.value) {
        confirmPassword.setCustomValidity("Confirm password doesn't match");
    } else {
        confirmPassword.setCustomValidity('');
    }
}

// Add event listener for Tab key press on confirmPassword field
confirmPassword.addEventListener('keydown', function (event) {
    if (event.key === 'Tab' && this.value.trim() === '') {
        event.preventDefault();
    }
});

password.addEventListener('keydown', function (event) {
    if (event.key === 'Tab' && this.value.trim() === '') {
        event.preventDefault();
    }
});

password.oninput = validatePassword;
confirmPassword.oninput = cpass;


            /*first name and last name validation script*/

            document.addEventListener('DOMContentLoaded', function () 
            {
            function validateInput(inputElement, errorMessage,maxLength) 
            {
            inputElement.addEventListener('input', function () 
            {
            if (!/^[a-zA-Z]*$/.test(this.value) || this.value.length > maxLength || this.value.length === 21) 
            {
                this.setCustomValidity(errorMessage);
            } else 
            {
                this.setCustomValidity('');
            }
            this.reportValidity();
            });
            // Prevent entering numbers
            inputElement.addEventListener('keypress', function (event) 
            {
            if (/\d/.test(event.key)) 
            {
                event.preventDefault();
            }
            });

            // Prevent entering special characters
            inputElement.addEventListener('input', function () 
            {
            if (/[^a-zA-Z0-9]/.test(this.value)) 
            {
            this.value = this.value.replace(/[^a-zA-Z0-9]/g, '');
            }
            });
            // Prevent jumping to the next field on Tab press if the field is empty
            inputElement.addEventListener('keydown', function (event) {
             if (event.key === 'Tab' && this.value.trim() === '') {
                event.preventDefault();
            }
            });
            }

    var fnameInput = document.getElementById('fname');
    var lnameInput = document.getElementById('lname');
    validateInput(fnameInput, "Please enter a valid first name (e.g., Sardar). Maximum 20 characters allowed.",20);
    validateInput(lnameInput, "Please enter a valid last name (e.g., Patel). Maximum 20 characters allowed.",20);
});

            /*email id validation script*/
            document.addEventListener('DOMContentLoaded', function () {
    function validateEmail(emailElement, errorMessage) {
        emailElement.addEventListener('input', function () {
            var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$/;

            // Get the value of the email input field
            var email = this.value;

            if (emailRegex.test(email)) {
                console.log("Email is valid");
            } else {
                console.log("Email is not valid");
            }

            if (!emailRegex.test(email) || email.length > 50) {
                this.setCustomValidity(errorMessage);
            } else {
                this.setCustomValidity('');
            }

            this.reportValidity();
        });

        // Prevent jumping to the next field on Tab press if the field is empty
        emailElement.addEventListener('keydown', function (event) {
            if (event.key === 'Tab' && this.value.trim() === '') {
                event.preventDefault();
            }
        });
    }

    // Use querySelectorAll to select multiple elements by their IDs
    var emailInputs = document.querySelectorAll('#e-id, #l_e-id');

    // Iterate over each selected element and apply the validation logic
    emailInputs.forEach(function (emailInput) {
        validateEmail(emailInput, "Please enter a valid email address (e.g., fkprice@mail.com). Maximum 50 characters allowed.");
    });
});

        
        /*mobile number validation script
document.addEventListener('DOMContentLoaded', function () {
    var mobileInput = document.getElementById('mob');

    mobileInput.addEventListener('input', function () {
        // Regular expression for a 10-digit number
        var mobileRegex = /^[0-9]{10}$/;
       

        if (!mobileRegex.test(this.value)) {
            this.setCustomValidity("Please enter a valid 10-digit mobile number");
        } else {
            this.setCustomValidity('');
        }
        this.reportValidity();
    });

    mobileInput.addEventListener('keypress', function (event) {
        var keyCode = event.keyCode || event.which;
        var key = String.fromCharCode(keyCode);

        // Allow only numbers during keypress event
        if (!/^\d+$/.test(key)) {
            event.preventDefault();
        }
    });

    // Prevent jumping to the next field on Tab press if the field is empty
    mobileInput.addEventListener('keydown', function (event) {
        if (event.key === 'Tab' && this.value.trim() === '') {
            event.preventDefault();
        }
    });
});*/

/*mobile number validation script*/
document.addEventListener('DOMContentLoaded', function () {
    var mobileInput = document.getElementById('mob');

    mobileInput.addEventListener('input', function () {
        // Regular expression for exactly 10 digits
        var mobileRegex = /^\d{10}$/;

        if (!mobileRegex.test(this.value)) {
            this.setCustomValidity("Please enter a valid 10-digit mobile number");
        } else {
            this.setCustomValidity('');
        }
        this.reportValidity();
    });

    mobileInput.addEventListener('keypress', function (event) {
        // Prevent any input after reaching 10 digits
        if (this.value.length >= 10) {
            event.preventDefault();
        } else {
            var keyCode = event.keyCode || event.which;
            var key = String.fromCharCode(keyCode);

            // Allow only numbers during keypress event
            if (!/^\d+$/.test(key)) {
                event.preventDefault();
            }
        }
    });
});


document.getElementById("registration-form").onsubmit = function() {
    var checkBox = document.getElementById("register-check");
    if (!checkBox.checked) {
        alert("Please check the terms and conditions box.");
        return false;
    }
    return true;
};

//show password using toggle button(eye)
function togglePassword() {
    var passwordField = document.getElementById('password-field');
    var eyeIcon = document.querySelector('.toggle-password i');

    if (passwordField && eyeIcon) {
        if (passwordField.type === "password") {
            passwordField.type = "text";
            eyeIcon.classList.remove('bx-hide');
            eyeIcon.classList.add('bx-show');
        } else {
            passwordField.type = "password";
            eyeIcon.classList.remove('bx-show');
            eyeIcon.classList.add('bx-hide');
        }
    }
}

function togglePasswordRegister() {
    var passwordField = document.getElementById('pw');
    var confirmPasswordField = document.getElementById('cpw');
    var eyeIcon = document.querySelector('.rtoggle-password i');

    if (passwordField && confirmPasswordField && eyeIcon) {
        if (passwordField.type === "password") {
            passwordField.type = "text";
            confirmPasswordField.type = "text";
            eyeIcon.classList.remove('bx-hide');
            eyeIcon.classList.add('bx-show');
        } else {
            passwordField.type = "password";
            confirmPasswordField.type = "password";
            eyeIcon.classList.remove('bx-show');
            eyeIcon.classList.add('bx-hide');
        }
    }
}

