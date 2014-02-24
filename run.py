#!/usr/bin/env python3
from queue import Queue
from threading import Thread
import random

import download

def manage(worker, threads = 10, catalogs = download.catalogs):
    # Download
    args = []
    for catalog in catalogs:
        for dataset in download.datasets(catalog):
            args.append((catalog, dataset))
    random.shuffle(args)
    queue = Queue()
    for a in args:
        queue.put(args)
    for i in range(threads):
        Thread(target = worker, args = (queue,)).start()

if __name__ == '__main__':
#   manage(download.worker)
    manage(examine.worker)
