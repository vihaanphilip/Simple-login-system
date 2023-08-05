# Welcome to my Simple Login Page!

## This is a simple login system that utilizes the following libraries:

- SQLite is used as the database to store user data.
- FastAPI handles all the logic for the backend server.
- Express.js hosts the frontend server.
- Plain JavaScript is used to implement all frontend logic.
- JWTs (JSON Web Tokens) are utilized as secure tokens to authenticate user logins.

# Setup

Make sure you have the following installed:

- Python 3.11.4 (https://www.python.org/downloads/)
- Node.js 18.17.0 LTS (https://nodejs.org/en)

## Setting up the Backend

1. Open a terminal.
2. Make sure the folder is in the `simple-login-system` directory.
3. Go to the backend folder by typing `cd backend`.
4. Install dependencies by typing `pip3 install -r requirements.txt`.
5. Run the backend server by typing `uvicorn main:app --reload`.
6. The backend server should now be running on port 8000 (http://localhost:8000/).

## Setting up the Frontend

1. Open another terminal (Do not close the backend terminal).
2. Make sure the folder is in the `simple-login-system` directory.
3. Go to the frontend folder by typing `cd frontend`.
4. Install dependencies by typing `npm install`.
5. Run the frontend server by typing `npm start`.
6. The frontend server should now be running on port 3000 (http://localhost:3000/).

# How It Works

**Login:**

If the user's credentials are already located in the database, enter the correct username and password to log on. If the credentials are not valid, a simple error will be displayed.

**Sign Up:**

Users can navigate to the sign-up page via the "Register" button on the login page. Enter a username and password for a new account. If the input is valid, it will be stored in the database. Both the username and password must be more than one character; otherwise, an error will be displayed during the sign-up attempt. If the username already exists in the database, an error will be displayed indicating that the username already exists.

**Tokens:**

Tokens (JWT) are used in this system to authenticate a user's login. Each token lasts for 1 minute. This is done so that users do not have to log in every time they refresh the page.

**Login Tracking**

Additionally, this app tracks and logs each user's login activities. Every time a user logs in, the system records the login event and stores it in a separate database called logins.db. The logins.db database keeps a history of all successful login attempts, along with the associated user information and timestamps. This feature provides valuable insights into user activity and login patterns.