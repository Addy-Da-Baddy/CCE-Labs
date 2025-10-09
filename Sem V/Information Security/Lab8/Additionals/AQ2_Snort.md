
# Configuring and Using Snort as a Network Intrusion Detection System (NIDS)

## Introduction

Snort is an open-source network intrusion detection system capable of performing real-time traffic analysis and packet logging. This document outlines the steps to install, configure, and operate Snort to monitor network traffic, apply detection rules, and analyze logs to identify potential intrusions.

---

## 1. Installation of Snort

### On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install snort
````

During installation, specify the network interface and home network IP range as prompted.

### On CentOS/Red Hat:

```bash
sudo yum install epel-release
sudo yum install snort
```

---

## 2. Configuring Snort

### 2.1. Network Interface Setup

Identify the network interface you want to monitor:

```bash
ip a
```

Example interface: `eth0`

### 2.2. Configure Snort Variables

Edit the Snort configuration file `/etc/snort/snort.conf`:

* Set the HOME_NET variable to your network range, e.g.:

```conf
var HOME_NET 192.168.1.0/24
```

* Verify or set the network interface to listen on in Snort startup or service files.

### 2.3. Include Snort Rules

Snort uses rules to detect suspicious activity. Ensure rules are included in `snort.conf`, e.g.:

```conf
include $RULE_PATH/local.rules
include $RULE_PATH/community.rules
```

---

## 3. Writing Snort Rules

Snort rules define patterns and actions. A simple example rule to detect ICMP echo requests (pings):

```conf
alert icmp any any -> $HOME_NET any (msg:"ICMP Echo Request Detected"; sid:1000001; rev:1;)
```

Add custom rules to the local rules file (e.g., `/etc/snort/rules/local.rules`).

---

## 4. Running Snort for Real-Time Monitoring

To run Snort in NIDS mode and monitor real-time traffic:

```bash
sudo snort -A console -q -c /etc/snort/snort.conf -i eth0
```

Flags:

* `-A console` : Alerts displayed on console
* `-q` : Quiet output except alerts
* `-c` : Configuration file path
* `-i` : Network interface

---

## 5. Capturing Network Traffic

Snort passively monitors traffic on the specified interface without affecting traffic flow.

Alternatively, use tcpdump to capture traffic for offline analysis:

```bash
sudo tcpdump -i eth0 -w capture.pcap
```

Snort can analyze capture files with:

```bash
sudo snort -c /etc/snort/snort.conf -r capture.pcap
```

---

## 6. Analyzing Snort Logs

Snort logs alerts and packet captures for further inspection.

### 6.1. Default Log Location

Alerts and logs are typically stored in `/var/log/snort/`.

Example alert file: `/var/log/snort/alert`

### 6.2. Log Analysis

Review the alert file:

```bash
sudo tail -f /var/log/snort/alert
```

Sample alert entry:

```
[**] [1:1000001:1] ICMP Echo Request Detected [**]
[Priority: 3] 
03/10-10:15:32.123456 192.168.1.5 -> 192.168.1.10 ICMP TTL:64 TOS:0x0 ID:54321 IpLen:20 DgmLen:28
Type:8  Code:0  ID:12345   Seq:1  ECHO
```

---

## 7. Identifying Potential Intrusions

By monitoring Snort alerts, you can detect:

* Port scans
* Suspicious protocol usage
* Known exploits and malware signatures
* Unauthorized access attempts

Custom rules can be tailored to monitor specific threats in your environment.

