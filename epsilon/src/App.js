import React, {useState, useEffect} from 'react';

function App() {
   const [initialData, setInitialData]=useState([{}])
   useEffect(() => {
   // const response = await axios.get("http://localhost:6000/api/users", body, config);
//    fetch('/testReact').then(response=>response.json()).then(data=>setInitialData(data))}, []);
   fetch('http://localhost:5000/testReact',
   {headers:{'Accept':'application/json','Content-Type':'application/json'}}).then(response=>response.json()).then(data=>setInitialData(data))}, []);

 return (<div className="mock app">
           <h1>{initialData.title}</h1>
        </div>
        );
};

export default App;