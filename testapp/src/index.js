
import ReactDOM from 'react-dom';
import Home from "./Home";
import React, {Component} from 'react';
import {BrowserRouter , NavLink, Route, Switch} from 'react-router-dom';
import Page1 from "./Page1";
import Page2 from "./Page2";

/*
class Navegacao extends Component {
    redirect = () => {
        window.location.href = 'http://localhost:5000/';
        // maybe can add spinner while loading
        return null;
    }
}
*/

/*
// original
ReactDOM.render(
    <React.StrictMode>
        <Home />
    </React.StrictMode>,
    document.getElementById('root')
);
*/

const rootElement = document.getElementById("root");
ReactDOM.render(
    <BrowserRouter>
        <Switch>
            <Route exact path="/" component={Page1} />
            <Route path="/page2" component={Page2} />
            <Route path='/info' component={() => {
                window.location.href = 'http://localhost:5000/info';
                return  null;
            }}/>
        </Switch>
    </BrowserRouter>,
    rootElement
);
