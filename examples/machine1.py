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
--------------------------------- Machine 1 ------------------------------------
--------------------------------------------------------------------------------
The machine produces parts every 5 minutes. Parts go to quality control. Control
is performed by group of unlimited number of inspectors. Control time is 4±3 
minutes.

Simulate the process of quality control for 8 h. Time unit is 1 minute.
--------------------------------------------------------------------------------
"""

# Import simulation class
from pyes.base import simulation
# Import elapsed_time function
from pyes.base import elapsed_time
# Import random number generator RN1
from pyes.util import rn1

# Creation of simulation object
sim = simulation()

# Number of produced and controled parts
number_of_parts = 0

# Entity class - PART
class part: pass

# Init simulation
def init():
  # Schedule arrival of a first part
  yield control_started(part()),5
  # Schedule end of the simulation
  yield stop_simulation(),8*60

# Control of part quality started
def control_started(d):
  # Schedule control duration
  yield control_finished(d),rn1.uniform(1,7)
  # Shedule arrival of next part
  yield control_started(part()),5

# Control of part quality finised
def control_finished(d):
  global number_of_parts
  number_of_parts += 1

# Stop execution of the simulation
def stop_simulation():
  # Stop simulation
  yield simulation.stop()

# Print text of the example
print(__doc__)

# Start simulation
sim.start(init)

# Print statistics
print("# of controled parts: {}".format(number_of_parts))
print("Simulation time: {:.2f} min".format(elapsed_time()))

input("Press ENTER to continue...")
