
    function myMenuFunction() {
        var i = document.getElementById("navMenu");
        if (i.className === "nav-menu") {
            i.className += " responsive";
        } else {
            i.className = "nav-menu";
        }
    }

    function login() {
        var loginForm = document.getElementById("login");
        var registerForm = document.getElementById("register");
        var forgotForm = document.getElementById("forgot");

        loginForm.style.left = "4px";
        registerForm.style.right = "-520px";
        forgotForm.style.left = "-520px";

        document.getElementById("loginBtn").className += " white-btn";
        document.getElementById("registerBtn").className = "btn";

        loginForm.style.opacity = 1;
        registerForm.style.opacity = 0;
        forgotForm.style.opacity = 0;
    }

    function register() {
        var loginForm = document.getElementById("login");
        var registerForm = document.getElementById("register");
        var forgotForm = document.getElementById("forgot");

        loginForm.style.left = "-510px";
        registerForm.style.right = "5px";
        forgotForm.style.left = "-520px";

        document.getElementById("loginBtn").className = "btn";
        document.getElementById("registerBtn").className += " white-btn";

        loginForm.style.opacity = 0;
        registerForm.style.opacity = 1;
        forgotForm.style.opacity = 0;
    }

    function showForgotForm(event) {
        event.preventDefault();
        var loginForm = document.getElementById("login");
        var registerForm = document.getElementById("register");
        var forgotForm = document.getElementById("forgot");

        loginForm.style.left = "-520px";
        registerForm.style.right = "-520px";
        forgotForm.style.left = "4px";

        loginForm.style.opacity = 0;
        registerForm.style.opacity = 0;
        forgotForm.style.opacity = 1;
    }

    function hideForgotForm(event) {
        event.preventDefault();
        var forgotForm = document.getElementById("forgot");
        forgotForm.style.left = "-520px";
        forgotForm.style.opacity = 0;
    }
