import { useEffect, useState } from "react";
import "./PersonalScreen.css"
import SentScreen from "./SentScreen";
export default function PersonalScreen({barcode_id}){
    const [data, setData] = useState(null)
    const [send, setSend] = useState(false)
    const apiUrl = `http://${document.location.hostname}:3000/api/personData?barcode_id=${barcode_id}`
    
    console.debug('render')
    useEffect(() => {
        console.debug('fetchData')
        setTimeout(fetchData, 2000);
    },[])
    
    
    async function fetchData(){
        try{
            const response = await fetch(apiUrl);
            const jsonResponse = await response.json()
            const dataJson = jsonResponse;
            console.log(dataJson);
            setData(dataJson[0]);
        }
        catch (err){
            console.log(err)
        }
        
    }

    async function fetchActionData(code) {
        const apiActionUrl = `http://${document.location.hostname}:3000/api/personAction?worker_id=${data.id}&&code=${code}`;
        try{
            const response = await fetch(apiActionUrl);
            setSend(true)
        }
        catch (err){
            console.log(err);
        }
    }
    function start(){
        fetchActionData("start");
    }

    function end(){
        fetchActionData("end");
    }

    function start_break(){
        fetchActionData("start_break");
    }

    function end_break(){
        fetchActionData("end_break");
    }

    if(data == null){
        return <h1>loading</h1>
    }
    else if(send == true){
        return <SentScreen></SentScreen>
    }
    return(
        <div>
            <h1>Welcome {data.first_name}</h1>            
            <button className="button" onClick={start}>Start work</button>
            <button className="button" onClick={end}>End Work</button> <br />
            <button className="button" onClick={start_break}>Start Break</button>
            <button className="button" onClick={end_break}>End Break</button>
        </div>
    )
}