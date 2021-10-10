require('dotenv').config()
const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const https = require("https");
const cors = require("cors");
const gfs = require("./firestore.js")

var corsOptions = {
  origin: "*"
};

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

app.set('view engine', 'ejs');
app.use(express.static("public"))

app.get("/", (req, res) => {
    res.render("signup", {});
})

app.post("/", (req, res) => {
    const dataShortcut = req.body;
    const fname = dataShortcut.fname;
    const lname = dataShortcut.lname;
    const phone_num = dataShortcut.phone_num;
    myNumber = Math.floor(Math.random() * 90000) + 10000
    //const p = new Friend({name: name, email: email, bday: bday, tag: 's'});
    //p.save();
    gfs.add_user(phone_num, fname, lname, myNumber.toString())
    //console.log(myNumber)
    res.render("success", {myNumber: myNumber.toString()})
});

app.get("/data", (req, res) => {
})

app.post("/failure", (req,res) => {
    res.redirect("/");
});

app.post("/activate", async (req,res) => {
    const phone_num = req.body.phone_num;
    result = await gfs.activate_user(phone_num, req.body.code)
    res.send({aresult: result})
});

app.post("/get_user", async (req,res) => {
    const phone_num = req.body.phone_num;
    user = await gfs.get_user(phone_num)
    res.send({user: user})
});

const port = process.env.PORT || 3000;

app.listen(port, () => {
    console.log("Server is running on port " + port);
});
