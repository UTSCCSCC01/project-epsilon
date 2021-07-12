import React from "react";
import {Link, NavLink} from "react-router-dom";

function Page1() {
    return (
        <div>
            <p>
                This is the first page.
                <br />
                Click on the button below.
            </p>
            <Link to="/page2">
                <button>
                button Page 2
            </button>
            </Link>
            <li>
                <NavLink exact to="/page2">link to page 2</NavLink>
            </li>
        </div>
    );

}

export default Page1;