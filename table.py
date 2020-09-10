#!/usr/bin/env python3

import sys
import csv
import tarfile
import gzip

t1 = tarfile.open('access01.log.gz.tar')
t2 = tarfile.open('access02.log.gz.tar')
t3 = tarfile.open('access03.log.gz.tar')
t4 = tarfile.open('access04.log.gz.tar')

names = [
    'access.log-20200904.gz',
    'access.log-20200905.gz',
    'access.log-20200906.gz',
    'access.log-20200907.gz',
    'access.log-20200908.gz',
    'access.log-20200909.gz',
    'access.log-20200910.gz',
]

w = csv.DictWriter(
    sys.stdout,
    fieldnames=['ogpweb#', 'date', 'request', 'code', 'bytes', 'referrer', 'useragent', 'source', 'rt', 'urt'],
)
w.writeheader()

for ogpweb, t in enumerate((t1, t2, t3, t4), 1):
    for fn in names:
        g = gzip.GzipFile(fileobj=t.extractfile(fn))
        for row in g:
            _, rest = row.decode('utf-8').split('[', 1)
            dt, rest = rest.split('] "', 1)
            request, rest = rest.split('" ', 1)
            code, rest = rest.split(' ', 1)
            bts, rest = rest.split(' "', 1)
            dash, rest = rest.split('" "', 1)
            useragent, rest = rest.split('" "', 1)
            source, rest = rest.split('" rt=', 1)
            rt, rest = rest.split(' urt="', 1)
            urt, rest = rest.split('"')

            w.writerow({
                'ogpweb#': ogpweb,
                'date': dt,
                'request': request,
                'code': code,
                'bytes': bts,
                'dash': dash,
                'useragent': useragent,
                'source': source,
                'rt': rt,
                'urt': urt,
            })
