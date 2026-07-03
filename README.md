# RDP Initiator

## Overview

This script automates checking a list of IP addresses for an open RDP service (TCP port 3389). If the port is open, it launches a Remote Desktop session to that machine.

Instead of hard-coding IP addresses into the script, the user can provide them at runtime as a comma-separated list.

---

## Features

* Accepts user input as a comma-separated list of IPv4 addresses.
* Iterates through each IP individually.
* Uses **Netcat (`nc`)** to test whether TCP port **3389** is reachable.
* Skips hosts that are unreachable or have closed ports.
* Automatically launches Microsoft Remote Desktop (`mstsc`) for reachable hosts.
* Waits for the RDP session to close before moving on to the next host.

---

## Requirements

### Windows

* Python 3
* Microsoft Remote Desktop (`mstsc.exe`)
* A Windows-compatible version of Netcat (or Ncat)

### WSL / Linux

* Python 3
* Netcat installed

Example:

```bash
sudo apt update
sudo apt install netcat
```

---

## Usage

Run the script:

```bash
python3 rdp_initiator.py
```

When prompted, enter IP addresses as a comma-separated list.

Example:

```text
Enter a list of IPs as comma separated values:
129.100.43.171,129.100.42.245,172.30.247.83
```

The script will then:

1. Split the input into individual IP addresses.
2. Test each address on TCP port 3389.
3. Report whether the host is reachable.
4. Launch an RDP session if the port is open.
5. Continue until every IP has been processed.

---

## How It Works

### 1. User Input

The user enters one line containing multiple IP addresses.

Example:

```text
129.100.43.171,129.100.42.245,172.30.247.83
```

The input is split into a Python list using:

```python
split(",")
```

---

### 2. Connectivity Check

Each IP is tested using Netcat:

```text
nc -vz -w 2 <ip> 3389
```

If the connection succeeds, the script proceeds to launch Remote Desktop.

If the connection fails or times out, the script reports the error and continues with the next address.

---

### 3. Launching Remote Desktop

For hosts with an open RDP port, the script starts:

```text
mstsc /v:<ip>
```

The script waits for the RDP session to close before moving on to the next host.

---

## Known Limitations

* User input currently assumes valid IPv4 addresses.
* Extra spaces after commas are preserved unless they are removed before processing.
* The script is designed for Windows Remote Desktop (`mstsc`).
* Netcat (`nc`) must be installed and accessible from the command line.
* No IP address validation is currently performed.

---

## Future Improvements

* Remove leading/trailing whitespace from user input.
* Validate IPv4 address format before testing.
* Store parsed octets for subnet analysis.
* Replace the external Netcat dependency with Python sockets.
* Improve error handling and logging.
* Support reading IP addresses from a text file.
* Add support for concurrent port checks to improve performance.

---

## Purpose

This project was created to practice:

* Python lists
* String manipulation
* User input
* Splitting strings into usable data
* Iteration with `for` loops
* Using `subprocess`
* Basic network automation
* Automating repetitive RDP connection workflows
