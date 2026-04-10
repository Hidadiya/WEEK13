import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_ipaddress = socket.gethostbyname(socket.gethostname())
client_socket.connect((my_ipaddress, 9999))

print("[CLIENT] Connected to server. Type 'help' for commands.")

while True:
    message = input("[CLIENT → SERVER] ")

    # Input validation
    if not message.strip():
        print("[CLIENT] Empty message blocked.")
        continue

    client_socket.send(message.encode())

    if message.lower() == "exit":
        break

    reply = client_socket.recv(4096).decode()
    print(f"[SERVER → CLIENT] {reply}")

client_socket.close()
print("[CLIENT] Disconnected.")