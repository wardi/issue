#!/usr/bin/env python3

import io
import csv
import tarfile
import gzip
import urllib.parse
from datetime import datetime

t1 = tarfile.open('accessw1.log.gz.tar')
t2 = tarfile.open('accessw2.log.gz.tar')
t3 = tarfile.open('accessw3.log.gz.tar')
t4 = tarfile.open('accessw4.log.gz.tar')

w = csv.DictWriter(
    io.TextIOWrapper(gzip.GzipFile('logsw.csv.gz', 'w'), encoding="utf-8"),
    fieldnames=['ogpweb#', 'date', 'request', 'code', 'bytes', 'referrer', 'useragent', 'source', 'rt', 'urt'],
)
w.writeheader()

for ogpweb, t in enumerate((t1, t2, t3, t4), 1):
    for fn in t.getnames():
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
