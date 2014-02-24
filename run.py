#!/usr/bin/env python3
from time import sleep
import json
from queue import Queue
from threading import Thread
import random

def get(url, **kwargs):
    from get import get as _get
    return _get(url, cachedir = 'data', **kwargs)

catalogs = [
    'http://data.iledefrance.fr',
    'http://opendata.paris.fr.opendatasoft.com',
    'http://tourisme04.opendatasoft.com',
    'http://tourisme62.opendatasoft.com',
    'http://grandnancy.opendatasoft.com',
    'http://bistrotdepays.opendatasoft.com',
    'http://scisf.opendatasoft.com',
    'http://pod.opendatasoft.com',
    'http://dataratp.opendatasoft.com',
    'http://public.opendatasoft.com',
    'http://ressources.data.sncf.com',
]

def datasets(catalog):
    # Search an OpenDataSoft portal, and add things.
    # I chose OpenDataSoft because they care a lot about metadata.
    return json.loads(get(catalog + '/api/datasets/1.0/search?rows=1000000', load = True))['datasets']

def worker(queue):
    while not queue.empty():
        url = queue.get()
        try:
            get(url, load = False)
        except:
            queue.put(url)
            sleep(10)

def main(threads = 10, catalogs = catalogs):
    args = []
    for catalog in catalogs:
        for dataset in datasets(catalog):
            args.append((catalog, dataset['datasetid']))
    random.shuffle(args)
    queue = Queue()
    for a in args:
        queue.put('%s/explore/dataset/%s/download?format=csv' % a)
    for i in range(threads):
        Thread(target = worker, args = (queue,)).start()

if __name__ == '__main__':
    main()
