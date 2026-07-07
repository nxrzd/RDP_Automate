#!/usr/bin/env python3

import re
import subprocess

PORT = "3389"
TIMEOUT = "2"


def get_ips():
    """Prompt the user to choose how they want to enter IP addresses."""

    while True:
        print("\nHow would you like to enter IP addresses?")
        print("1. Comma-separated list")
        print("2. Paste a list (one per line or mixed text)")
        choice = input("\nEnter your choice (1 or 2): ").strip()

        if choice == "1":
            ip_input = input("\nEnter IPs separated by commas: ").strip()
            ips = [ip.strip() for ip in ip_input.split(",") if ip.strip()]
            return ips

        elif choice == "2":
            print("\nPaste your IP list below.")
            print("Press Enter on a blank line when finished.\n")

            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            text = "\n".join(lines)

            # Extract IPv4 addresses from any pasted text
            ips = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)

            if not ips:
                print("\nNo IP addresses were found. Please try again.")
                continue

            return ips

        else:
            print("\nInvalid selection. Please enter 1 or 2.\n")


def main():
    all_ips = get_ips()

    print("\nThe following IPs will be checked:")
    for ip in all_ips:
        print(f"  - {ip}")

    print()

    for ip in all_ips:
        print(f"Checking {ip}...")

        test = subprocess.run(
            ["nc", "-vz", "-w", TIMEOUT, ip, PORT],
            capture_output=True,
            text=True,
        )

        if test.returncode != 0:
            print(f"  {ip}: {test.stderr.strip()}")
            continue

        print(f"  {ip}: OPEN")
        print(f"Launching RDP to {ip}...")

        # Launch Remote Desktop
        proc = subprocess.Popen([
            "cmd.exe",
            "/c",
            "start",
            "/wait",
            "mstsc",
            f"/v:{ip}",
        ])

        # Wait until the RDP session is closed
        proc.wait()

        print(f"Closed session for {ip}\n")

    print("Finished.")


if __name__ == "__main__":
    main()
