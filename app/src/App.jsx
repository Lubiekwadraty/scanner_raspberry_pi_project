import { useState } from 'react';
import './App.css'
import Default from './default' 
import PersonalScreen from './PersonalScreen'

import mqtt from "mqtt"; // https://www.npmjs.com/package/mqtt

export default function App() {
  const client = mqtt.connect("mqtt://localhost:9001");
  const [change, setChange] = useState(false);    
  const [latestMessage, setLatestMessage] = useState(null);
  

    client.on("message", async (topic, message) => {
        // message is Buffer
        console.log(message.toString());
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


