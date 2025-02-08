import React from 'react'
import Header from '../components/Header'
import GameBrowser from './GameBrowser'
import TradePage from './TradePage'

function Root() {
  return (
    <div>
        <Header/>
        <div>
            <TradePage/>
        </div>
    </div>
  )
}

export default Root