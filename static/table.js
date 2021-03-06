function createTable() {
    if (!document.getElementById("table_result")) {
        return false;
    }
    $.getJSON($SCRIPT_ROOT + "timesheet/t", function(result) {
        
        var tbl = document.createElement('table');
        
        var lenRow = Object.keys(result.table).length;
        var lenCol = result.table[Object.keys(result.table)[0]].length;

        for (var i = 0; i < lenRow; i++) {
            var tr = tbl.insertRow();
            
            for (var j = -1; j < lenCol; j++) {
                var td = tr.insertCell();
                if (j == -1) {
                    td.setAttribute('class', 'table-names');
                    if (i == 0) {
                        td.appendChild(document.createTextNode(''));
                    } else {
                        td.appendChild(document.createTextNode(
                                    result.names['staff'.concat(i)].name));
                    }
                } else {
                // color function here
                var cell = result.table[Object.keys(result.table)[i]][j];
                if (i > 0) {
                    td.setAttribute("bgcolor", cellColor(cell));
                }
                td.appendChild(document.createTextNode(cell));
                
                }
            }
        }
        var div = document.getElementById('timetable');
        while (div.firstChild) {
            div.removeChild(div.firstChild);
        }
        document.getElementById('timetable').appendChild(tbl);
        
        var timeGen = document.createElement('p');
        timeGen.setAttribute('id', 'time-gen');
        var str1 = 'Timetable generated in ';
        var str2 = ' seconds';
        var message = str1.concat(result.time.concat(str2));
        timeGen.appendChild(document.createTextNode(message));
        document.getElementById('timetable').appendChild(timeGen);
     });
}

function cellColor(cellContent) {
    var color;
    switch (cellContent) {
        case " ":
            color = "#f9c381";
            break;
        case "ADU":
            color = "#ff0000";
            break;
        case "QP": 
            color = "#668cff";
            break;
        case "JUV":
            color = "#99d68d";
            break;
        case "T":
        case "L":
            color = "#ffeba5";
            break;
        default:
            color = "white";
    }
    return color;
};

document.addEventListener('DOMContentLoaded', function() {
    createTable();
}, false);


