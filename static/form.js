window.onload=function() {
    if (!document.getElementById("index")) {
        return false;
    }   
    
    if (document.getElementById("modify")) {
        console.log("funsion");
        loadModForm();
        return false;
    } else {
        document.getElementById("staff_number").onsubmit=function() {
        var value = document.getElementById("form").value;
        
        generateForm(value);
        return false;
        }
    }
}


function loadModForm() {
    $.getJSON($SCRIPT_ROOT + "data", function(data) {
        var staffNumber = data.cache.staff_number;
        generateForm(staffNumber, data.cache);
    });
}



function generateForm(value, data) {
    var f = document.createElement("form");
    f.setAttribute('action', "/timesheet");
    f.setAttribute('method', "POST");

    for (var i = 0; i < value; i++) {
        // p
        f.appendChild(genPStaff(i));
        
        var lb = document.createElement("label");
        lb.appendChild(document.createTextNode(" Starting Time: "));

        if (typeof data !== 'undefined') {
            f.appendChild(genInputTag(i, data.name));
            f.appendChild(genJobSelector(i, data.job));
        } else {
            f.appendChild(genInputTag(i));
            f.appendChild(genJobSelector(i));
        }

        // start selector + label
        var lb = document.createElement("label");
        lb.appendChild(document.createTextNode(" Starting Time: "));
        f.appendChild(lb);
        
        if (typeof data !== 'undefined') {
            f.appendChild(genTimeSelector(i, "start", data.start));
        } else {
            f.appendChild(genTimeSelector(i, "start"));
        }

        // finish selector + label
        lb = document.createElement("label");
        lb.appendChild(document.createTextNode(" Finishing Time: "));
        f.appendChild(lb);
        
        if (typeof data !== 'undefined') {
            f.appendChild(genTimeSelector(i, "finish", data.finish));
        } else {
            f.appendChild(genTimeSelector(i, "finish"));
        }
    }  
    
    // hidden field
    var hidden = document.createElement("input");
    hidden.setAttribute('type', "hidden");
    hidden.setAttribute('name', "num");
    hidden.setAttribute('value', value);
    var staffNum = value;
    f.appendChild(hidden);

    // button
    var br = document.createElement("br");
    f.append(br);
    var btn = document.createElement("button");
    btn.setAttribute('type', "submit");
    btn.appendChild(document.createTextNode("Generate timetable!"));
    f.appendChild(btn);
   
    // remove any previous form

    document.getElementById("new_form").appendChild(f);
}
    

// Generate <p> with staff number
function genPStaff(num) {
    var p = document.createElement("p");
    var pContent = "Staff " + (num + 1);
    p.appendChild(document.createTextNode(pContent));
    return p;
}


// Generate <input> tag
function genInputTag(num, name) {
    var inp = document.createElement("input");
    inp.setAttribute('name', "name" + (num + 1));
    
    if (typeof name !== 'undefined') {
        inp.setAttribute('value', name[num]);
    } else {
        inp.setAttribute('placeholder', "name");
    }
    return inp;
}


// Generate <select> tag for jobs
function genJobSelector(num, job) {
    var jobSelector = document.createElement("select");
    jobSelector.setAttribute('name', "job" + (num + 1));

    var value = ["DLM", "SUP", "LA", "RA"];
    var textValue = ["Manager", "Supervisor", "Assistant", "Relief"];
    
    for (var i = 0; i < value.length; i++) {
        var opt = document.createElement("option");
        opt.setAttribute('value', value[i]);
        
        
        if (typeof job !== 'undefined' && value[i] === job[num]) {
            opt.setAttribute('selected', "");
        } else if (typeof job === 'undefined' && value[i] === "LA") {
            opt.setAttribute('selected', "");
        }
        
        opt.appendChild(document.createTextNode(textValue[i]));
        jobSelector.appendChild(opt);
    }
    return jobSelector;
}


// Generate <select> tag for starting time
function genTimeSelector(num, time, time_index) {
    var timeSelector = document.createElement("select");
    timeSelector.setAttribute('name', time + (num + 1));
    
    var startValue = [0, 1, 2, 3, 4, 5, 6, 7, 8];
    var startTime = ["9:00", "10:00", "10:20", "10:40", "11:00", "12:00",
                    "1:00", "2:00", "3:00"];
    var finishValue = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16];
    var finishTime = ["1:00", "2:00", "3:00", "3:20", "3:40", "4:00", "5:00",
                    "5:30", "6:00", "7:00", "8:00"];
    var selectionValue;
    var selectionTime;
    
    
    if (time === "start") {
        selectionValue = startValue;
        selectionTime = startTime;
    } else {
        selectionValue = finishValue;
        selectionTime = finishTime;
    }

    for (var i = 0; i < selectionValue.length; i++) {
        var opt = document.createElement("option");
        opt.setAttribute('value', selectionValue[i]);
        
        if (typeof time_index !== 'undefined' &&
            selectionValue[i] === parseInt(time_index[num])) {
            opt.setAttribute('selected', "");
        } else if (typeof time_index === 'undefined' &&
                   (selectionValue[i] === 0 || selectionValue[i] === 16)) {
            opt.setAttribute('selected', "");
        }
        
        opt.appendChild(document.createTextNode(selectionTime[i]));
        timeSelector.appendChild(opt);
    }
    return timeSelector;

}   
