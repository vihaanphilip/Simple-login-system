const express = require('express');
const path = require('path');

const app = express();
const port = 3000; // Change this to the desired port number

// Serve static files (CSS, images, etc.) from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Serve index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Serve app.js
app.get('/app.js', (req, res) => {
  res.sendFile(path.join(__dirname, 'app.js'));
});

// Serve other HTML pages from the "other-pages" directory
app.get('/about', (req, res) => {
  res.sendFile(path.join(__dirname, 'other-pages', 'about.html'));
});

// Handle the redirect to the about page
app.get('/redirect', (req, res) => {
  res.redirect('/about');
});

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}/`);
});