#!/usr/bin/env python3
from queue import Queue
from threading import Thread
import random

import download

def main(threads = 10, catalogs = download.catalogs):
    # Download
    args = []
    for catalog in catalogs:
        for dataset in download.datasets(catalog):
            args.append((catalog, dataset['datasetid']))
    random.shuffle(args)
    queue = Queue()
    for a in args:
        queue.put('%s/explore/dataset/%s/download?format=csv' % a)
    for i in range(threads):
        Thread(target = download.worker, args = (queue,)).start()

    # Wait for that to finish
    while not queue.empty():
        pass

    # Do stuff

if __name__ == '__main__':
    main()
