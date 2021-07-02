// import React from 'react';
// import ReactDOM from 'react-dom';
// // import EditBtn from './editBtn';

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
    is_editing = !is_editing;
    console.log(is_editing);

    const pencil_icon = '<i class="fa fa-pencil" aria-hidden="true""></i> ';
    let display_name = is_editing ? "Save" : "Edit";
    document.getElementById("editBtn").innerHTML = pencil_icon + display_name;

    document.getElementById('name').readOnly = !is_editing;
    document.getElementById('description').readOnly = !is_editing;
    document.getElementById('contact').readOnly = !is_editing;
    if (!is_editing) {
        document.getElementById("userForm").submit();
    }
}
