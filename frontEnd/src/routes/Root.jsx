import React from 'react'
import Header from '../components/Header'
import GameBrowser from './GameBrowser'

function Root() {
  return (
    <div>
        <Header/>
        <div>
            <GameBrowser/>
        </div>
    </div>
  )
}

export default Root