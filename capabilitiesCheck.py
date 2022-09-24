import os
import sys
import subprocess

def app_path(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

def ProcessMe(cmd, shell=True):
    proc = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    retproc = proc.communicate()
    retval = []
    for i in retproc:
        retval.append(i.decode("utf-8"))
    return retval

def InstallPips():
    print("Installing Library Needed For Miracles.py...")
    ProcessMe("pkexec pip3 install netifaces pexpect")
    print("Library Installed...")
    with open(app_path(".installed"), 'w') as f:
        f.write("")

def NotifySendCheck():
    if any('command not found' not in s for s in ProcessMe("notify-send --version")):
        print("[INFO] Notify-send Installed")
    else:
        print("[ERROR] Notify-send Not Installed")

def MiracleCastCheck():
    if any('NOTICE: Must run as root' in s for s in ProcessMe("miracle-wifid")):
        print("[INFO] Miraclecast Installed")
    else:
        print("[ERROR] Miraclecast Not Installed")

def ScrcpyCheck():
    if any('<https://github.com/Genymobile/scrcpy>' in s for s in ProcessMe("scrcpy")):
        print("[INFO] Scrcpy Installed")
    else:
        print("[ERROR] Scrcpy Not Installed")

def P2PCapableCheck():
    p2pwifi = {}
    idx = 1
    base_dir = "/sys/class/net"
    for wireless in os.listdir(base_dir):
        if os.path.exists(os.path.join(base_dir,wireless, "wireless")):
            idxphy = ProcessMe(f"iw dev {wireless} info | grep wiphy | awk '{{print $2}}'")[0].strip()
            p2pcap = ProcessMe(f'''iw phy phy{idxphy} info | grep -Pzo "(?s)Supported interface modes.*Supported commands" | grep "P2P"''')
            if any('binary file matches' in p for p in p2pcap):
                p2pwifi[str(idx)] = str(wireless)
                idx += 1

    return p2pwifi

def CapabilityChecking():
    if not os.path.exists(".installed"):
        InstallPips()
        NotifySendCheck()
        MiracleCastCheck()
        ScrcpyCheck()
        input("Press Enter To Continue...")

    chooseWifi = P2PCapableCheck()

    while 1:
        os.system("clear")
        print("***Available Interface That Support Wifi-Direct**")
        for idx, wifi in chooseWifi.items():
            print(idx, wifi)

        choice = input(f"Choose Number: ")

        if any(choice not in s for s in chooseWifi.keys()):
            print("Interface NotFound")
        else:
            print(f"Selected: {chooseWifi[choice]}")
            break
    return chooseWifi[choice]
