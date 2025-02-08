import asyncio
import json
import websockets
from datetime import datetime
import time

class BinanceTradeManager:
    def __init__(self, window_minutes=10):
        self.BINANCE_WS_URL = "wss://stream.binance.com:443/stream?streams=btcusdt@trade/solusdt@trade/ethusdt@trade"
        self.candle_manager = CandleStickManager(window_minutes)
        self.kline_manager = KlineManager()
        
    async def connect(self):
        print("Connecting to Binance WebSocket...")
        async with websockets.connect(self.BINANCE_WS_URL) as websocket:
            print("Connected to Binance WebSocket")
            await self.subscribe(websocket)
            await self.listen(websocket)

    async def subscribe(self, websocket):
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": [
                "btcusdt@kline_1s",
                "ethusdt@kline_1s",
                "solusdt@kline_1s"
            ],
            "id": 1
        }
        await websocket.send(json.dumps(subscribe_message))
        response = await websocket.recv()
        print(f"Subscription response: {response}")

    async def listen(self, websocket):
        try:
            while True:
                message = await websocket.recv()
                await self.process_message(json.loads(message))
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"Error in listen loop: {e}")

    async def process_message(self, message):
        #print(f"Received message: {message}")
        try:
            if 'data' not in message:
                return
            stream = message['stream']
            if '@trade' in stream:
                self.candle_manager.process_trade(message)
                await self.print_latest_stats(message['stream'].split('@')[0].upper())
            elif '@kline' in stream:
                self.kline_manager.process_kline(message)
            
        except Exception as e:
            print(f"Error processing message: {e}")

    async def print_latest_stats(self, trading_pair):
        candles = self.candle_manager.get_candles(trading_pair, limit=1)
        if candles:
            candle = candles[0]
            print(f"\n{trading_pair} Stats at {datetime.fromtimestamp(candle.timestamp)}:")
            print(f"OHLC: ${candle.open:.2f}, ${candle.high:.2f}, ${candle.low:.2f}, ${candle.close:.2f}")
            print(f"Volume: {candle.volume:.4f} | Trades: {candle.trades_count}")
            if candle.vwap:
                print(f"VWAP: ${candle.vwap:.2f}")
                

class CandleStickManager:
    def __init__(self, window_minutes=10):
        self.window_seconds = window_minutes * 60
        self.trading_pairs = {}
    
    class Candle:
        def __init__(self, timestamp):
            self.timestamp = timestamp
            self.open = None
            self.high = 0
            self.low = float('inf')
            self.close = None
            self.volume = 0
            self.trades_count = 0
            self.vwap_sum = 0
            
        @property
        def vwap(self):
            return self.vwap_sum / self.volume if self.volume > 0 else None
    
    def process_trade(self, message):
        stream_name = message['stream']
        trading_pair = stream_name.split('@')[0].upper()
        
        if trading_pair not in self.trading_pairs:
            self.trading_pairs[trading_pair] = {}
        
        trade_data = message['data']
        price = float(trade_data['p'])
        quantity = float(trade_data['q'])
        trade_time = trade_data['T'] // 1000
        candle_timestamp = trade_time - (trade_time % 1)
        
        pair_candles = self.trading_pairs[trading_pair]
        
        if candle_timestamp not in pair_candles:
            candle = self.Candle(candle_timestamp)
            candle.open = price
            pair_candles[candle_timestamp] = candle
        else:
            candle = pair_candles[candle_timestamp]
        
        candle.high = max(candle.high, price)
        candle.low = min(candle.low, price)
        candle.close = price
        candle.volume += quantity
        candle.trades_count += 1
        candle.vwap_sum += price * quantity
        
        self._cleanup_old_candles(trading_pair)
    
    def _cleanup_old_candles(self, trading_pair):
        current_time = int(time.time())
        cutoff_time = current_time - self.window_seconds
        pair_candles = self.trading_pairs[trading_pair]
        
        outdated_timestamps = [ts for ts in pair_candles.keys() if ts < cutoff_time]
        if outdated_timestamps:
            print(f"Cleaning up {len(outdated_timestamps)} outdated candles for {trading_pair}")
        for ts in outdated_timestamps:
            del pair_candles[ts]
    
    def get_candles(self, trading_pair, start_time=None, limit=None):
        if trading_pair not in self.trading_pairs:
            return []
        
        if start_time is None:
            start_time = int(time.time()) - self.window_seconds
            
        candles = sorted([
            candle for candle in self.trading_pairs[trading_pair].values()
            if candle.timestamp >= start_time
        ], key=lambda x: x.timestamp)
        
        if limit:
            return candles[-limit:]
        return candles

class KlineManager:
    def __init__(self, window_minutes=10):
        self.window_seconds = window_minutes * 60
        self.kline_data = {}  # {symbol: {interval: {timestamp: KlineData}}}

    class KlineData:
        def __init__(self, kline):
            self.start_time = int(kline['t']) // 1000
            self.end_time = int(kline['T']) // 1000
            self.interval = kline['i']
            self.open = float(kline['o'])
            self.high = float(kline['h'])
            self.low = float(kline['l'])
            self.close = float(kline['c'])
            self.volume = float(kline['v'])
            self.trades_count = int(kline['n'])
            self.is_closed = kline['x']
            self.quote_volume = float(kline['q'])
            self.taker_buy_volume = float(kline['V'])
            self.taker_buy_quote_volume = float(kline['Q'])

    def process_kline(self, message):
        symbol = message['data']['s']
        kline = message['data']['k']
        interval = kline['i']

        if symbol not in self.kline_data:
            self.kline_data[symbol] = {}
        if interval not in self.kline_data[symbol]:
            self.kline_data[symbol][interval] = {}

        self.kline_data[symbol][interval][kline['t']] = self.KlineData(kline)
        self.print_kline_summary(symbol)

    def get_latest_kline(self, symbol, interval):
        if symbol in self.kline_data and interval in self.kline_data[symbol]:
            klines = self.kline_data[symbol][interval]
            if klines:
                latest_timestamp = max(klines.keys())
                return klines[latest_timestamp]
        return None
    
    # Get all klines for a symbol in the past N minutes
    def get_cached_kline(self, symbol, past):
        current_time = int(time.time())
        cutoff_time = current_time - (past * 60)
        cached_klines = []

        if symbol in self.kline_data:
            for interval in self.kline_data[symbol]:
                klines = self.kline_data[symbol][interval]
                for ts in sorted(klines.keys()):
                    if ts >= cutoff_time:
                        cached_klines.append(klines[ts])

        return cached_klines

    def print_kline_summary(self, symbol):
        print(f"\nKline Summary for {symbol}:")
        for interval in self.kline_data.get(symbol, {}):
            kline = self.get_latest_kline(symbol, interval)
            if kline:
                print(f"\n{interval} Candle:")
                print(f"OHLC: ${kline.open:.2f}, ${kline.high:.2f}, "
                      f"${kline.low:.2f}, ${kline.close:.2f}")
                print(f"Volume: {kline.volume:.4f} | Trades: {kline.trades_count}")
                
    def cleanup_old_klines(self, symbol, interval):
        current_time = int(time.time())
        cutoff_time = current_time - self.window_seconds
        klines = self.kline_data.get(symbol, {}).get(interval, {})
        for ts in list(klines.keys()):
            if ts < cutoff_time:
                print("Cleaning up outdated kline")
                del klines[ts]
        

async def main():
    manager = BinanceTradeManager()
    await manager.connect()

if __name__ == "__main__":
    asyncio.run(main())