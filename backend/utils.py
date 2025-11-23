# backend/utils.py
import pandas as pd




def compute_technical_indicators(df: pd.DataFrame):
# expects 'close' column
out = {}
out['last_close'] = float(df['close'].iloc[-1])
# simple SMA
out['sma_20'] = float(df['close'].rolling(window=20, min_periods=1).mean().iloc[-1])
out['sma_50'] = float(df['close'].rolling(window=50, min_periods=1).mean().iloc[-1])
# RSI simple approximation
delta = df['close'].diff()
up = delta.clip(lower=0).fillna(0)
down = -1 * delta.clip(upper=0).fillna(0)
roll_up = up.rolling(14, min_periods=1).mean()
roll_down = down.rolling(14, min_periods=1).mean()
rs = roll_up / (roll_down + 1e-8)
rsi = 100 - (100 / (1 + rs))
out['rsi_14'] = float(rsi.iloc[-1])
# MACD (fast 12 slow 26)
ema12 = df['close'].ewm(span=12, adjust=False).mean()
ema26 = df['close'].ewm(span=26, adjust=False).mean()
macd = ema12 - ema26
out['macd'] = float(macd.iloc[-1])
return out
