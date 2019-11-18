#! /usr/bin/python3

"""
----------------------------------------------------------------------------------------
---------------------------------  Bank model  -----------------------------------------
----------------------------------------------------------------------------------------
 A bank employs four tellers to serve its customers. Interarrival time of the customers
 is exponetialy distributed with the mean time of 2 minutes. Also, the service time is
 exponentialy distributed with the mean time of 3 min. Consider the four tellers as the
 one resource with the one joint queue. The bank opening ours are from 9 AM to 4 PM.
----------------------------------------------------------------------------------------"""
    
from pyes.base import simulation
from pyes.base import elapsed_time, start_time, time_unit, print_time
from pyes.proc import queue, resource
from pyes.util import timer
from pyes.util import rn1, rn2
from pyes.util import second, minute, hour
from datetime import datetime

# Print text of the example
print(__doc__)

# Print simulation time
print_time(False)
# Start date
start_time(datetime(2018,1,1,8))
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
service.TIME = 3 # min

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

# Timer object
t = timer()
# Start timer
t.tic()
# Execute simulation
simulation().start(init)
# End timer
t.toc()

# Finishing statistics
que.stats.finish()
teller.stats.finish()

# Printing results
results()
print(t)
input()
