
var mysql = require('mysql');

var con = mysql.createConnection({
  host: "127.0.0.1",
  user: "root",
  password: "test",
  database: "DroneOp"
});

//
// con.connect(function(err) {
//   if (err) throw err;
//   console.log("Connected!");
// });

con.connect(function(err) {
  if (err) throw err;
  con.query("SELECT * FROM DroneOp.crew", function (err, result, fields) {
    if (err) throw err;
    var json = JSON.parse(JSON.stringify(result));
    json.forEach(function(obj) {
      console.log(obj.pilot);
      console.log(obj.pic_title);
      console.log(obj.faa_uas_cert_num);
      console.log(obj.issue_on);
      console.log(obj.valid_until);
      console.log(obj.ama_num);
      console.log("");
    });
  });
  console.log("---------");
  con.query("SELECT * FROM DroneOp.equipment", function (err, result, fields) {
    if (err) throw err;
    var json = JSON.parse(JSON.stringify(result));
    json.forEach(function(obj) {
      console.log(obj.aircraft_mod);
      console.log(obj.drones);
      console.log("");
    });
  });
  console.log("---------");
  con.query("SELECT * FROM DroneOp.equip_details", function (err, result, fields) {
    if (err) throw err;
    var json = JSON.parse(JSON.stringify(result));
    json.forEach(function(obj) {
      console.log(obj.drone);
      console.log(obj.faa_reg);
      console.log(obj.issued_on);
      console.log(obj.valid_until);
      console.log(obj.serial_num);
      console.log("");
    });
  });
});
