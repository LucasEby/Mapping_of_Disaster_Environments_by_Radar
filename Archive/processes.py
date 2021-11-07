from multiprocessing import Process
from queue import Queue
from data import Reader

class ReadProcess(Process):
    def __init__(self, reader: Reader, queue: Queue, **kwargs):
        self.reader = reader
        self.queue = queue
        super(ReadProcess, self).__init__(target=self.read_func, **kwargs)
        self.target = self.read_func
        self.stopped = False
        
    def read_func(self) -> None:
        try:
            self.reader.data_port.close()
            self.reader.data_port.open()
        except:
            pass
        result = self.reader.read()
        if result:
            self.queue.put(result)
            self.reader.data_port.close()
            return
    
    def run(self) -> None:
        while not(self.stopped):
            self.target()
    
    def stop():
        self.stopped = True