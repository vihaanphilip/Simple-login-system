const baseUrl = "http://localhost:8000/";

function isLoginPage() {
  return window.location.pathname === '/login';
}

function isSignUpPage() {
  return window.location.pathname === '/signup';
}

function isSuccessPage() {
  return window.location.pathname === '/success';
}

function isMainPage() {
  return window.location.pathname === '/';
}

function redirectToLogin() {
  console.log('Token is not valid. Redirecting to login...');
  window.location.href = '/login'; // Redirect to the login page
}

document.addEventListener("DOMContentLoaded", function() {
  // Call the function to check the token and display the username on the success page

  if(isSignUpPage()){

    if (localStorage.getItem('access_token')) {
      checkAuthenticated();
    }

    document.getElementById('back_button').addEventListener('click', function() {
      window.location.href = '/login';
    });

    document.getElementById('signup_button').addEventListener('click', function() {
      // attempts to post to server
      const inputUsername = document.getElementById('input_username').value;
      const inputPassword = document.getElementById('input_password').value;

      fetch(baseUrl + 'users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: inputUsername,
          password: inputPassword
        })
      })
      .then(response => {

        if (!response.ok) {
          return response.json().then(errorData => {
            throw new Error(errorData.detail);
          });
        }
        return response.json()
      })
      .then(async data => {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('username', data.username);

        // Call the function to check the token and redirect accordingly
        await checkNotAuthenticated();
      })  
      .catch(error => {
        console.error('Error:', error);
        var errorMessage = document.getElementById("error-message");
        errorMessage.textContent = error.message; // Set the error message to the error detail received from the backend
        errorMessage.style.display = "block";
      });

    });
  }
  
  if (isSuccessPage()) {
    checkAuthTokenAndDisplayUsername();

    document.getElementById('logout_button').addEventListener('click', function() {
      localStorage.removeItem('access_token');
      localStorage.removeItem('username');
      window.location.href = '/login';
    });
  }

  if (isLoginPage()) {

    if (localStorage.getItem('access_token')) {
      checkAuthenticated();
    }

    

    document.getElementById('login_button').addEventListener('click', function() {
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
      .then(response => {

        if (!response.ok) {
          throw new Error('Login failed.');
        }
        return response.json()
      })
      .then(async data => {
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('username', data.username);

        // Call the function to check the token and redirect accordingly
        await checkNotAuthenticated();
      })  
      .catch(error => {
        console.error('Error:', error);
        var errorMessage = document.getElementById("error-message");
        errorMessage.style.display = "block";
      });

    });

    document.getElementById('register_button').addEventListener('click', function() {
      window.location.href = '/signup';
    });

  }
});

function authToken() {
  const access_token = localStorage.getItem('access_token');
  return fetch(baseUrl + 'verify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      access_token: access_token
    })
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.message);
    return data.message === 'Valid';
  })
  .catch(error => {
    console.error(error);
    return false;
  });
}

async function checkAuthTokenAndDisplayUsername() {
  try {
    const isValid = await authToken();
    console.log(isValid); // true or false depending on token validity

    if (!isValid) {
      // Token is not valid, redirect to login
      redirectToLogin();
      return;
    }

    // If the token is valid, continue with success page operations
    const username = localStorage.getItem('username');
    document.getElementById('username').innerHTML = username;
  } catch (error) {
    console.error(error);
    // If there's an error, redirect to login
    redirectToLogin();
  }
}

  async function checkAuthenticated() {
    try {
      const isValid = await authToken();
      console.log(isValid); // true or false depending on token validity
  
      if (!isValid) {
        // Token is not valid, redirect to login
        return;
      }
  
      // If the token is valid, redirect to the success page
      window.location.href = '/success';
    } catch (error) {
      console.error(error);
      // If there's an error, redirect to login
      redirectToLogin();
    }
  }

async function checkNotAuthenticated() {
  try {
    const isValid = await authToken();
    console.log(isValid); // true or false depending on token validity

    if (!isValid) {
      // Token is not valid, redirect to login
      redirectToLogin();
      return;
    }

    // If the token is valid, redirect to the success page
    window.location.href = '/success';
  } catch (error) {
    console.error(error);
    // If there's an error, redirect to login
    redirectToLogin();
  }
}