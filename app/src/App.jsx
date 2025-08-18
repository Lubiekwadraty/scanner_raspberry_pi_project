import { useState } from 'react';
import './App.css'
import Default from './default' 
import PersonalScreen from './PersonalScreen'

import mqtt from "mqtt"; // https://www.npmjs.com/package/mqtt

export default function App() {
  const client = mqtt.connect("mqtt://localhost:9001");
  const [change, setChange] = useState(false)    
    let latestMessage = null;

    client.on("message", async (topic, message) => {
        // message is Buffer
        console.log(message.toString());
        latestMessage = message.toString();
        setChange(true);
        // client.end();
    });
    
    client.subscribe("scan/code");
  return (
    <>
      {change ? <PersonalScreen/> : <Default/>}
    </>
  )
}


