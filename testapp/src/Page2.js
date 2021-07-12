import React, {useState, useEffect, Component} from 'react';

function Page2() {
    const [initialData, setInitialData]=useState([{}])
    useEffect(() => {
        // const response = await axios.get("http://localhost:6000/api/users", body, config);
//    fetch('/testReact').then(response=>response.json()).then(data=>setInitialData(data))}, []);

        fetch('http://localhost:5000/testReact',
            {headers:{'Accept':'application/json','Content-Type':'application/json'}}).then(response=>response.json()).then(data=>setInitialData(data))}, []);
    return (
        <div>
            <h1>{initialData.title}</h1>
            <p>This is the second page.</p>
        </div>
    );
}

export default Page2;