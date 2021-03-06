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

# Start time
ST   = datetime.datetime(1970,1,1,8)

# Simulation clock 
CLOCK = None

def clock():
  """Return simulation clock"""
  return CLOCK

def elapsed_time():
  """Return elapsed time"""
  return (CLOCK-CONF["start_time"])/CONF["time_unit"]

def start_time(val=None):
  """Set or get start time"""
  global CONF
  if val:
    if not isinstance(val,datetime.datetime):
      raise TypeError("datetime object is expected")
    CONF["start_time"] = val
  else:
    return CONF["start_time"]

def time_unit(val=None):
  """Set or get time unit"""
  if val:
    if not isinstance(val,datetime.timedelta):
      raise TypeError("timedelta object is expected")
    CONF["time_unit"] = val  
  else:
    return CONF["time_unit"]

def print_time(val):
  """Set print time"""
  if not isinstance(val,bool):
    raise TypeError("bool is expected")
  CONF["print_time"] = val    

class simulation:
  """Class simulation"""

  def __init__(self):
    """Simulation class c-tor"""
    # Stop flag
    self.__stop = False
    # Future event chain
    self.__fec = []


  def __execute(self,ge):
    """Executing event action"""
    if ge:
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

  def start(self,init_event,end_time=None):
    """Start simulation"""
    global CLOCK
    # Initialization of start time
    if not CLOCK:
      if isinstance(CONF['time_unit'],datetime.timedelta) and CONF["start_time"]==0.0:
        CONF["start_time"] = ST
      CLOCK = CONF["start_time"]
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

  def reset(self):
    """Reset simulation clock"""
    global CLOCK
    # Reset advance time of the events
    for i, e in enumerate(self.__fec):
      td = e[1] - CLOCK
      self.__fec[i] = (e[0],CONF["start_time"]+td,e[2])
    # Reset simulation clock
    CLOCK = CONF["start_time"]

  def clear(self):
    """Clear all events from simulation and reset simulation time"""
    global CLOCK
    # Clear FEC
    self.__fec.clear()
    # Clear simulation clock
    CLOCK = None
  
  @staticmethod
  def stop():
    """Terminate simulation"""
    return None,CLOCK,-1

