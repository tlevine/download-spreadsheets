#!/usr/bin/env python3
from queue import Queue, Empty
from threading import Thread
import random

import download, examine

def manage(worker, n_threads = 10, catalogs = download.catalogs):
    'Manage a bunch of worker threads.'
    # Download in random order
    args = []
    for catalog in catalogs:
        for dataset in download.datasets(catalog):
            args.append((catalog, dataset))
    random.shuffle(args)

    read_queue = Queue()
    for a in args:
        read_queue.put(args)

    write_queue = Queue()
    threads = []
    for i in range(n_threads):
        threads.append(Thread(target = worker, args = (read_queue,write_queue)))
        threads[-1].start()

    while not (read_queue.empty() and write_queue.empty() and set(t.is_alive() for t in threads) == {False}):
        try:
            x = write_queue.get_nowait()
        except Empty:
            pass
        else:
            yield x

def main_download():
    'Run a download and exit.'
    for _ in manage(download.worker):
        pass

def main():
    datasets = manage(examine.worker)

if __name__ == '__main__':
    main()
