import { useState } from 'react';
import './App.css'
import Default from './Default' 
import PersonalScreen from './PersonalScreen'

import mqtt from "mqtt"; // https://www.npmjs.com/package/mqtt

export default function App() {
  const client = mqtt.connect(`ws://${document.location.hostname}:9001`);
  const [change, setChange] = useState(false);    
  const [latestMessage, setLatestMessage] = useState(null);
  
    client.on("connect", async() =>{
        console.log("it's working")
    })
    client.on("message", async (topic, message) => {
        // message is Buffer
        setLatestMessage(message.toString());
        setChange(true);
        // client.end();
    });
    
    client.subscribe("scan/code");
  return (
    <>
      {change ? <PersonalScreen barcode_id={latestMessage}/> : <Default/>}
    </>
  )
}


