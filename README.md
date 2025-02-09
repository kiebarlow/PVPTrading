# PVPTrading

Welcome to [pvptrading.club](https://pvptrading.club), where you can test your crypto trading skills against your friends (or enemies) and win the jackpot!

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

PVPTrading is a platform made for Hackaway v8 using Flask, React and real-time Binance data, where users can engage in competitive crypto trading. Users can create or join lobbies, trade cryptocurrencies in real-time, and win the prize pool by having the highest balance when the time expires.

## Features

- Real-time crypto trading
- Create and join lobbies
- Compete against other traders
- Real-time updates
- Historical data and charting to understand where the market is heading

## Installation

To get started with PVPTrading, follow these steps:

1. Clone the repository:
    ```
    bash
    git clone https://github.com/kiebarlow/PVPTrading.git
    cd PVPTrading
    ```

2. Install the required dependencies:
    For the python
    ```
    pip install -r backEnd/requirements.txt
    ```
    For the React
    ```
    cd frontEnd
    npm install
    ```

3. Run the application:
    Start the Flask server
    ```
    cd backEnd
    python BackEnd.py
    ```
    In a new terminal, start the React frontend
    ```
    cd ../frontend
    npm dev build
    npm start
    ```

## Usage
Open your web browser and navigate to http://localhost:5000.

Create a new lobby or join an existing one.

Start trading and compete against other users.
