#!/usr/bin/python3

# By Alden Hilton
# For usage, run python3 portscanner.py -h

from bottle import route, run, template, static_file, request, get, response, redirect
from scanner_class import Scanner
from threading import Thread
from htmlTable import Table
from scapy.all import *
from time import sleep
import webbrowser
import argparse
import json
import IPy
import sys

# Set up command-line instructions
parser = argparse.ArgumentParser()
parser.add_argument('saveto', help='The name of the file to save the output (html) to.')
parser.add_argument('--host', help='The IP address of the host. If not provided, a web interface will be opened.', default='')
parser.add_argument('--ports', help='The range of ports to be searched (inclusive). For example: "--ports 5,10-1000". If not provided, a web interface will be opened.', default='')
parser.add_argument('--timeout', help='The default timeout for each query. Defaults to 1 (second)', default=1, type=int)
args = parser.parse_args()

# Open file used for output
output = open(args.saveto, 'w')

# Global variables
scans = []
alerts = []
progress = 0
started = False
finished = False

# Top 100 ports according to nmap
tcpDefaults = [7,9,13,21,22,23,25,26,37,53,79,80,81,88,106,110,111,113,119,135,139,143,144,179,199,389,427,443,444,445,465,513,514,515,543,544,548,554,587,631,646,873,990,993,995,1025,1026,1027,1028,1029,1110,1433,1720,1723,1755,1900,2000,2001,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,6000,6001,6646,7070,8000,8008,8009,8080,8081,8443,8888,9100,9999,10000,32768,49152,49153,49154,49155,49156,49157]
udpDefaults = [7,9,17,19,49,53,67,68,69,80,88,111,120,123,135,136,137,138,139,158,161,162,177,427,443,445,497,500,514,515,518,520,593,623,626,631,996,997,998,999,1022,1023,1025,1026,1027,1028,1029,1030,1433,1434,1645,1646,1701,1718,1719,1812,1813,1900,2000,2048,2049,2222,2223,3283,3456,3703,4444,4500,5000,5060,5353,5632,9200,10000,17185,20031,30718,31337,32768,32769,32771,32815,33281,49152,49153,49154,49156,49181,49182,49185,49186,49188,49190,49191,49192,49193,49194,49200,49201,65024]

# Convert "1-5,10, 12" into [1,2,3,4,5,10,12]
def parsePorts(ports):
    l = []
    ports = "".join(ports.split())

    rnges = ports.split(',')
    for r in rnges:
        if '-' in r:
            start, stop = r.split('-')
            for p in range(int(start), int(stop) + 1):
                l.append(str(p))
        else:
            l.append(r)
    return list(dict.fromkeys(l))

@route('/')
def index():
    global alerts
    tempAlerts = alerts.copy()
    alerts = []
    total = 0
    for scan in scans:
        total += len(scan['hosts']) * len(scan['ports'])
    return template('web_files/index', hosts=scans, alerts=tempAlerts, total=total, started=started, saveto=args.saveto, timeout=args.timeout)

@route('/add_host')
def add_host():
    if started:
        alerts.append("The scan has already started. To restart or terminate the scan, terminate the python script.")
        return redirect("/")
    # Read GET request
    host = request.query.host
    ports = request.query.ports
    protocol = request.query.protocol

    # Parse the hosts field
    try:
        hosts = [str(ip) for ip in IPy.IP(host)]
    except:
        alerts.append("Invalid IP prefix " + host)
        return redirect("/")
    hostStr = host

    # Parse the ports field
    if ports == '':
        ports = udpDefaults if protocol == 'UDP' else tcpDefaults
    else:
        try:
            ports = parsePorts(ports)
        except:
            alerts.append("Malformed port specification " + ports)
            return redirect("/")
    if len(ports) > 10:
        portsStr = ', '.join([str(p) for p in ports[:7]]) + ', ..., ' + ', '.join([str(p) for p in ports[-1:]])
    else:
        portsStr = ', '.join([str(p) for p in ports])

    # Add data to model and reload
    scans.append({'hosts': hosts, 'hostStr': hostStr, 'ports':ports, 'portsStr': portsStr, 'protocol': protocol})
    return redirect("/")

@route('/delete_host')
def delete_host():
    if started:
        alerts.append("The scan has already started. To restart or terminate the scan, terminate the python script.")
        return redirect("/")
    host = request.query.hostNum
    del scans[int(host)]
    return redirect("/")

@route('/start')
def start():
    global started
    if started:
        alerts.append("The scan has already started. To restart or terminate the scan, terminate the python script.")
        return redirect("/")
    nthreads = request.query.nthreads
    started = True
    Thread(target = runScan).start()
    return redirect("/")

def runScan():
    global progress, finished
    header = f'<!DOCTYPE HTML><html><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width" /><link rel="icon" href="favicon.png"><title>Scan Results</title>{style}</head>'
    output.write(header)

    for scan in scans:
        table = Table()
        table.title = scan['hostStr'] + " (" + scan['protocol'] + ")"
        table.setHeader(scan['hosts'])
        for host in scan['hosts']:
            for port in scan['ports']:
                table.addEntry(port, Scanner.scan1(host, port, scan['protocol'], args.timeout))
                progress += 1
        output.write(str(table))
    output.write("</body>")
    finished = True
    output.close()
    print('Done. Output saved to', args.saveto, file=sys.stderr)

# Handle so that the javascript can update the progress bar.
@route('/progress')
def get_progress():
    response.content_type = 'application/json'
    if not finished:
        total = 0
        for scan in scans:
            total += len(scan['hosts']) * len(scan['ports'])
        if total != 0:
            return json.dumps({'progress': progress*100//total})
        else:
            return 0
    else:
        return json.dumps({'progress': 'DONE'})

# Default file handler
@route('/:filename#.*#')
def serve_frontend(filename):
    if filename == args.saveto:
        return static_file(filename, os.getcwd())
    else:
        return static_file(filename, os.getcwd() + "/web_files/")

if __name__ == "__main__":
    with open('web_files/main.css', 'r') as f:
        style = "<style>" + f.read() + "</style>"
    if args.host == '' or args.ports == '':
        print('Program is listening on http://localhost:8088.',file=sys.stderr)
        run(host='localhost', port=8088, quiet=True)
    else:
        ports = parsePorts(args.ports)
        scans.append({'hosts': [args.host], 'hostStr': args.host, 'ports': ports, 'protocol': 'TCP'})
        runScan()
