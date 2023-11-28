#!/usr/bin/env python3

"""
------------------------------------------------------------------------------------------------------------------------
nllookup.py - Names Local Lookup - resolve names/IPs using OS resolving routines (do not make direct requests to DNS)
------------------------------------------------------------------------------------------------------------------------

Copyright (c) 2023 Mikhail Zakharov <zmey20000@yahoo.com>

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
   disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

-- CHANGELOG -----------------------------------------------------------------------------------------------------------
2023.11.28  v1.0    Initial release
------------------------------------------------------------------------------------------------------------------------
"""

import socket
import sys


def usage(e):
    print(f'Usage:\n  {sys.argv[0]} IP-address\t- Get a hostname by IPv4 or IPv6 address')
    print(f'  {sys.argv[0]} [-a] host\t\t- Get one or (-a)ll IPv4/6 addresses by a host')
    print(f'  {sys.argv[0]} -s host | IP\t- Get a pair: a host and the 1-st IPv4/6-address')
    sys.exit(e)


IP = True
sflg = False
host = ''
argc = len(sys.argv)

if argc == 1:
    usage(0)
elif argc == 2:
    host = sys.argv[1]
elif argc == 3 and '-a' in sys.argv and '-s' not in sys.argv:
    host = sys.argv[argc - sys.argv.index('-a')]
elif argc == 3 and '-s' in sys.argv and '-a' not in sys.argv:
    host = sys.argv[argc - sys.argv.index('-s')]
    sflg = True
else:
    usage(2)

if sflg:
    # Shortcut form to get the host and the first IP
    try:
        print(socket.gethostbyaddr(host)[0], socket.gethostbyaddr(host)[2][0])
    except (socket.error, ValueError, OSError):
        print(f'Host {host} not found')
        exit(1)

    exit(0)

# Validate address: IP
try:
    socket.inet_pton(socket.AF_INET, host)
except (socket.error, ValueError, OSError):
    try:
        socket.inet_pton(socket.AF_INET6, host)
    except (socket.error, ValueError, OSError):
        IP = False

if not IP:
    # hostname -> IP
    addrs_4 = []
    addrs_6 = []
    addrs_x = []

    try:
        addrs = [[a[0].value, a[4][0]] for a in socket.getaddrinfo(host, None)]
    except:
        print(f'Host {host} not found')
        exit(1)

    for addr in addrs:
        if addr[0] == socket.AF_INET:
            addrs_4.append(addr[1])
        elif addr[0] == socket.AF_INET6:
            addrs_6.append(addr[1])
        else:
            addrs_x.append(addr[1])

    for addr in [a for a in list(dict.fromkeys(addrs_4 + addrs_6 + addrs_x))]:
        print(addr)
        if argc == 2:
            break

else:
    # IP -> hostname
    try:
        print(socket.gethostbyaddr(host)[0] if socket.gethostbyaddr(host)[0] else '\n'.join(socket.gethostbyaddr(host)[2]))
    except (socket.error, ValueError, OSError):
        print(f'Host {host} not found')
        exit(1)
