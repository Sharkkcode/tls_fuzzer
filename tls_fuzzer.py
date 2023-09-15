import socket
import ssl
import datetime
import random
import string

# Target's address and port
target_ip = "<target_ip>"
target_port = 443

for i in range(100005):

    print("\n" + "-" * 60 + "\n")

    print("Test case:", i+1, ", Test time:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the target
        client_socket.connect((target_ip, target_port))

        # Create a TLS connection on the socket
        tls_context = ssl.create_default_context()
        tls_context.check_hostname = False
        tls_context.verify_mode = ssl.CERT_NONE
        tls_socket = tls_context.wrap_socket(client_socket, server_hostname=target_ip)

        # Send fuzzing message
        message_length = random.randint(1, 200)
        message = bytes([random.randint(0, 255) for _ in range(message_length)])
        print()
        print("MESSAGE IN HEX:")
        print(' '.join([hex(x) for x in message]))
        print()
        tls_socket.send(message)

        # Receive response data
        response = tls_socket.recv(1024)
        print("Received response:", response.decode())

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the connection
        if "tls_socket" in locals():
            tls_socket.close()

