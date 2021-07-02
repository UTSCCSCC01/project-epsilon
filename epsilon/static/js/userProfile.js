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
    
    document.getElementById("responseMsg").innerHTML = "";
    
    const pencil_icon = '<i class="fa fa-pencil" aria-hidden="true""></i> ';
    let display_name = is_editing ? "Save" : "Edit";

    document.getElementById("editBtn").innerHTML = pencil_icon + display_name;
    document.getElementById("discardBtn").style.display = is_editing ? "inline" : "none";

    document.getElementById('name').readOnly = !is_editing;
    document.getElementById('description').readOnly = !is_editing;
    document.getElementById('contact').readOnly = !is_editing;
}

