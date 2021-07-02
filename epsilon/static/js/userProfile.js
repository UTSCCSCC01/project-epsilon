// import React from 'react';
// import ReactDOM from 'react-dom';

// class EditBtn extends React.Component {
//     constructor(props) {
//         super(props);
//         this.state = {
//             isEditing: false,
//         }
//     };

//     handleClick() {
//         isEditing = this.state.isEditing;
//         this.setState({
//             isEditing: !isEditing,
//         });
//     };

//     render() {
//         const saveOrEdit = isEditing ? "Save" : "Edit";
//         return (
//             <button type="submit">{saveOrEdit}</button>
//         )
//     }
// }

//     ReactDOM.render(
//         <EditBtn />,
//         document.getElementById("editBtn")
//     );

var is_editing = false
function isEditing() {
    //toggle edit/save button
    const valid = document.getElementById("userForm").checkValidity();
    console.log("valid: " + valid);
    console.log("beforeCHange: " + is_editing);
    if (!valid) {
        document.getElementById("validationMsg").innerHTML = "A field is not valid, please try again.";
        console.log("valid: " + valid);
        console.log("afterCHange: " + is_editing);
    } else {
        is_editing = !is_editing;

        if (!is_editing) {
            document.getElementById("userForm").submit();
        }

        updateEditDisplay();
        console.log("valid: " + valid);
        console.log("afterCHange: " + is_editing);
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
    document.getElementById('contact').readOnly = !is_editing;
}

