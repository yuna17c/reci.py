function searchTable() {
    var input = document.getElementById("search_input");
    var filter = input.value.toUpperCase();
    var table = document.getElementById("fridge-table");
    var rows = table.getElementsByTagName("tr");

    for (var i = 0; i < rows.length; i++) {
        var row = rows[i].getElementsByTagName("td")[0];
        if (row) {
            var text = row.textContent || row.innerText;
            if (text.toUpperCase().indexOf(filter) > -1) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}