"""
# PYES - PYthon Event Scheduling simulation library

Easy to use Python simulation library based on event scheduling strategy.

Author: Marko S. Djogatovic

Licence: MIT

## Installation
python setup.py install

## Requirements
1. Python >= 3.6
"""

import datetime
import operator

# Configuration object
CONF = {"start_time":0.0,"time_unit":1.0,"print_time":False}

# Simulation clock 
CLOCK = 0.0

def clock():
  """Return simulation clock"""
  return CLOCK

def elapsed_time():
  """Return elapsed time"""
  return (CLOCK-CONF["start_time"])/CONF["time_unit"]

def start_time(val):
  """Set start time"""
  if not isinstance(val,datetime.datetime):
    raise TypeError("datetime object is expected")
  CONF["start_time"] = val

def time_unit(val):
  """Set time unit"""
  if not isinstance(val,datetime.timedelta):
    raise TypeError("timedelta object is expected")
  CONF["time_unit"] = val  

def print_time(val):
  """Set print time"""
  if not isinstance(val,bool):
    raise TypeError("bool is expected")
  CONF["print_time"] = val    

class simulation:
  """Class simulation"""

  def __init__(self):
    """Simulation class c-tor"""
    global CLOCK
    # Stop flag
    self.__stop = False
    # Future event chain
    self.__fec = []
    # Initialization of start time
    CLOCK = CONF["start_time"]

  def __execute(self,ge):
    """Executing event action"""
    for e in ge:
      if e == (None,CLOCK,-1):
        self.__stop = True
      else:
        if not isinstance(e,tuple):
          e1 = (e,CLOCK,10)
        elif len(e)==2:
          if not isinstance(e[1],datetime.timedelta) and not isinstance(e[1],datetime.datetime):
            e1 = (e[0],CLOCK+e[1]*CONF["time_unit"],10)
          elif isinstance(e[1],datetime.datetime):
            e1 = (e[0],e[1],1)
          else:
            e1 = (e[0],CLOCK+e[1],10)
        else:
          if not isinstance(e[1],datetime.timedelta) and not isinstance(e[1],datetime.datetime):
            e1 = (e[0],CLOCK+e[1]*CONF["time_unit"],e[2])
          elif isinstance(e[1],datetime.datetime):
            e1 = (e[0],e[1],e[2])
          else:
            e1 = (e[0],CLOCK+e[1],e[2])
        self.__schedule(e1)

  def __schedule(self,e):
    """Scheduling event"""
    # Add entity into list
    self.__fec.append(e)
    # FEC sorting
    self.__fec.sort(key = operator.itemgetter(1,2)) #lambda ev:(ev[1],e[2]))

  def start(self,init_event):
    """Start simulation"""
    global CLOCK
    # Execute initial event
    self.__execute(init_event())
    # Stop flag is false
    self.__stop = False
    # Execute simulation
    # Simulation is terminated if FEC list is empty
    # or stop flag is raised.
    while(self.__fec and not self.__stop):
      # First event in FEC. That event becomes current event
      event, ctime, _ = self.__fec[0]
      # Remove current event from FEC
      del self.__fec[0]
      # Phase A: Update simulation clock
      CLOCK = ctime
      # Print simulation time
      if CONF["print_time"]:
        print("Simulation time: {0}".format(CLOCK),end='\r')
      # Phase B: Execute event action
      self.__execute(event)

  def clear(self):
    """Clear all events from simulation"""
    # Clear FEC
    self.__fec.clear()

  def reset(self):
    """Reset simulation time"""
    global CLOCK
    CLOCK = CONF["start_time"]
  
  @staticmethod
  def stop():
    """Terminate simulation"""
    return None,CLOCK,-1
