#!/usr/bin/env python3

import io
import csv
import tarfile
import gzip
import urllib.parse
from datetime import datetime

g1 = 'access01-20200917.gz'
g2 = 'access02-20200917.gz'
g3 = 'access03-20200917.gz'
g4 = 'access04-20200917.gz'

w = csv.DictWriter(
    io.TextIOWrapper(gzip.GzipFile('logs2.csv.gz', 'w'), encoding="utf-8"),
    fieldnames=['ogpweb#', 'date', 'request', 'code', 'bytes', 'referrer', 'useragent', 'source', 'rt', 'urt'],
)
w.writeheader()

for ogpweb, f in enumerate((g1, g2, g3, g4), 1):
    g = gzip.GzipFile(f)
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
