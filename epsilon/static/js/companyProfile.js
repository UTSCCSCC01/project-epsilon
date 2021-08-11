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
document.getElementById('editForm').style.display =  "none";

var prevName="";
var prevDes="";
var prevPic="";
const img = document.getElementById("pfpi");


function isEditing() {
    //toggle edit/save button
    prevName = document.getElementById('name').value
    prevDes = document.getElementById('description').value

    prevPic = document.getElementById('pfp').src
    const valid = document.getElementById("companyForm").checkValidity();
    if (!valid) {
        document.getElementById("validationMsg").innerHTML = "A field is not valid, please try again.";
    } else {
        is_editing = !is_editing;
        if (!is_editing) {
            document.getElementById("companyForm").submit();
        }

        updateEditDisplay();
    }

}

function disableEdit() {
    is_editing = false;
    document.getElementById('name').value=prevName
    document.getElementById('description').value=prevDes
    document.getElementById('pfp'),src=prevPic
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
        document.getElementById('des-row-1').style.display =  "block";
        document.getElementById('des-row-2').style.display =  "flex";
        document.getElementById('editForm').style.display =  "block";
    } else{
        document.getElementById('des-row').style.display =  "none";
        document.getElementById('des-row-1').style.display =  "none";
        document.getElementById('des-row-2').style.display =  "none";
        document.getElementById('editForm').style.display =  "none";
    }
}

