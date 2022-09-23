# TuxDex
Script to Help Run Your Samsung Dex From Linux Machine
Note: The Current Script is messy but it works :)

## Limitation
  The Current script is not really stable, but overall it works well on my machine, currently miraclecast requires to turnoff NetworkManager and WPA_Supplicant when activating it as as sink thats why before connecting to SamsungDex it needs to disable your wifi temporarily

## Requirements
- Python >=3.6
- notify-send
- [miraclecast](https://github.com/albfan/miraclecast)
- [scrcpy](https://github.com/Genymobile/scrcpy)
- Enable Developer Tools On Samsung S-Series Phone
- Enable Wireless Debugging

## Installation
```bash
  $ git clone https://github.com/semarainc/TuxDex
  $ chmod +x tuxdex-restore.sh
```
## How To Use
```bash
  $ python3 tuxdex.py
```

## DEMO
[![TuxDexDemo](https://img.youtube.com/vi/2AE4A_fFCOA/0.jpg)](https://www.youtube.com/watch?v=2AE4A_fFCOA)
