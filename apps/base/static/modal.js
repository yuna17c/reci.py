const openEls = document.querySelectorAll("[data-open]");
const closeEls = document.querySelectorAll("[data-close]");
const isVisible = "is-visible";
const popupContent = document.querySelector(".popup-content");
var overlay = document.getElementById("overlay");
var window = document.getElementById("window");

for(const el of openEls) {
  el.addEventListener("click", function() {
    const popupinfo = el.parentNode.childNodes[5];
    popupContent.querySelector(".popup-title").textContent = popupinfo.children[0].textContent
    var ingredient = popupinfo.children[1].textContent
    var ing_list = ingredient.split(", ")
    ing_list.splice(-1)
    var ul = document.getElementById("ul-ing");
    ul.innerHTML = "";
    for (i of ing_list) {
      var li = document.createElement("li");
      li.appendChild(document.createTextNode(i));
      ul.appendChild(li);
    }
    popupContent.querySelector(".popup-prep").textContent = popupinfo.children[2].textContent
    popupContent.querySelector(".popup-img").src = popupinfo.children[3].textContent
    popupContent.querySelector(".popup-link").href = popupinfo.children[4].textContent
    const modal1 = this.dataset.open;
    document.getElementById(modal1).classList.add(isVisible);
  });
}

for (const el of closeEls) {
  el.addEventListener("click", function() {
    console.log("yes")
    this.parentElement.parentElement.parentElement.classList.remove(isVisible);
  });
}
