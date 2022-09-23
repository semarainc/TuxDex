#!/bin/bash

pkill -f 'miracles.py' & systemctl restart wpa_supplicant NetworkManager
