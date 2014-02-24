#!/usr/bin/env python3
from queue import Queue
from threading import Thread
import random

import download, examine

def manage(worker, threads = 10, catalogs = download.catalogs):
    # Download
    args = []
    for catalog in catalogs:
        for dataset in download.datasets(catalog):
            args.append((catalog, dataset))
    random.shuffle(args)

    read_queue = Queue()
    for a in args:
        read_queue.put(args)

    write_queue = Queue()
    for i in range(threads):
        Thread(target = worker, args = (read_queue,write_queue)).start()
    while not read_queue.empty():
        pass

    return write_queue

def main():
#   manage(download.worker)
    datasets = manage(examine.worker)
    while not datasets.empty():
        print(datasets.get())

if __name__ == '__main__':
    main()
