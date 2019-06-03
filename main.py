# cross py2/py3 compatible version
try: import queue
except ImportError: import Queue as queue
import fileinput
import threading
import time

class TaskQueue(object):

    def __init__(self):
        self._income_queue = queue.Queue()

    def get(self):
        while True: 
            yield self._income_queue.get()

    def put(self, message):
        self._income_queue.put(message)
        return 0

    def finalize(self):
        self._income_queue.task_done()
        

class TaskProvider(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
        print("= INIT threadName={}".format(self.name))

    def run(self):
        for line in fileinput.input():
            self._queue.put(line.strip())


class TaskWorker(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
        print("= INIT threadName={}".format(self.name))

    def run(self):
        for message in self._queue.get():
            if not message:
                continue
            print("-> START  threadName={}, message={}".format(self.name, message))
            time.sleep(3)
            print("<- FINISH threadName={}".format(self.name))
            self._queue.finalize()


def main():

    queue = TaskQueue()

    for _ in range(10):
        worker = TaskWorker(queue)
        worker.setDaemon(True)
        worker.start()

    provider = TaskProvider(queue) 
    provider.start()
    provider.join()


if __name__ == '__main__':
    main()
