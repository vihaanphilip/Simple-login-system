const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 3000; // Change this to the desired port number

http.createServer((req, res) => {
  if (req.url === '/') {
    // Serve index.html
    const filePath = path.join(__dirname, 'index.html');
    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500);
        res.end('Error loading index.html');
      } else {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(content);
      }
    });
  } else if (req.url === '/app.js') {
    // Serve app.js
    const filePath = path.join(__dirname, 'app.js');
    fs.readFile(filePath, (err, content) => {
      if (err) {
        res.writeHead(500);
        res.end('Error loading app.js');
      } else {
        res.writeHead(200, { 'Content-Type': 'application/javascript' });
        res.end(content);
      }
    });
  } else {
    // Handle other requests (if needed)
    res.writeHead(404);
    res.end('Page not found');
  }
}).listen(port, () => {
  console.log(`Server running http://localhost:${port}/`);
});