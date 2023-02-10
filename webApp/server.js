const express = require('express');
const app = express();

PORT = 8080;

app.use(express.static('public'));

app.listen(PORT, function() {
    console.log('Server is listening on Port: ', PORT);
});
