#!/usr/bin/env python3

import subprocess

list_of_ips = str(input("Enter a list of IPs as comma separated values: "))
print(list_of_ips)
all_ips = list_of_ips.split(",")
print(all_ips)


for ip in list_of_ips:
    octets = ip.split(".")
    all_ips.append(octets)

split_ips = []
#for ip in list_of_ips:

PORT = "3389"
TIMEOUT = "2"

for ip in all_ips:
    print(f"Checking {ip}...")

    test = subprocess.run(
        ["nc", "-vz", "-w", TIMEOUT, ip, PORT],
        capture_output=True,
        encoding="utf-8",
        text=True,
    )

    if test.returncode != 0:
        print(f"{ip}: {test.stderr.strip()}")
        continue

    print(f"  {ip}: OPEN")
    print(f"Launching RDP to {ip}...")

    # opens rdp session
    proc = subprocess.Popen([
        "cmd.exe",
        "/c",
        "start",
        "/wait",
        "mstsc",
        f"/v:{ip}",
    ])

    # wait for rdp session close
    proc.wait()

    print(f"Closed session for {ip}\n")

print("Finished.")
