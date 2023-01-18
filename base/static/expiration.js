var expired = document.getElementsByClassName("expired")
var expiring = document.getElementsByClassName("warning");
var expired_count = document.getElementById("count1");
var expiring_count = document.getElementById("count2");

expired_count.innerHTML = expired.length;
expiring_count.innerHTML = expiring.length;