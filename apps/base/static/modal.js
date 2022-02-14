const openEls = document.querySelectorAll("[data-open]");
const closeEls = document.querySelectorAll("[data-close]");
const isVisible = "is-visible";
const popupContent = document.querySelector(".popup-content");

for(const el of openEls) {
  el.addEventListener("click", function() {
    const popupinfo = el.parentNode.childNodes[5];
    popupContent.querySelector(".popup-title").textContent = popupinfo.children[0].textContent
    popupContent.querySelector(".popup-ing").textContent = popupinfo.children[1].textContent
    popupContent.querySelector(".popup-img").src = popupinfo.children[2].textContent
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

// document.addEventListener("click", e => {
//   if (e.target == document.querySelector(".modal.is-visible")) {
//     document.querySelector(".modal.is-visible").classList.remove(isVisible);
//   }
// });

/*
popupbtns.forEach(btn => btn.addEventListener('click', () => {
const popupinfo = btn.parentNode.childNodes[1];
    popupContent.querySelector(".popup-title").src = popupinfo.children[0].textContent //project image
    console.log("click")
   wrapper.style.display = "block";
   const modal1 = this.dataset.open;
   document.getElementById(modal1).classList.add(isVisible);
}));
*/