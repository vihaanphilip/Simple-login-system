const baseUrl = "http://localhost:8000/";

document.addEventListener("DOMContentLoaded", function () {

    const loginButton = this.getElementById('login_button');
    loginButton.addEventListener('click', function() {
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
            console.log(data);
        })  
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

// function handleLoginResponse(userDetails)