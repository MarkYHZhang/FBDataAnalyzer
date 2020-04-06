from FBAnalyzer import FBAnalyzer
from utils import get_root_path_from_input

import matplotlib.pyplot as plt

if __name__ == '__main__':
    # fb_analyzer = FBAnalyzer(root_path=get_root_path_from_input())
    # fb_analyzer.save_to_pickle("../FBAnalyzer.pkl")
    fb_analyzer = FBAnalyzer.get_pickle_instance("../FBAnalyzer.pkl")

    msg_freq = fb_analyzer.get_all_msg_freq_minutes_since_midnight(msg_sent=True)
    receive_msg_freq = fb_analyzer.get_all_msg_freq_minutes_since_midnight(msg_sent=False)

    minute, frequency = zip(*msg_freq)
    minute_rec, frequency_rec = zip(*receive_msg_freq)

    plt.hist(
        [minute, minute_rec],
        weights=[frequency,frequency_rec],
        bins=1440//30,
        label=["Characters Sent", "Characters Received"],
        edgecolor='black',
        linewidth=0.8
    )

    plt.xticks(ticks=minute[::60], labels=range(25))
    plt.title("Hours in Day vs Frequency of Messages")
    plt.xlabel("Hours in Day (24h format)")
    plt.ylabel("Number of Messages sent")
    plt.legend(loc="upper left")
    plt.savefig('../../docs/images/msg_freq_histogram.png', dpi=500)
