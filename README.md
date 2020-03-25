# FBDataAnalyzer
A tool that enables you to easier programmatically (or not) interact with your downloaded Facebook data

## Sample use cases
![Hours in day Vs Frequency of messages](https://raw.githubusercontent.com/MarkYHZhang/FBDataAnalyzer/master/docs/images/filename.png)

### Analysis
Directly, from the graph you can tell:
1. I message people more than they message me (in terms of characters count)
2. I tend to initiate conversations more
3. People usually responds 1-3 bars after, (every bar is 15 min)

### Code
```python
# ---------------------------[ FBDataAnalyzer Code ]------------------------------
from FBAnalyzer import FBAnalyzer
fb_analyzer = FBAnalyzer(root_path="{PATH_TO_FB_DATA}")
msg_freq = fb_analyzer.get_msg_freq_minutes_since_midnight(msg_sent=True)
receive_msg_freq = fb_analyzer.get_msg_freq_minutes_since_midnight(msg_sent=False)
# ---------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

ax = plt.gca()

minute, frequency = zip(*msg_freq)
minute_rc, frequency_rec = zip(*receive_msg_freq)

indices, indices_rc = np.arange(len(msg_freq)), np.arange(len(frequency_rec))
colors = {'Messages Sent': 'red', 'Messages Received': 'blue'}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]

ax.bar(indices, frequency, color='r')
ax.bar(indices_rc, frequency_rec, color='b')
ax.set_xticks(minute[::4])
ax.set_xticklabels(range(24))
plt.title("Hours in Day vs Frequency of Messages")
plt.xlabel("Hours in Day (24h format)")
plt.ylabel("Number of Messages sent")
plt.legend(handles, labels)
plt.show()
```
