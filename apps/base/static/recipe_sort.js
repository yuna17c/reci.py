var desc = document.getElementById("desc");
var asc = document.getElementById("asc");

desc.onclick = function() {
    console.log("n")
    asc.style.display = "block";
    desc.style.display = "none";
}

asc.onclick = function() {
    console.log("y")
    desc.style.display = "block";
    asc.style.display = "none";
}
