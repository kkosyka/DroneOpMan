// http://127.0.0.1:8081

var express = require('express');

var app = express();

app.use(express.static(__dirname + '/index.html'));

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://%s:%s", host, port)
})

var mysql = require('mysql');
//
//
// var express = require('express');
// var app = express();
// var path = require('path');
//
// // viewed at http://localhost:8080
// app.get('/', function(req, res) {
//     res.sendFile(path.join(__dirname + '/index.html'));
// });
//
// app.listen(8080);
