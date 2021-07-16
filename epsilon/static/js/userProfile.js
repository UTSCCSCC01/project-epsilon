var is_editing = false
document.getElementById('des-row').style.display =  "none";

function isEditing() {
    //toggle edit/save button
    const valid = document.getElementById("userForm").checkValidity();
    if (!valid) {
        document.getElementById("validationMsg").innerHTML = "A field is not valid, please try again.";
    } else {
        is_editing = !is_editing;

        if (!is_editing) {
            document.getElementById("userForm").submit();
        }

        updateEditDisplay();
    }

}

function disableEdit() {
    is_editing = false;
    updateEditDisplay();
}

function updateEditDisplay() {
    // switch between editable/readonly fields

    var response_msg = document.getElementById("responseMsg");

    if(response_msg) {
        response_msg.innerHTML = "";
    }

    const pencil_icon = '<i class="fa fa-pencil" aria-hidden="true""></i> ';
    let display_name = is_editing ? "Save" : "Edit";

    document.getElementById("editBtn").innerHTML = pencil_icon + display_name;
    document.getElementById("discardBtn").style.display = is_editing ? "inline" : "none";

    document.getElementById('name').readOnly = !is_editing;
    document.getElementById('description').readOnly = !is_editing;

    if (display_name==="Save"){
        document.getElementById('des-row').style.display =  "block";
    } else{
        document.getElementById('des-row').style.display =  "none";
    }
    // document.getElementById('des-row').style.display = is_edit ? "block" : "none";

}


// let x = document.getElementById('des-row');
// x.style.display = "none";