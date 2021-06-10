import React from 'react'
import PropTypes from 'prop-types'

const Btn = ({color, text}) => {
    return <button style={{backgroundColor: color}}>{text}</button>
}

Btn.defaultProps = {
    color: 'white',
    text: 'N/A'
}

Btn.propTypes = {
    color: PropTypes.string,
    text: PropTypes.string,
}
export default Btn
