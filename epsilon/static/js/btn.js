'use-strict'

const e = React.createElement;

class Btn extends React.Component {
    constructor(props){
        super(props);
    }

    render(){
        return e(
            'button',
            {value: this.props.value,
             type: 'submit',
             id:"main-button-slider"},
            this.props.text 
        )
    }
}

document.querySelectorAll('.btn_container')
    .forEach(domContainer => {
        const value = String(domContainer.dataset.value);
        const text = String(domContainer.dataset.text);
        ReactDOM.render(
            e(Btn, {value: value, text: text}), domContainer
        );
    });