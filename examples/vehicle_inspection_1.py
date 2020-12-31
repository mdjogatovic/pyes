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
---------------------------------  Vehicle inspection  -------------------------------------
--------------------------------------------------------------------------------------------
Vehicles arrive at technical inspection. The last check relates to engine operation. If an 
engine is defective, the vehicle is sent to the repair department. After the repair, the 
vehicle returns to inspection. After a successful inspection, the vehicle goes to the 
parking lot. At the inspection point, where engine operation control is performed, vehicles
arrive every 10 ± 5 min. The vehicle is inspected by two workers. Vehicle inspection time 
is 20 ± 5 min. Of all vehicles inspected, 70% of them are in order  and go to parking. The 
other 30% of vehicles go to the repair department, where one worker works on the repair. 
The time required to repair the vehicle is 45 ± 15 min.

It is necessary to collect statistics of the vehicle queues at the place of inspection and
at the place of repair. Also, it is necessary to create histograms of:

1. waiting times of vehicles at the inspection,
2. waiting times of vehicles at repair.

Simulate a time period of 8 hours, and for the time unit take 0.1 min.
--------------------------------------------------------------------------------------------"""

from pyes.base import simulation
from pyes.base import clock, elapsed_time, time_unit, start_time
from pyes.proc import queue, resource
from pyes.util import rn1, rn2, rn3, rn4
from pyes.util import timer, histogram, minute, hour
from datetime import datetime

time_unit(0.1*minute)

## Class vehicle
class vehicle:
  def __init__(self):
    self.ti = 0.0*minute
  pass

# Inspection queue 
que1    = queue()
# Repear queue 
que2    = queue()
# Inspection
insp = resource(2)
# Repair
mike = resource(1)
# Histograms
hist1 = histogram()
hist2 = histogram()

## Initialization
def init():
  # Schedule first arrival event in FEC
  yield arrival(vehicle()),rn1.uniform(5,15)*minute
  # Schedule terminate simulation event
  yield terminate(),8*hour

## Event arrival - unconditional event
def arrival(v):
  # Time instant of entry in the inspection queue
  v.ti = clock()
  # Push arrived vehicles into the queue
  que1.push(v)
  # Start new inspection of the first vehicle in queue
  yield inspection()
  # Schedule new arrival
  yield arrival(vehicle()),rn1.uniform(5,15)*minute

## Event service - conditional event
def inspection():
  # If resource is available and queue is not empty
  if insp and que1:
    # Pop vehicle from the queue
    v = que1.pop()
    # Add waiting time to hsitogram
    hist1.add(clock()-v.ti)
    # Seize the passport officer
    insp.seize(v)
    # Schedule event of vehicle departure
    yield departure1(v),rn2.uniform(15,25)*minute

## Event departure - unconditional event
def departure1(v):
  # Passanger departs
  insp.release(v)
  # Start new service for the first passanger in queue
  yield inspection()
  # Check whether a vehicle is in order or not
  if rn3()<0.7:
    # Vehicles go to the parking lot.
    del v
  else:
    # Time instant of entry in the repair queue
    v.ti = clock()
    # Push arrived vehicles into the queue
    que2.push(v)
    # Start repair for the first vehicle in the queue
    yield repair()

# Event repair - conditional event
def repair():
  # If resource is available and queue is not empty
  if mike and que2:
    # Pop vehicle from the queue
    v = que2.pop()
    # Add waiting time to hsitogram
    hist2.add(clock()-v.ti)
    # Seize the repair worker
    mike.seize(v)
    # Schedule event of vehicle arrival to inspection
    yield departure2(v),rn4.uniform(30,60)*minute

## Event departure - unconditional event
def departure2(v):
  # Passanger departs
  mike.release(v)
  # Start new service for the first passanger in queue
  yield repair()
  # Push repaired vehicles into the queue
  que1.push(v)
  # Start new inspection
  yield inspection()

## Event class terminate simulation
def terminate():
  # Stop simulation
  yield simulation.stop()

# Print text of the example
print(__doc__)

## Timer
t = timer()
# Start timer
t.tic()
## Simulation
sim = simulation()
# Execute simulation
sim.start(init)
# Finishing statistics
que1.stats.finish()
insp.stats.finish()
que2.stats.finish()
mike.stats.finish()
# End timer
t.toc()
# Printing results
print("Simulation time: {0:.3f} [0.1 min]".format(elapsed_time()))
print(45*"-")
print("| Inspection queue statistics               |")
print(45*"-")
print(que1)
print(45*"-")
print("| Repeair queue statistics                  |")
print(45*"-")
print(que2)
print(45*"-")
print("| Inspection statistics                     |")
print(45*"-")
print(insp)
print(45*"-")
print("| Repair statistics                         |")
print(45*"-")
print(mike)
print(45*"-")
print("| Hist 1 statistics                         |")
print(45*"-")
print(hist1)
print(45*"-")
print("| Hist 2 statistics                         |")
print(45*"-")
print(hist2)
print(45*"-")
print(t)

## Plotting
hist1.plot()
hist2.plot()

input("Press ENTER to continue...")
