const express = require('express');
const path = require('path');

const app = express();
const port = 3000; // Change this to the desired port number

// Middleware to parse incoming JSON payloads
app.use(express.json());

// Serve static files (CSS, images, etc.) from the "public" directory
app.use(express.static(path.join(__dirname, 'public'), {
  index: false
}));

// Serve login
app.get('/login', (req, res) => {
  // console.log('Redirecting to /login')
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

// Serve success
app.get('/success', (req, res) => {
  // console.log('Redirecting to /login')
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/', (req, res) => {
  console.log('Redirecting to /login');
  res.redirect('/login');
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}/`);
});











