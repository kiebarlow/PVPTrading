import React from 'react'
import Header from '../components/Header'
import { Outlet } from "react-router-dom";

function Root() {
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