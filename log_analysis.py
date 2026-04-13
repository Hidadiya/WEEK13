import re
from collections import defaultdict

log_file = "network_logs.txt"

failed_logins = defaultdict(int)
success_logins = defaultdict(int)
web_requests = defaultdict(int)
port_scans = defaultdict(list)

with open(log_file, "r") as file:
    for line in file:

        # Extract IP
        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
        ip = ip_match.group(0) if ip_match else None

        # SSH Failed
        if "Failed password" in line:
            failed_logins[ip] += 1

        # SSH Success
        elif "Accepted password" in line:
            success_logins[ip] += 1

        # Nginx Requests
        elif "nginx" in line:
            url_match = re.search(r'\"(GET|POST) (.*?) HTTP', line)
            if url_match:
                url = url_match.group(2)
                web_requests[url] += 1

        # Port Scan
        elif "DPT=" in line:
            port_match = re.search(r'DPT=(\d+)', line)
            if port_match:
                port_scans[ip].append(port_match.group(1))


# OUTPUT

print(" Failed Login Attempts:")
for ip, count in failed_logins.items():
    print(ip, "->", count)

print(" Successful Logins:")
for ip, count in success_logins.items():
    print(ip, "->", count)

print(" Web Requests:")
for url, count in web_requests.items():
    print(url, "->", count)

print(" Port Scanning Activity:")
for ip, ports in port_scans.items():
    print(ip, "->", ports)

print(" Suspicious IPs (Failed attempts > 5):")
for ip, count in failed_logins.items():
    if count > 5:
        print(ip, "-> Possible brute-force attack!")