from pyes.base import clock, elapsed_time, start_time, time_unit
from functools import reduce
import sys

class stats:
  """Class statistics"""
  def __init__(self):
    """Class statistics c-tor"""
    # Number of calls
    self.__count = 0
    # Current number of agents 
    self.__size  = 0
    # Mainimal number of agents
    self.__min_size = sys.maxsize
    # Maximum number of agents
    self.__max_size = 0
    # Number of 'zero wait' agents
    self.__count_zw = 0
    # Total waiting time
    self.__total_time = 0.0
    # Elapsed time per state
    self.__state_time = {}
    # Moment of last state change
    self.__prev_ti = None
    # Dictonary of agents and their entry times
    self.__memory = {}

  def start(self,a,n = 1):
    if not isinstance(n,int):
      raise ValueError("stats.start - int is expected")

    if not self.__prev_ti:
      # Moment of last state change
      self.__prev_ti = start_time()

    # Number of calls
    self.__count+=1
    # Area
    if not self.__size in self.__state_time:
      self.__state_time[self.__size] = ((clock() - self.__prev_ti)/time_unit())
    else:
      self.__state_time[self.__size] += ((clock() - self.__prev_ti)/time_unit())
    # Current number of agents
    self.__size += n
    # Remember moment of last state change
    self.__prev_ti = clock()
    # Maximum number of current agents during simulation
    self.__max_size = max([self.__size, self.__max_size])
    # Pamtimo redni broj entiteta u resursu i trenutak ulaska entiteta u resurs
    self.__memory[id(a)] = clock()

  def stop(self,a,n = 1):
    if not isinstance(n,int):
      raise ValueError("stats.stop - int is expected")

    if id(a) in self.__memory:
      dt = (clock()-self.__memory[id(a)])/time_unit()
      # Ukoliko je vreme koje je transakcija provela u redu 0
      # uvecavamo broj transakcija koji nisu cekale u redu
      if abs(dt)==0.0:
        self.__count_zw += 1
      # Total time
      self.__total_time += dt
      # Calculate area
      if not self.__size in self.__state_time:
        self.__state_time[self.__size] = ((clock() - self.__prev_ti)/time_unit())
      else:
        self.__state_time[self.__size] += ((clock() - self.__prev_ti)/time_unit())
      # Reduce current number of transactions
      self.__size -= n
      # Minimal number of current agents during simulation
      self.__min_size = min([self.__size, self.__min_size])
      # Remember moment of last state change
      self.__prev_ti = clock()
      # Removing item from dictonary
      del self.__memory[id(a)]

  def finish(self):
    """Finishing statistics at the end of simulation"""
    for mt in self.__memory.values():
      self.__total_time += (clock()-mt)/time_unit()
    if not self.__size in self.__state_time:
      self.__state_time[self.__size] = ((clock() - self.__prev_ti)/time_unit())
    else:
      self.__state_time[self.__size] += ((clock() - self.__prev_ti)/time_unit())
    
  def reset(self):
    """Reset statistics"""
    self.__count      = 0
    self.__min_size   = self.__size
    self.__max_size   = 0
    self.__size       = 0
    self.__count_zw   = 0
    self.__total_time = 0.0
    self.__state_time = {}

  def clear(self):
    """Clear statistics"""
    self.reset()
    self.__min_size = sys.maxsize
    self.__prev_ti  = None
    self.__memory.clear()
  
  @property
  def count(self):
    return self.__count
  
  @property
  def size(self):
    return self.__size

  @property
  def max_size(self):
    return self.__max_size

  @property
  def min_size(self):
    return self.__min_size
  
  @property
  def count_zw(self):
    return self.__count_zw
  
  @property
  def total_time(self):
    return self.__total_time

  @property
  def mean_time(self):
    return self.__total_time / self.__count

  @property
  def mean_time_zw(self):
    if self.__count - self.__count_zw:
      return self.__total_time / (self.__count - self.__count_zw) 
    else:
      return float('nan')
  
  @property
  def average(self):
    return sum(s*t for s,t in self.__state_time.items()) / elapsed_time()
  
  def utilization(self,num_of_servers = 1):
    if not isinstance(num_of_servers,int):
      raise ValueError("stats.utilization - int is expected")
    return self.average/num_of_servers
  
  @property
  def percent_zw(self):
    return (100.0*self.__count_zw)/self.__count
