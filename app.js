const express = require('express');
var mongoose = require('mongoose');
const app = express();


// Create connection for mongoose and specific Mongo database
mongoose.connect('mongodb://localhost:27017/macy_scrape', {
  useMongoClient: true,
});

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));


// Define schema of database
var Schema = mongoose.Schema;

var itemSchema = new Schema({
  name: String,
  original_price: {
    min: {type: Number, min: 0},
    max: {type: Number, min: 0}
  },
  sale_price: {
    min: {type: Number, min: 0},
    max: {type: Number, min: 0}
  }
});

// Create mongoose model based on schema
var Item = mongoose.model('Item', itemSchema, 'items');


// Define routes
app.get('/', function (req, res) {
  res.send('Go to localhost:3000/home to see HTTP response output.');
})

app.get('/home', function(req, res) {
  // Query all documents from collection and send JSON response
  Item.find(function (err, items){
    if (err) {
      res.status(500).send(err);
    } else {
      console.log(items.length + ' items found.');
      item_json = {"items": items};
      res.json(item_json);
    }
  });
})

app.listen(3000, function () {
  console.log('App listening on port 3000');
})
