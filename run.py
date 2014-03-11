#!/usr/bin/env python3
from queue import Queue, Empty
from threading import Thread
import random
import logging

import featured_spreadsheets.download as download
import featured_spreadsheets.examine as examine

def manage(worker, n_threads = 10, catalogs = download.catalogs):
    'Manage a bunch of worker threads, and generate their results.'
    # Download in random order
    args = []
    for catalog in catalogs:
        for dataset in download.datasets(catalog):
            args.append((catalog, dataset))
    random.shuffle(args)

    read_queue = Queue()
    for a in args:
        read_queue.put(a)

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
    logger = logging.getLogger('featured-spreadsheets')
    logger.setLevel(logging.DEBUG)

    h1 = logging.FileHandler(os.path.join(directory, "featured-spreadsheets.log"),"w")
    h1.setLevel(logging.DEBUG)
    logger.addHandler(h1)

    h2 = logging.StreamHandler()
    h2.setLevel(logging.ERROR)
    logger.addHandler(h2)

    for dataset in manage(examine.worker):
        print(dataset['primary_keys'])

if __name__ == '__main__':
    main()
