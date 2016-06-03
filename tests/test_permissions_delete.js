
var event = {
  "region": "us-east-1",
  "permissions": [
    {
      "user_id": "49d8bc68-f57e-11e3-ba1d-005056ba0d15",
      "role": "",
      "resource": "account",
      "value": "089476987273",
      "action": "read",
      "condition": ""
    },
    {
      "user_id": "49d8bc68-f57e-11e3-ba1d-005056ba0d15",
      "role": "",
      "resource": "account",
      "value": "089476987273",
      "action": "create",
      "condition": ""
    }
  ]
};
var i = require('../permissions_delete.js');
var context = {fail:function(a){console.log(a)}, done:function(e, a){console.log(a)}};
i.handler(event, context);
