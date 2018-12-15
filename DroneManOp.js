// var weatherAPIkey= "205d5b7250932424c8062f648affe291";
// // const weather = require('openweathermap-js');
//
// // weather.defaults({
// //     appid: weatherAPIkey,
// //     location: 'London',
// //     cityID: 1851632,	// Shuzenji, JP
// //     method: 'name',
// //     format: 'JSON',
// //     accuracy: 'accurate',
// //     units: 'imperial'
// // });
//
//
//
// // weather.daily({method: 'coord', coord: {lat: -33.9, lon: 151.2, cnt: 3}}, function(err, data) {
// //     if (!err)
// //         console.log(data);
// //     else
// //         console.error(err.message);
// // });
// //
// // console.log(weather);
//
var mysql = require('mysql');
// //
// var con = mysql.createConnection({
//   host: "127.0.0.1",
//   user: "root",
//   password: "test",
//   database: "DroneOp"
// });

// con.connect(function(err) {
//   if (err) throw err;
//   //CONNECT TO CREW
//   con.query("SELECT * FROM DroneOp.crew", function (err, result, fields) {
//     if (err) throw err;
//     var json = JSON.parse(JSON.stringify(result));
//     json.forEach(function(obj) {
//       console.log(obj.pilot);
//       console.log(obj.pic_title);
//       console.log(obj.faa_uas_cert_num);
//       console.log(obj.issue_on);
//       console.log(obj.valid_until);
//       console.log(obj.ama_num);
//       console.log("");
//     });
//   });
//   console.log("---------");
//   // //CONNECT TO EQUIPMENT
//   // con.query("SELECT * FROM DroneOp.equipment", function (err, result, fields) {
//   //   if (err) throw err;
//   //   var json = JSON.parse(JSON.stringify(result));
//   //   json.forEach(function(obj) {
//   //     console.log(obj.aircraft_mod);
//   //     console.log(obj.drones);
//   //     console.log("");
//   //   });
//   // });
//   //
//   // console.log("---------");
//   // //CONNECT TO EQUIPMENT DETAILS
//   // con.query("SELECT * FROM DroneOp.equip_details", function (err, result, fields) {
//   //   if (err) throw err;
//   //   var json = JSON.parse(JSON.stringify(result));
//   //   json.forEach(function(obj) {
//   //     console.log(obj.drone);
//   //     console.log(obj.faa_reg);
//   //     console.log(obj.issued_on);
//   //     console.log(obj.valid_until);
//   //     console.log(obj.serial_num);
//   //     console.log("");
//   //   });
//   // });
// });
//
function start(){


}


function test(){
  console.log("test");
  document.getElementById("faa_uas_cert_num").value = "test";
}
