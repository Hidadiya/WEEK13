#Network Scan using ARP packets
from scapy.all import *

def arp_scan(network):
    print(f"Scanning network using ARP: {network}\n")

    ans, _ = srp(
        Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network),
        timeout=2,
        verbose=0
    )

    active_hosts = []

    for sent, received in ans:
        print(f"[+] IP: {received.psrc}   MAC: {received.hwsrc}")
        active_hosts.append(received.psrc)

    print(f"\nTotal Active Hosts: {len(active_hosts)}")
    return active_hosts


# CHANGE THIS
target_network = "192.168.1.0/24"

arp_scan(target_network)