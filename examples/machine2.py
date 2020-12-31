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
--------------------------------- Machine 2 ------------------------------------
--------------------------------------------------------------------------------
The machine produces parts every 5 minutes. Parts go to quality control. Control
is performed by group of unlimited number of inspectors. Control time is 4±3
minutes. It is known that the machine produces 10% scrap.

Simulate the process of quality control for 1000 parts. Time unit is 1 minute.
--------------------------------------------------------------------------------"""

# Import simulation class
from pyes.base import simulation
# Import elapsed_time function
from pyes.base import elapsed_time
# Import random number generators RN1 and RN2
from pyes.util import rn1,rn2

# Creation of simulation object
sim = simulation()

number_of_correct_parts, number_of_bad_parts = 0, 0

# Entity class - PART
class part: pass

# Init simulation
def init():
  # Schedule arrival of a first part
  yield control_started(part()),5

# Control of part quality started
def control_started(p):
  # Schedule control duration
  yield control_finished(p),rn1.uniform(1,7)
  # Shedule arrival of next part
  yield control_started(part()),5

# Control of part quality finised
def control_finished(d):
  global number_of_correct_parts, number_of_bad_parts
  if rn2.rand()<0.9:
    number_of_correct_parts += 1
  else:
    number_of_bad_parts += 1  
  if number_of_correct_parts+number_of_bad_parts==1000:
    yield simulation.stop()


# Print text of the example
print(__doc__)

# Start simulation
sim.start(init)

# Print statistics
print("# of correct parts: {}".format(number_of_correct_parts))
print("# of bad parts: {}".format(number_of_bad_parts))
print("Simulation time: {:.2f} min".format(elapsed_time()))

input("Press ENTER to continue...")
