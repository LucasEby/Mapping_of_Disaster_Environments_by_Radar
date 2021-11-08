# Standard Library Imports
from typing import Union
from time import monotonic

# Package Imports
None

# Self Imports
None

class TimeOutException(Exception):
    """TimeOutException represents an exception that occurs at a timeout
    """    
    def __init__(self, message: str = "Time out ocurred!", **kwargs):
        self.message = message
        super(TimeOutException, self).__init__(message, kwargs)

class Timer:
    """Timer is a class that helps time functions and performs timeouts
    """    
    def __init__(self, timeout: Union[None, float] = None, error_message: str = None):
        """__init__ [summary]

        Parameters
        ----------
        timeout : Union[None, float], optional
            the time in seconds until a timeout should occur if None a timeout won't occur, by default None
        error_message : str, optional
            the error message to send in a timeout, by default None
        """        
        self.timeout = timeout
        self.error_message = error_message
        self.end = 0.0
        self.start = monotonic()
    
    def run(self):
        """run run the timer

        Raises
        ------
        TimeOutException
            If the timer value exceeds the timeout value
        """        
        self.end = monotonic()
        if self.timeout:
            if (self.end-self.start) >= self.timeout:
                if self.error_message:
                    raise TimeOutException(error_message)
                else:
                    raise TimeOutException()

    def time(self) -> float:
        """time returns the timer value

        Returns
        -------
        float
            the time that was timed
        """        
        return self.end-self.start