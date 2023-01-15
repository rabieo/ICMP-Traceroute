from socket import *
import os
import sys
import struct
import time
import select
import argparse

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 2

# This code is a python implementation of the traceroute command which is
# a network troubleshooting tool that can be used to track the route that
# a packet takes from the source to the destination.

def checksum(data: bytes) -> int:
    """
    This function calculates the checksum of the input string.
    
    Parameters:
        string (str): The input string to calculate the checksum for.
    
    Returns:
        int: The calculated checksum.
    """
    csum = 0
    for i in range(0, len(data), 2):
        csum += int.from_bytes(data[i:i+2], 'big')
    csum = (csum >> 16) + (csum & 0xffff)
    csum += csum >> 16
    return ~csum & 0xffff


def build_packet() -> bytes:
    """
    This function builds an ICMP Echo Request packet.
    
    Returns:
        bytes: The constructed packet.
    """
    myChecksum = 0
    myID = os.getpid() & 0xFFFF
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)
    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, myID, 1)
    packet = header + data
    return packet


def get_route(hostname: str) -> None:
    """
    This function traces the route to the specified hostname.
    
    Parameters:
        hostname (str): The hostname to trace the route to.
    
    Returns:
        None
    """
    timeLeft = TIMEOUT
    for ttl in range(1, MAX_HOPS):
        for tries in range(TRIES):
            destAddr = gethostbyname(hostname)
            icmp = getprotobyname("icmp")
            mySocket = socket(AF_INET, SOCK_RAW, icmp)
            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []:
                    print(" * * * Request timed out.")
                recvPacket, addr = mySocket.recvfrom(1024)
                timeReceived = time.time()
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    print(" * * * Request timed out.")

            except timeout:
                continue

            else:
                icmpHeader = recvPacket[20:21]
                types = struct.unpack("b", icmpHeader)[0]
                try:
                    host = gethostbyaddr(addr[0])[0]
                except:
                    host = " "
                if types == 11:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(
                        f" {ttl} rtt={(timeReceived -t)*1000:.2f}ms {addr[0]} {host}")
                elif types == 3:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(
                        f" {ttl} rtt={(timeReceived -t)*1000:.2f}ms {addr[0]} {host}")
                elif types == 0:
                    bytes = struct.calcsize("d")
                    timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    print(
                        f" {ttl} rtt={(timeReceived - timeSent)*1000:.2f}ms {addr[0]} {host}")
                    return
                else:
                    print("error")
                break
            finally:
                mySocket.close()


parser = argparse.ArgumentParser(description='Trace route')
parser.add_argument('hostname', type=str, help='The destination hostname')
args = parser.parse_args()
hostname = args.hostname
get_route(hostname)
