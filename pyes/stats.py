"""
# PYES - PYthon Event Scheduling simulation library

Easy to use Python simulation library based on event scheduling strategy.

Author: Marko S. Djogatovic

Licence: MIT

## Installation
python setup.py install

## Requirements
1. Python >= 3.6

Statistics
"""
from pyes.base import clock, elapsed_time, CONF

class stats:
  """Class statistics"""
  def __init__(self):
    """Class statistics c-tor"""
    # Number of calls
    self.__count = 0
    # Current number of agents 
    self.__size  = 0
    # Maximum number of agents
    self.__max_size = 0
    # Number of 'zero wait' agents
    self.__count_zw = 0
    # Total waiting time
    self.__total_time = 0.0
    # 'number of agents' x 'waiting time'
    self.__area = 0.0
    # Moment of last state change
    self.__prev_ti = CONF["start_time"]
    # Dictonary of agents and their entry times
    self.__memory = {}

  def start(self,a,n = 1):
    if not isinstance(n,int):
      raise ValueError("stats.start - int is expected")

    # Number of calls
    self.__count+=1
    # Area
    self.__area += self.__size*((clock() - self.__prev_ti)/CONF["time_unit"])
    # Current number of agents
    self.__size += n
    # Remember moment of last state change
    self.__prev_ti = clock()
    # Maximum number of current agents during simulation
    self.__max_size = max([self.__size, self.__max_size])
    # Pamtimo redni broj entiteta u resursu i trenutak ulaska entiteta u resurs
    self.__memory[a] = clock()

  def stop(self,a,n = 1):
    if not isinstance(n,int):
      raise ValueError("stats.stop - int is expected")

    if a in self.__memory:
      dt = (clock()-self.__memory[a])/CONF["time_unit"]
      # Ukoliko je vreme koje je transakcija provela u redu 0
      # uvecavamo broj transakcija koji nisu cekale u redu
      if abs(dt)==0.0:
        self.__count_zw += 1
      # Total time
      self.__total_time += dt
      # Calculate area
      self.__area += self.__size*((clock() - self.__prev_ti)/CONF["time_unit"])
      # Reduce current number of transactions
      self.__size -= n
      # Remember moment of last state change
      self.__prev_ti = clock()
      # Removing item from dictonary
      del self.__memory[a]

  def finish(self):
    """Finishing statistics at the end of simulation"""
    for mt in self.__memory.values():
      self.__total_time += (clock()-mt)/CONF["time_unit"]
    self.__area += self.__size*((clock()-self.__prev_ti)/CONF["time_unit"])
  
  def reset(self):
    """Reset statistics"""
    self.__count      = 0
    self.__size       = 0
    self.__max_size   = 0
    self.__count_zw   = 0
    self.__total_time = 0.0
    self.__area       = 0.0

  def clear(self):
    """Clear statistics"""
    self.__size    = 0
    self.__prev_ti = CONF["start_time"]
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
      return 0.0
  
  @property
  def average(self):
    #if not isinstance(sim_time,float):
    #  raise ValueError("stats.finish - float is expected")    
    return self.__area / elapsed_time()
  
  def utilization(self,num_of_servers = 1):
    #if not isinstance(sim_time,float):
    #  raise ValueError("stats.utilization - float is expected")    
    if not isinstance(num_of_servers,int):
      raise ValueError("stats.utilization - int is expected")              
    return self.average/num_of_servers
  
  @property
  def percent_zw(self):
    return (100.0*self.__count_zw)/self.__count
