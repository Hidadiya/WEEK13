import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_ipaddress = socket.gethostbyname(socket.gethostname())
server_socket.bind((my_ipaddress, 9999))
server_socket.listen(1)

print("[SERVER] Started. Waiting for client...")

client_socket, client_address = server_socket.accept()
print(f"[SERVER] Client connected from {client_address}")

try:
    while True:
        data = client_socket.recv(4096)
        if not data:
            print("[SERVER] Client disconnected.")
            break

        message = data.decode()
        print(f"[CLIENT → SERVER] : {message}")

        # Handle exit
        if message.lower() == "exit":
            print("[SERVER] Client requested exit. Closing connection.")
            break

        # Input validation
        if len(message) > 500:
            reply = "Error: Message too long."
            client_socket.send(reply.encode())
            continue

        # Help menu
        if message.lower() == "help":
            reply = (
                "Available commands:\n"
                "  msg:<text>  - send a normal message\n"
                "  exit        - close the session\n"
            )
            client_socket.send(reply.encode())
            continue

        # Normal reply
        reply = input("[SERVER → CLIENT] Enter reply: ")
        client_socket.send(reply.encode())

        if reply.lower() == "exit":
            print("[SERVER] Server initiated exit.")
            break

finally:
    client_socket.close()
    server_socket.close()
    print("[SERVER] Closed.")