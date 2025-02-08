import React from 'react'
import Header from '../components/Header'
import Bank from './Bank'
import { Outlet, Link } from "react-router-dom";

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