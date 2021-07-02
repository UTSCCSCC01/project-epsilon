// import React from 'react';
// import ReactDOM from 'react-dom';
// import EditBtn from './editBtn';

class EditBtn extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isEditing: false
        }
    }

    handleClick() {
        isEditing = this.state.isEditing;
        this.setState({
            isEditing: !isEditing,
        });
    }

    render() {
        const saveOrEdit = isEditing ? "Save" : "Edit"
        return (
            <button type="submit">{saveOrEdit}</button>
        )
    }
};

    ReactDOM.render(
        <EditBtn />,
        document.getElementById("editBtn")
    );
