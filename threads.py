from threading import Thread
from queue import Queue, Empty
from data import Reader

class ReadThread(Thread):
    def __init__(self, reader: Reader, queue: Queue, **kwargs):
        self.reader = reader
        self.queue = queue
        super(ReadThread, self).__init__(target=self.read_func, **kwargs)
        self.target = self.read_func
        self.stopped = False
        
    def read_func(self) -> None:
        result = self.reader.read()
        if result:
            self.queue.put(result)
            return
    
    def run(self) -> None:
        while not(self.stopped):
            self.target()
    
    def stop():
        self.stopped = True

class QueueThread(Thread):
    def __init__(self, queue: Queue, **kwargs):
        self.queue = queue
        self.stopped = False
        super(QueueThread, self).__init__(**kwargs)

    def run(self) -> None:
        while not(self.stopped):
            try:
                gotten = self.queue.get()
                print(gotten)
            except Empty:
                pass

    def stop():
        self.stopped = True
