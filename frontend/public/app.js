const baseUrl = "http://localhost:8000/";

document.addEventListener("DOMContentLoaded", function () {

    function isLoginPage() {
        return window.location.pathname === '/login';
    }

    function isSuccessPage() {
        return window.location.pathname === '/success';
    }

    // console.log(isLoginPage());
    // console.log(isSuccessPage());


    if (isLoginPage()) {
        this.getElementById('login_button').addEventListener('click', function() {
            const inputUsername = document.getElementById('input_username').value;
            const inputPassword = document.getElementById('input_password').value;

            console.log(inputUsername);
            console.log(inputPassword);

            fetch(baseUrl + 'login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: inputUsername,
                    password: inputPassword
                })
            })
            .then(response => response.json())
            .then(data => {
                // console.log(data.access_token);
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('username', data.username);

                // console.log(localStorage.getItem('access_token'));
                // console.log(localStorage.getItem('username'));

            })  
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});

