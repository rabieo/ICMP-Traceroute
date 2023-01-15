# Network Diagnostics Scripts
This repository contains two Python scripts that allow you to perform network diagnostics tasks:

## ping.py
This script allows you to ping a host and measure the round trip time (RTT) of the packets. The script uses the ICMP protocol to send echo request packets to the host and measure the time it takes for the host to respond. The script also prints out the time it takes for each packet to reach the host and return.

## traceroute.py
This script allows you to trace the route a packet takes from your machine to the destination host. The script uses the ICMP protocol to send echo request packets with increasing Time-To-Live (TTL) values. Each router along the path will decrement the TTL by 1 and when it reaches 0 it will send an ICMP Time Exceeded message back to the source. The script will print out the IP address of each router along the path, as well as the round trip time (RTT) for the packet to reach that router.

## Requirements
python 3.x
root permission if running on linux
## Usage

```
python3 ping.py hostname
python3 traceroute.py hostname
```
## Example

```
python3 ping.py google.com
python3 traceroute.py google.com
```

Note: The script may require root permission to run on Linux as it uses raw sockets.

## Limitations
The script may not work properly on some networks which block ICMP packets.
The script may not work properly on some hosts that do not respond to ICMP echo request packets.
The script may not work properly on some hosts that respond to ICMP echo request packets with a different protocol.
It is not a good idea to use this code for any kind of production use, it is for demonstration and educational purposes only.
