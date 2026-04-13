#Network Scan using Icmp packets
from scapy.all import *

def scan_network(network):
    print(f"Scanning network: {network}\n")
    
    ans,unans = sr(IP(dst=network)/ICMP(), timeout=2, verbose=0)
    
    active_hosts = []
    for snd, rcv in ans:
        print(f"[+] Host is alive: {rcv.src}")
        active_hosts.append(rcv.src)
    print(f"\nTotal Active Hosts: {len(active_hosts)}")
    return active_hosts


# CHANGE THIS BASED ON YOUR NETWORK
target_network = "192.168.1.0/24"

scan_network(target_network)