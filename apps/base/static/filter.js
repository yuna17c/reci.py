function check() {
    let food_groups = ["fruits", "vegetables", "grains", "protein", "dairy", "cooking product", "herbs/spices", "other"];
    let curr_filters = [];

    food_groups.forEach(function(food_group) {
        if (document.getElementById(food_group).checked) {
            curr_filters.push(food_group);
        }
    })

    if (curr_filters.length == 0) {
        filter([""]);
    } else {
        filter(curr_filters);
    }
};

function filter(categories) {
    var i;
    var all_elements = document.getElementsByClassName("food_item");
    if (categories.length == 0) {
        categories.push("");
    }
    // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
    for (i = 0; i < all_elements.length; i++) {
        let match = false;
        w3RemoveClass(all_elements[i], "show");
        for (var c in categories) {
            if (all_elements[i].className.indexOf(categories[c]) > -1) match = true;
        }
        if (match) {
            w3AddClass(all_elements[i], "show");
        }
    }
}
  
  // Show filtered elements
  function w3AddClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
      if (arr1.indexOf(arr2[i]) == -1) {
        element.className += " " + arr2[i];
      }
    }
  }
  
  // Hide elements that are not selected
  function w3RemoveClass(element, name) {
    var i, arr1, arr2;
    arr1 = element.className.split(" ");
    arr2 = name.split(" ");
    for (i = 0; i < arr2.length; i++) {
      while (arr1.indexOf(arr2[i]) > -1) {
        arr1.splice(arr1.indexOf(arr2[i]), 1);
      }
    }
    element.className = arr1.join(" ");
  }
