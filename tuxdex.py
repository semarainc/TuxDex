
import os
import sys
import requests
import json
import subprocess
import time
import signal
import capabilitiesCheck as CapCheck

MiraRun = 0

def app_path(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)

def choosen(wifi):
    global MiraRun
    while 1:
        os.system("clear")
        print("******TuxDex Main Control*******")
        print("Select Menu: ")
        print("1. Connect to USB")
        print("2. Connect to TCP")
        print("3. Exit")
        chooser = input("Pilihan: ")

        if chooser == "1":

            if MiraRun == 0:
                print("Please Insert Password To Launch Miraclecast as Superuser")
                print("==> Waiting User To Connect Dex From Phone!")
                mir = subprocess.Popen(f"pkexec python3 {app_path('miracles.py')} {wifi} >> /dev/null", shell=True)
                time.sleep(4)

                while not os.path.exists("/var/koneksimiracle"):
                    pass
            else:
                print("Reuse Connection...")
            subprocess.run('notify-send "Connecting to Samsung Dex..."', shell=True)
            subprocess.Popen("pkill scrcpy & pkill ffplay", shell=True)
#            time.sleep(10)
            subprocess.Popen('''ffplay -ar 48000 -ac 2 -b:v 0 -b:a 1k -max_delay 0 -buffer_size 15k -framedrop  -vf "setpts=(PTS*1)" -vn -sn -nodisp rtp://127.0.0.1:1991 --loglevel quiet''', shell=True)
            subprocess.run('''scrcpy -d --display 2  --window-title "TuxDex - Alpha" --fullscreen --forward-all-clicks > /dev/null''', shell=True)
            subprocess.check_output("pkexec kill {}".format(mir.pid), shell=True)
            sys.exit(0)
        elif chooser == "2":
            subprocess.Popen("pkill scrcpy & pkill ffplay", shell=True)
            ipport = input("Insert IP:PORT => ")

            if MiraRun == 0:
                print("Please Insert Password To Launch Miraclecast as Superuser")
                print("==> Waiting User To Connect Dex From Phone!")
                subprocess.run('notify-send "Open And Connect Dex From Your Phone!"', shell=True)
                mir = subprocess.Popen(f"pkexec python3 {app_path('miracles.py')} {wifi} >/dev/null", shell=True)
                time.sleep(4)
                while not os.path.exists("/var/koneksimiracle"):
                    pass
            else:
                print("Reuse Connection...")
            subprocess.run('notify-send "Connecting to SamsungDex..."', shell=True)
#            time.sleep(10)
            WaitToConnect(str(ipport))
            print("Restoring NetworkManager and Connecting To Device (Ensure Wifi Is Stable)...")
            time.sleep(3)
            input("Press Enter If Your Wifi is Ready, To Connect To SamsungDex...")
            MiraRun = 1
            subprocess.Popen(f'''scrcpy --tcpip={str(ipport)} --display 2  -b 2M --window-title "TuxDex - Alpha" --fullscreen --forward-all-clicks >/dev/null && pkill ffplay''', shell=True)
            zelda = subprocess.run('''ffplay -ar 48000 -ac 2 -b:v 0 -b:a 2k -max_delay 0 -buffer_size 10k -framedrop  -vf "setpts=(PTS*1)" -vn -sn -nodisp rtp://127.0.0.1:1991 -loglevel quiet''', shell=True)
            os.system("pkill scrcpy && pkill ffplay")
            #zelda.kill()
            choosen(wifi)
        elif chooser == '3':
            print("Insert Password Before Exit to Restore NetworkManager")
            subprocess.run(f"pkexec {app_path('tuxdex-restore.sh')}", shell=True)
            sys.exit("App Exited Successfuly")

def WaitToConnect(ip):
    readines = 0
    while not readines:
        z = subprocess.Popen(f"adb connect {ip}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if 'connected' in str(z.communicate()[0]):
            readines = 1
        time.sleep(3)

def main():
    wifi_ = CapCheck.CapabilityChecking()
    try:
        print("Welcome to TuxDex")
        print("Preparing Data...")
        print("Make Sure You Are Connected From Miraclecast")
        print("Starting Miraclecast.., Insert sudo password...")
#    time.sleep(2)
#    subprocess.Popen("sudo python3 ~/Documents/python/miracles.py", shell=True)
        subprocess.Popen("pkill scrcpy && pkill ffplay", shell=True)

#    time.sleep(20)

        choosen(wifi_)

    except KeyboardInterrupt:
        os.system("clear")
        print("Insert Password Before Exit to Restore NetworkManager")
        subprocess.run(f"pkexec {app_path('tuxdex-restore.sh')}",shell=True)

main()
