import React from 'react';
import {Route, IndexRoute} from 'react-router';

// put all pages to render
import App from "./App";
import Home from "./Home";
import Login from "./Login.js";

// link the pages to routes
export default(
    <Route path="/" component={App}>
        <IndexRoute component={Home}/>
        <Route path="/Login" component={Login}/>
    </Route>
);