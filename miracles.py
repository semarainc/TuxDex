
import os
import pexpect
import subprocess
import sys
import time
import netifaces as ni

if __name__ == "__main__":  # a guard from unintended usage
    try:
        os.remove("/var/koneksimiracle")
    except:
        pass

    print("Disabling NetworkManager and WpaSupplicant Temporarily")
    subprocess.Popen("systemctl stop NetworkManager wpa_supplicant", shell=True)
    time.sleep(5)
    print("Starting Miraclecast")
#    q = pexpect.spawn('miracle-wifid --lazy-managed', encoding='utf-8')
    q = pexpect.spawn(f'miracle-wifid --interface {sys.argv[1]}', encoding='utf-8')
    q.setecho(False)
    time.sleep(2)
    p = pexpect.spawn("miracle-sinkctl --external-player true --port 1991 --audio 1", encoding='utf-8')
    p.setecho(False)
    p.logfile_read = sys.stdout

    p.sendline("set-managed 3 yes")
    #time.sleep(2)
    p.sendline("run 3")

    print("System Ready..., Waiting To Connect then Starting All NM and Wpa Back")
    time.sleep(5)
    #subprocess.Popen("systemctl start wpa_supplicant NetworkManager", shell=True)
    #time.sleep(5)
    konek = -1
    while 1:
        if konek == -1:
            time.sleep(5)
            #subprocess.Popen("systemctl restart NetworkManager wpa_supplicant", shell=True)
            konek = 0
        if not konek:
            p.expect("NOTICE: SINK connected", timeout=None)
        elif konek:
            p.expect("NOTICE: SINK disconnected", timeout=None)
        #print(p.after)

        if 'NOTICE: SINK connected' in str(p.after):
            konek = 1
            #p.expect("[DISCONNECT] Peer:")
            print("YOU ARE CONNECTED")
            subprocess.Popen("systemctl restart NetworkManager wpa_supplicant", shell=True)
            with open("/var/koneksimiracle", 'w') as f:
                f.write("Gua")
            #break
        elif "NOTICE: SINK disconnected" in str(p.after):
            konek = 0
            print("DISCONNECT")
            try:
                os.remove("/var/koneksimiracle")
            except:
                pass

    input("KEEPING IT RUNNING :D")

