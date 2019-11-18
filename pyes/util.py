"""
# PYES - PYthon Event Scheduling simulation library

Easy to use Python simulation library based on event scheduling strategy.

Author: Marko S. Djogatovic

Licence: MIT

## Installation
python setup.py install

## Requirements
1. Python >= 3.6

Utilities
"""
import time 
import numpy.random 
from datetime import timedelta

rn1  = numpy.random.RandomState(1)
rn2  = numpy.random.RandomState(3)
rn3  = numpy.random.RandomState(5)
rn4  = numpy.random.RandomState(7)
rn5  = numpy.random.RandomState(9)
rn6  = numpy.random.RandomState(11)
rn7  = numpy.random.RandomState(13)
rn8  = numpy.random.RandomState(15)
rn9  = numpy.random.RandomState(17)
rn10 = numpy.random.RandomState(19)
rn11 = numpy.random.RandomState(21)
rn12 = numpy.random.RandomState(23)
rn13 = numpy.random.RandomState(25)
rn14 = numpy.random.RandomState(27)
rn15 = numpy.random.RandomState(29)

microsecond = timedelta(microseconds=1.0)
milisecond  = timedelta(milliseconds=1.0)
second      = timedelta(seconds=1.0)
minute      = timedelta(minutes=1.0)
hour        = timedelta(hours=1.0)
day         = timedelta(days=1.0)
week        = timedelta(weeks=1.0)

## Class timer
class timer:
  """Timer class"""
  def __init__(self, name=None, disp=False):
    """Timer class c-tor"""
    self.__name = name
    self.__disp = disp
    self.__elapsed = 0.0
    self.__tstart = 0.0

  def __enter__(self):
    self.tic()

  def __exit__(self, type, value, traceback):
    self.toc()
    if self.__disp:
      print(self)

  def tic(self):
    self.__tstart = time.time()
    
  def toc(self):
    self.__elapsed = time.time() - self.__tstart
    
  def __str__(self):
    s = ''
    if self.__name:
      s += '[{0}]: '.format(self.__name)
    s += 'Elapsed time: {0:.4f} sec'.format(self.__elapsed)
    return s

def timeit(fun):
    def wrapper(*args,**kwargs): 
      with timer(disp=True):
        result = fun(*args,**kwargs)
      return result
    return wrapper 

