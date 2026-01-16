print("AP Uplink Speed Status")

import paramiko
import time
import logging
import re

USERNAME = "support"
PASSWORD = "Sab18Jaro19++"

IP_START = 130
IP_END = 140
IP_BASE = "192.168.0."

logging.basicConfig(
    filename="AP-Status.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w"
)

def check_port_speed(host):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=USERNAME, password=PASSWORD, timeout=5)

        shell = client.invoke_shell()
        time.sleep(1)

        shell.send("ethtool eth0\n")
        time.sleep(2)

        output = shell.recv(5000).decode("utf-8")

        # Speed und Duplex auslesen
        speed_match = re.search(r"Speed:\s*(\S+)", output)
        duplex_match = re.search(r"Duplex:\s*(\S+)", output)

        speed_value = speed_match.group(1) if speed_match else "unbekannt"
        duplex_value = duplex_match.group(1) if duplex_match else "unbekannt"

        speed_ok = speed_value == "1000Mb/s"
        duplex_ok = duplex_value == "Full"

        if speed_ok and duplex_ok:
            status = "OK"
        else:
            status = "NICHT OK"

        print(f"{host} {status} Speed: {speed_value} Duplex: {duplex_value}")
        logging.info(f"{host} {status} Speed: {speed_value} Duplex: {duplex_value}")

        client.close()

    except Exception:
        print(f"{host} nicht erreichbar")
        logging.info(f"{host} nicht erreichbar")

if __name__ == "__main__":
    for i in range(IP_START, IP_END + 1):
        host = IP_BASE + str(i)
        check_port_speed(host)

# start Script  C:\Users\gtobias\Desktop\Python>python .\AP-Status-Request.py