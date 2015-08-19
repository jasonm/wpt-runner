require("dotenv").load();
var _ = require("lodash");
var uuidv4 = require("node-uuid").v4;

var pgp = require('pg-promise')(process.env.DATABASE_URL);

var pgclient = await pgp.connect();

await pgclient.query("select * from runs");
console.log();


var WebPageTest = require("webpagetest");
var wpt = new WebPageTest("www.webpagetest.org");

var commonOptions = {
  // Runner options
  key: process.env.WEBPAGETEST_API_KEY,
  // pollResultsIntervalSeconds: 5,
  // timeoutSeconds: 60,

  // Shared test options
  "video": true
};

var testConfigs = [
  {
    "label": "Dulles_MotoG 3G",
    "url": "https://www.minerva.kgi.edu",
    "options": {
      "location": "Dulles_MotoG",
      "bwDown": 1500, "bwUp": 384, "latency": 50, "plr": 0,
    }
  }
];

function pollForResults(uuid, runLabel, data) {
  console.log("Not really polling for results on ", arguments);
}

// Expects obj.uuid to be a UUID
function recordRun(obj, cb) {
  // wptrunner_development=# insert into runs (data) values ('{"a":1}');
  pgclient.query('INSERT INTO runs (uuid, data) VALUES ($1, $2)', [obj.uuid, obj], function(err, result) {
    cb(err, result);
  });
}


_.each(testConfigs, function(testConfig) {
  var runLabel = testConfig.label + " " + new Date().toISOString();
  var options = {};
  var uuid = uuidv4();
  _.extend(options, commonOptions);
  _.extend(options, testConfig["options"]);
  _.extend(options, {
    "label": runLabel
  });

  wpt.runTest(
      testConfig.url,
      options,
      function(err, data) {
        console.log(err || data);
        if (err) {
          recordRun({
            "uuid": uuid,
            "runLabel": runLabel,
            "status": "error",
            "error": err
          }, function(err, result) {
            // shitshow time
          });
        } else {
          recordRun({
            "uuid": uuid,
            "runLabel": runLabel,
            "status": data.statusText,
            "data": data
          });

          pollForResults(uuid, runLabel, data);
        }
      });
});

/*
{ statusCode: 200,
  statusText: 'Ok',
  data:
   { testId: '150813_YW_8DF',
     ownerKey: '8ba9778b2c3581cb77bc3a57428ae2af5ed80982',
     jsonUrl: 'http://www.webpagetest.org/jsonResult.php?test=150813_YW_8DF',
     xmlUrl: 'http://www.webpagetest.org/xmlResult/150813_YW_8DF/',
     userUrl: 'http://www.webpagetest.org/result/150813_YW_8DF/',
     summaryCSV: 'http://www.webpagetest.org/result/150813_YW_8DF/page_data.csv',
     detailCSV: 'http://www.webpagetest.org/result/150813_YW_8DF/requests.csv' } }

 */

// [master][~/dev/wpt-runner] node index.js
// { statusCode: 200,
//   statusText: 'Ok',
//   data:
//    { testId: '150819_SB_8ZR',
//      ownerKey: '7682eb761589bbf5adb9adaa31781e02239d7039',
//      jsonUrl: 'http://www.webpagetest.org/jsonResult.php?test=150819_SB_8ZR',
//      xmlUrl: 'http://www.webpagetest.org/xmlResult/150819_SB_8ZR/',
//      userUrl: 'http://www.webpagetest.org/result/150819_SB_8ZR/',
//      summaryCSV: 'http://www.webpagetest.org/result/150819_SB_8ZR/page_data.csv',
//      detailCSV: 'http://www.webpagetest.org/result/150819_SB_8ZR/requests.csv' } }
