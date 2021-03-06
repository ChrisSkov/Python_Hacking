from scapy.all import *
from threading import Thread
import pandas
import time
import os

# BSSID is MAC address of the access point
networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto"])
networks.set_index("BSSID", inplace=True)


def callback(packet):
    if packet.haslayer(Dot11Beacon):
        bssid = packet[Dot11].addr2
        ssid = packet[Dot11Elt].info.decode()
        try:
            dbm_signal = packet.dBm_AntSignal
        except:
            dbm_signal = "N/A"

        stats = packet[Dot11Beacon].network_stats()
        channel = stats.get("channel")
        crypto = stats.get("crypto")
        networks.loc[bssid] = (ssid, dbm_signal, channel, crypto)


def print_all():
    while True:
        os.system("clear")
        print(networks)
        time.sleep(0.5)


def change_channel():
    ch = 1
    while True:
        os.system(f"iwconfig {interface} channel {ch}")
        ch = ch % 36 + 1
        time.sleep(0.5)


if __name__ == "__main__":
    interface = "wlan0mon"
    printer = Thread(target=print_all)
    printer.daemon = True
    printer.start()

    channel_changer = Thread(
        target=change_channel)  # change channel command = iwconfig wlan0mon channel 2  changes to channel 2
    channel_changer.daemon = True
    channel_changer.start()

    sniff(prn=callback, iface=interface)
