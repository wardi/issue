#!/usr/bin/env python3

import io
import csv
import tarfile
import gzip
import urllib.parse
from datetime import datetime

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
    io.TextIOWrapper(gzip.GzipFile('logs.csv.gz', 'w'), encoding="utf-8"),
    fieldnames=['ogpweb#', 'date', 'request', 'code', 'bytes', 'referrer', 'useragent', 'source', 'rt', 'urt'],
)
w.writeheader()

for ogpweb, t in enumerate((t1, t2, t3, t4), 1):
    for fn in names:
        g = gzip.GzipFile(fileobj=t.extractfile(fn))
        for row in g:
            _, rest = row.decode('utf-8').split('[', 1)
            dt, rest = rest.split(' +0000] "', 1)
            request, rest = rest.split('" ', 1)
            code, rest = rest.split(' ', 1)
            bts, rest = rest.split(' "', 1)
            referrer, rest = rest.split('" "', 1)
            useragent, rest = rest.split('" "', 1)
            source, rest = rest.split('" rt=', 1)
            rt, rest = rest.split(' urt="', 1)
            urt, rest = rest.split('"')

            w.writerow({
                'ogpweb#': ogpweb,
                'date': datetime.strptime(dt, '%d/%b/%Y:%H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S'),
                'request': urllib.parse.unquote(request),
                'code': code,
                'bytes': bts,
                'referrer': referrer,
                'useragent': useragent,
                'source': source,
                'rt': rt,
                'urt': '' if urt == '-' else urt,
            })
