'use strict';

const e = React.createElement;

class LikeButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = { available: false };
    }

    render() {
        if (this.state.liked) {
            return 'Navigation Menu is available.';
        }

        return e(
            'button',
            { onClick: () => this.setState({ liked: true }) },
            'Available'
        );
    }
}

const domContainer = document.querySelector('#like_button_container');
ReactDOM.render(e(LikeButton), domContainer);
