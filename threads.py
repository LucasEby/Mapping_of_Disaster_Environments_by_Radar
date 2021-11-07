# Standard Library Imports
from threading import Thread
from queue import Queue
from time import sleep
from typing import Callable

# Package Imports
None

# Self Imports
from data import Reader

class TimedThread(Thread):
    """TimedThread represents a thread that times itself and performs a timeout if timed
    """    
    def __init__(self, target: Callable, time: float = None, **kwargs):
        """__init__ initialize the thread

        Parameters
        ----------
        target : Callable
            the target function/callable
        time : float, optional
            the time in seconds until a timeout should occur if None a timeout won't occur, by default None
        """        
        super(TimedThread, self).__init__(target=target, **kwargs)
        self.target = target
        self.time = time
        self.timer = None
        self.stopped = False
    
    def run(self) -> None:
        """run runs the target
        """        
        if self.time:
            self.timer = Timer(timeout=self.time)
        
        while not(self.stopped):
            self.target()
            if self.time:
                try:
                    self.timer.run()
                except TimeOutException:
                    self.stopped = True
                    return
    
    def stop(self) -> None:
        """stop safely stops the thread (waits until the target finishes before re-calling the target)
        """        
        self.stopped = True

class ReadThread(Thread):
    """ReadThread performs a thread that reads from the IWR6843
    """    
    def __init__(self, reader: Reader, queue: Queue, wait_time: float = 0.0, **kwargs):
        """__init__ initialize the thread

        Parameters
        ----------
        reader : Reader
            the reader object that performs parsing of read packets
        queue : Queue
            the queue object to add read/parsed objects to
        wait_time : float, optional
            the time to wait to perform another read, by default 0.0
        """        
        self.reader = reader
        self.queue = queue
        super(ReadThread, self).__init__(target=self.read_func, **kwargs)
        self.target = self.read_func
        self.stopped = False
        self.wait_time = wait_time
        
    def read_func(self) -> None:
        """read_func the function that reads from the IWR6843 and puts succesful parsed packets into the queue
        """        
        result = self.reader.read()
        if result:
            self.queue.put(result)
            return
    
    def run(self) -> None:
        """run runs the target
        """    
        while not(self.stopped):
            self.target()
            sleep(self.wait_time)
    
    def stop():
        """stop safely stops the thread (waits until the target finishes before re-calling the target)
        """     
        self.stopped = True
