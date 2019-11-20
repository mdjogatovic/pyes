#! /usr/bin/python3

## # PYES - PYthon Event Scheduling simulation library
##
## Easy to use Python simulation library based on event scheduling strategy.
##
## Author: Marko S. Djogatovic
##
## Licence: MIT
##
## ## Installation
## python setup.py install
##
## ## Requirements
## 1. Python >= 3.6


"""
--------------------------------------------------------------------------------------------
------------------------------------  Bank model  ------------------------------------------
--------------------------------------------------------------------------------------------
 A bank employs four tellers to serve its customers. Interarrival time of the customers
 is exponentially distributed with the average time of 2 minutes. Also, the service time is
 exponentially distributed with the average time of 3 min. Consider the four tellers as the
 one resource with the one joint queue. The bank opening hours are from 9 AM to 4 PM.
 Simulate this system for three working days.
--------------------------------------------------------------------------------------------"""
    
from pyes.base import simulation
from pyes.base import elapsed_time, start_time, time_unit, print_time
from pyes.proc import queue, resource
from pyes.util import timer
from pyes.util import rn1, rn2
from pyes.util import second, minute, hour
from datetime import datetime

# Print simulation time
print_time(True)
# Model time unit
time_unit(second)

# Queue
que    = queue()
# Tellers
teller = resource(4)
   
# Statistics
def results():
  s = 47*"-"+'\n'
  s += "---       RESULTS OF BANK SIMULATION        ---\n"
  s += 47*"-"+'\n'
  s += "Simulation time: {0:.3f} seconds\n".format(elapsed_time())
  s += 45*"-"+'\n'
  s += "| Queue statistics                          |\n"
  s += 45*"-"+'\n'
  s += str(que)+'\n'
  s += 45*"-"+'\n'
  s += "| Teller statistics                         |\n"
  s += 45*"-"+'\n'
  s += str(teller)+'\n'
  s += 45*"-"
  print(s)

## Class user
class user:
  pass

## Initialization
def init():
  # Schedule first arrival event in FEC
  yield arrival(user()),rn1.exponential(arrival.TIME)*minute
  # Schedule terminate simulation event
  yield terminate(),terminate.TIME*hour

## Event arrival - unconditional event
def arrival(usr):
  # Push arrived user into the queue
  que.push(usr)
  # Start new service the first user in queue
  yield service()
  # Schedule new arrival
  yield arrival(user()),rn1.exponential(arrival.TIME)*minute
# Interrival time
arrival.TIME = 2.0 # min

## Event service - unconditional event
def service():
  # If resource is available and queue is not empty
  if teller and que:
    # Pop user from the queue
    usr = que.pop()
    # Seize the resource
    teller.seize(usr)
    # Schedule event of user departure
    yield departure(usr),rn2.exponential(service.TIME)*minute
# Service time
service.TIME = 3.0 # min

## Event departure - unconditional event
def departure(usr):
    # User departs
    teller.release(usr)
    # Start new service for the first user in queue
    yield service()

## Event class terminate simulation
def terminate():
  # Stop simulation
  yield simulation.stop()
# Simulation time
terminate.TIME = 8.0 # hour

def simulation_of_a_day(sim):
  ## Set start time for the simulation
  start_time(datetime(2018,11,simulation_of_a_day.DAY,8))    
  ## Simulation
  # Execute simulation
  sim.start(init)
  # Finishing statistics
  que.stats.finish()
  teller.stats.finish()
  # Printing results
  results()
  print(t)
  # Clear statistics from previous simulation
  que.clear()
  teller.clear()
  # Clear events from the model
  sim.clear()
  # Next day
  simulation_of_a_day.DAY += 1
# Day
simulation_of_a_day.DAY = 5

# Print text of the example
print(__doc__)
  
# Timer object
t = timer()
# Start timer
t.tic()
sim = simulation()
# Day 1
simulation_of_a_day(sim)
# Day 2
simulation_of_a_day(sim)
# Day 3
simulation_of_a_day(sim)
# End timer
t.toc()

input()
