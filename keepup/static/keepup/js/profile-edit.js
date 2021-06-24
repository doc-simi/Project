document.addEventListener('DOMContentLoaded', () => {
    
    // Check the saved gender of the user
    var gender = document.getElementById('sex-value').value;
    console.log(gender);
    if (gender === "Female") {
        document.getElementById("radio2").checked = true;
    } else if (gender === "Male") {
        document.getElementById("radio1").checked = true;
    } else if (gender === "Undisclosed") {
        document.getElementById("radio3").checked = true;
    }

    // Check if password match
    document.getElementById('RepeatPassword').oninput = () => {
        var password = document.getElementById('InputPassword').value;
        var repeat = document.getElementById('RepeatPassword').value;

        var correct = document.getElementById('yes');
        var incorrect = document.getElementById('no');

        if (password != "") {
            if (password == repeat) {
                incorrect.style.display = "none";
                correct.style.display = "block";
            } else {
                correct.style.display = "none";
                incorrect.style.display = "block";
            }
        }

        if (password == "" || repeat == "") {
            incorrect.style.display = "none";
            correct.style.display = "none";
        }
        
    }
    
    document.getElementById('InputPassword').oninput = () => {
        var password = document.getElementById('InputPassword').value;
        var repeat = document.getElementById('RepeatPassword').value;

        var correct = document.getElementById('yes');
        var incorrect = document.getElementById('no');

        if (password != "") {
            if (password == repeat) {
                incorrect.style.display = "none";
                correct.style.display = "block";
            } else {
                correct.style.display = "none";
                incorrect.style.display = "block";
            }
        }
        
        if (password == "" || repeat == "") {
            incorrect.style.display = "none";
            correct.style.display = "none";
        }
    }
});