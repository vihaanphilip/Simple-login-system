const inputUsername = document.getElementById('input_username');
const inputPassword = document.getElementById('input_password');

function attempt_login() {
    console.log('Attempting login...');
    console.log('Username: ' + inputUsername.value);
    console.log('Password: ' + inputPassword.value);
    fetch('http://localhost:8000/users')
        .then(response => response.json())
        .then(data => console.log(data));
}
