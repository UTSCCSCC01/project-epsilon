import { LogInfoPlugin } from 'enhanced-resolve';
import React from 'react';

class Login extends React.Component {
    constructor(){
        super();
        this.state={
            msg:"",
            user:"",
            pwd:""
        };
        this.tryCredentials = this.tryCredentials.bind(this);
        this.userChange = this.userChange.bind(this);
        this.pwdChange = this.pwdChange.bind(this);
    }

    userChange(){
        this.state.user = document.getElementById("username").value;
    }
    pwdChange(){
        this.state.pwd = document.getElementById("password").value;
    }

    tryCredentials(){
        fetch("/tryLogin", {
            body: JSON.stringify({username: this.state.user, 
                                  passsowrd: this.state.pwd})
        }).then(res => res.json())
        .then(res => this.setState({msg:res.msg}));
    }

    render(){
        return(
            <div>
                <div id="background" class="title-card">
                    <h1>Epsilon</h1>
                    <h2>Login to get started</h2>
                    <hr/>
                </div>
                <div class="contents">
                    <p class="error"> {this.state.msg}</p>
                    
                    <br/>
                    <input class="auth" type="text" placeholder="Username" name="username" onChange="userChange()"/>
                    <br/>
                    <input class="auth" type="text" placeholder="Password" name="password" onChange="pwdChange()"/>
                    <br/>
                    <br/>
                    <input type="button" onSubmit="tryCredentials()">
                        <label>Logim</label>
                    </input>
                    
                </div>
            </div>
        );
    }

}

export default Login;