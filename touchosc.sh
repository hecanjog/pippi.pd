#!/bin/bash
modprobe -r ath_pci
modprobe ath_pci autocreate=adhoc
wlanconfig ath0 destroy
wlanconfig ath create wlandev wifi0 wlanmode adhoc

ifconfig ath0 down
iwconfig ath0 mode ad-hoc
iwconfig ath0 channel 4
iwconfig ath0 essid 'pippi'
ifconfig ath0 10.0.0.1 up
