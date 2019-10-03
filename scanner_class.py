from scapy.all import *

class Scanner:
    @staticmethod
    def udp_scan(hosts, ports):
        ports = [int(p) for p in ports]
        # ans, unans = sr( IP(dst=hosts)/UDP(dport=ports),timeout=1, verbose=False) # Adapted from scapy documentation: https://scapy.readthedocs.io/en/latest/usage.html#udp-ping
        res, unans = sr( IP(dst=hosts)/UDP(dport=ports), timeout=1, verbose=False) # Adapted from scapy documentation: https://scapy.readthedocs.io/en/latest/usage.html#tcp-port-scanning
        return res, unans
            
    @staticmethod
    def tcp_scan(hosts, ports):
        ports = [int(p) for p in ports]
        res, unans = sr( IP(dst=hosts)/TCP(flags="S", dport=ports), timeout=1, verbose=False) # Adapted from scapy documentation: https://scapy.readthedocs.io/en/latest/usage.html#tcp-port-scanning
        return res,unans