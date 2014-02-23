#!/usr/bin/env python3
from queue import Queue
from threading import Thread

from get import get

def datasets():
    # Search an OpenDataSoft portal, and add things.
    # I chose OpenDataSoft because they care a lot about metadata.
    get(blah blah)
    read json
    return metadata

def worker(queue):
    while not queue.empty():
        url = queue.get()
        get(url)

def main(threads = 50):
    queue = Queue()
    for dataset in datasets():
        queue.put(dataset url)
    for i in range(threads):
        Thread(target = worker, args = (queue,)).start()
