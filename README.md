# portscanner
Scan ports on either TCP or UDP. portscanner can be run entirely on the command-line or with a web interface. The output will be saved as an html file.

## Dependencies
bottle, scapy, and IPy.

## Instructions
The command-line usage is as follows:
```
usage: portscanner.py [-h] [--host HOST] [--ports PORTS] [--timeout TIMEOUT]
                      saveto

positional arguments:
  saveto             The name of the file to save the output (html) to.

optional arguments:
  -h, --help         show this help message and exit
  --host HOST        The IP address of the host. If not provided, a web
                     interface will be opened.
  --ports PORTS      The range of ports to be searched (inclusive). For
                     example: "--ports 5,10-1000". If not provided, a web
                     interface will be opened.
  --timeout TIMEOUT  The default timeout for each query. Defaults to 1
                     (second)
```

As the script uses the scapy library, it may not function properly unless run as root (the ability to open raw sockets is required).

## Examples
If I were to want to run it with the web interface, I would enter the following command:
```python3 portscanner.py savehere.html```

If I were to want to run it entirely on the command-line, I would enter a command such as the following:
```python3 portscanner.py savehere.html --host 167.99.109.5 --ports 25,80-90```
