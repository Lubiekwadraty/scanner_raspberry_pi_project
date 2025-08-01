import { useEffect, useState } from "react";
import "./PersonalScreen.css"
const apiUrl = "http://localhost:3000/api/personData"

export default function PersonalScreen(){
    const [data, setData] = useState(null)

    console.debug('render')
    useEffect(() => {
        console.debug('fetchData')
        setTimeout(fetchData, 1000)
    },[])
    
    async function fetchData(){
        const response = await fetch(apiUrl);
        const jsonResponse = await response.json()
        const dataJson = jsonResponse;
        console.log(dataJson)
        setData(dataJson[0])
    }

    if(data == null){
        return <h1>loading</h1>
    }
    return(
        <div>
            <h1>Welcome {data.name}</h1>            
            <button className="button">Start work</button>
            <button className="button">End Work</button>
        </div>
    )
}