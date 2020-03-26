from FBAnalyzer import FBAnalyzer
from utils import get_root_path_from_input

if __name__ == '__main__':
    fb_analyzer = FBAnalyzer(root_path=get_root_path_from_input())
    # fb_analyzer = FBAnalyzer.get_pickle_instance("../FBAnalyzer.pkl")

    msg_freq = fb_analyzer.get_msg_freq_minutes_since_midnight(msg_sent=True)
    receive_msg_freq = fb_analyzer.get_msg_freq_minutes_since_midnight(msg_sent=False)

    import numpy as np
    import matplotlib.pyplot as plt

    ax = plt.gca()

    minute, frequency = zip(*msg_freq)
    minute_rc, frequency_rec = zip(*receive_msg_freq)

    indices = np.arange(len(msg_freq))
    indices_rc = np.arange(len(frequency_rec))
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
