import { useState } from "react"
import App from "./App";
export default function SentScreen(){
    const [time, setTime] = useState(false);

    setTimeout(() =>{
        setTime(true)
    }, 3000)
    if(time == true){
        return <App></App>
    }
    return(
        <div>
            <h1>Your action has been sent</h1>
        </div>
    )
}