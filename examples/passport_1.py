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
--------------------------------------------------------------------------------
----------------------------  Passport counters  -------------------------------
--------------------------------------------------------------------------------
An airport has two passport counters. Passenger arrivals at passport counters 
are according to a uniform distribution between 30 and 60 seconds. Service times
are uniformly distributed with the mean value of 60 s and half-interval of 20 s.  
It's necessary to determine the utilization of passport control officers.

Simulate the system for a time period of 12 hours. The time unit is 1 second.
--------------------------------------------------------------------------------"""
from pyes.base import simulation
from pyes.base import clock, elapsed_time, time_unit
from pyes.proc import queue, resource
from pyes.util import rn1, rn2
from pyes.util import timeseries,second,hour

time_unit(second)

## Class passanger
class passanger:
  pass

# Queue
que    = queue()
# Passport officers
passport_counters = resource(2)
# Utilization in time
util = timeseries()

## Initialization
def init():
  # Schedule first arrival event in FEC
  yield arrival(passanger()),rn1.uniform(30,60)*second
  # Schedule terminate simulation event
  yield terminate(),12*hour

## Event arrival - unconditional event
def arrival(p):
  # Push arrived passanger into the queue
  que.push(p)
  # Start new service the first passanger in queue
  yield service()
  # Schedule new arrival
  yield arrival(passanger()),rn1.uniform(30,60)*second

## Event service - conditional event
def service():
  # If resource is available and queue is not empty
  if passport_counters and que:
    # Pop passanger from the queue
    p = que.pop()
    # Seize the passport officer
    passport_counters.seize(p)
    # Capture utilization in time
    util.add((passport_counters.stats.utilization(2)))
    # Schedule event of passanger departure
    yield departure(p),rn2.uniform(40,80)*second

## Event departure - unconditional event
def departure(p):
    # Passanger departs
    passport_counters.release(p)
    # Start new service for the first passanger in queue
    yield service()

## Event class terminate simulation
def terminate():
  # Stop simulation
  yield simulation.stop()

# Print text of the example
print(__doc__)

## Simulation
sim = simulation()
# Execute simulation
sim.start(init)
# Finishing statistics
que.stats.finish()
passport_counters.stats.finish()
# Printing results
print("Simulation time: {0:.3f} seconds".format(elapsed_time()))
print(45*"-")
print("| Queue statistics                          |")
print(45*"-")
print(que)
print(45*"-")
print("| Passport officers statistics              |")
print(45*"-")
print(passport_counters)
print(45*"-")

input("Press ENTER to continue...")

# Plotting
util.plot()
