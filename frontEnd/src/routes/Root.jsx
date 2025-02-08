import React from 'react'
import Header from '../components/Header'
import { Outlet } from "react-router-dom";
import useStore from '../UseStore';
import { useEffect } from 'react';
function Root() {

  const connect = useStore((state) => state.connect);
  const sendData = useStore((state) => state.sendData);


  useEffect(() => {
    connect('http://127.0.0.1:5001');
    sendData('historicalDataRequest');
    
  }, [connect]);



  return (
    <div>
        <Header/>
        <div>
            
        </div>
        <div id="detail">
        <Outlet context={[]} />
      </div>

    </div>
  )
}

export default Root