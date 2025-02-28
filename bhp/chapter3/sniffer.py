"""
A raw socket sniffer for UDP that takes a single packet
then quits. Supports both Windows and Unix
"""

import socket
import os

# Host to listen on
HOST = '129.21.73.57'

def main():
    #Create raw socken, bind to public interface
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))

    #Add IP header to capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)

    #Turn on promiscuous mode if on windows
    if os.name == 'nt':
        sniffer.ioctl(socket.SIORCVALL, socket.RCVALL_ON)

    # Read one packet

    print (sniffer.recvfrom(65565))

    #Turn off promiscuous mode if on windows

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == '__main__':
    main()
        