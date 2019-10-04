from scapy.all import *
import sys

class Scanner:
    @staticmethod
    def udp_scan1(host, port, timeout):
        port = int(port)
        sport = RandShort()
        resp = sr1(IP(dst=host)/UDP(dport=port),timeout=timeout, verbose=False)
        if resp is not None:
            print(host, port, 'UDP', 'Open', file=sys.stderr)
            return "Open"
        else:
            print(host, port, 'UDP', 'Timeout', file=sys.stderr)
            return "Timeout"

    @staticmethod
    def tcp_scan1(host, port, timeout):
        port = int(port)
        sport = RandShort()
        resp = sr1(IP(dst=host)/TCP(sport=sport,dport=port,flags="S"),timeout=timeout, verbose=False)
        if resp is None:
            print(host, port, 'TCP', 'Timeout', file=sys.stderr)
            return 'Timeout'
        if(resp.getlayer(TCP).flags == 0x12): # 0x12 SYN-ACK
            # Reset the connection
            send(IP(dst=host)/TCP(sport=sport,dport=port,flags="AR"), verbose=False)
            print(host, port, 'TCP', 'Open', file=sys.stderr)
            return 'Open'
        else:
            print(host, port, 'TCP', 'Closed', file=sys.stderr)
            return f'Closed ({resp.getlayer(TCP).flags})'

    @staticmethod
    def scan1(host, port, protocol, timeout):
        if protocol == 'TCP':
            return Scanner.tcp_scan1(host, port, timeout)
        else:
            return Scanner.udp_scan1(host, port, timeout)