import React from 'react'
import PropTypes from 'prop-types'

const Btn = ({color, text, onClick}) => {
    const remove = (state) => {

        fetch("\remove", {
            methods: ["POST"],
            body: JSON.stringify({
                uid: state.uid,
                tid: state.tid,
            }),}
        ).then(response => response.json()
        );

    }

    return <button style={{backgroundColor: color}} onClick={onClick}>{text}</button>
}

Btn.defaultProps = {
    color: 'white',
    text: 'N/A'
}

Btn.propTypes = {
    color: PropTypes.string,
    text: PropTypes.string,
    onClick: PropTypes.func,
}
export default Btn
