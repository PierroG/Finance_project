
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import talib
from talib import stream

close = np.random.random(20)
cclose = [close[:i] for i in range(1, len(close))]

print(cclose)
sma = talib.SMA(close, timeperiod=5)
ema = talib.EMA(close, timeperiod=5)


sma = [stream.SMA(close, timeperiod=5) for close in cclose]
ema = [stream.EMA(close, timeperiod=5) for close in cclose]

plt.plot(close)
plt.plot(sma)
plt.plot(ema)
plt.show()