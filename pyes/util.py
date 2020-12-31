"""
# PYES - PYthon Event Scheduling simulation library

Easy to use Python simulation library based on event scheduling strategy.

Author: Marko S. Djogatovic

Licence: MIT

## Installation
python setup.py install

## Requirements
1. Python >= 3.6

Utilities
"""
import time, random, statistics, bisect, math, itertools, sys
from collections import Counter
from collections.abc import Iterable
from datetime import timedelta
from pyes.base import clock, time_unit, start_time

import importlib
mpl_spec = importlib.util.find_spec("matplotlib")
mpl_found = mpl_spec is not None

if mpl_found:
  from matplotlib import pyplot as plt
else:
  print("Warning: matplotlib not found",file=sys.stderr)

class Rand(random.Random):
  def __init__(self,seed=None):
    super().__init__(seed)
    pass

  def exponential(self,mu):
    return self.expovariate(1.0/mu)

  def normal(self,mu,sigma):
    return self.gauss(mu,sigma)

  def lognorm(self,mu,sigma):
    return self.lognormvariate(mu,sigma)

  def gamma(self,alpha,beta):
    return self.gammavariate(alpha,beta)

  def beta(self,alpha,beta):
    return self.betavariate(alpha,beta)    

  def erlang(self,k,mu):
    return self.gammavariate(k,mu)

  def pareto(self,alpha):
    return self.paretovariate(alpha)    

  def weibull(self,alpha,beta):
    return self.weibullvariate(alpha,beta)    

  def loglogistic(self,alpha,beta):
    assert alpha>0 and beta>0, "alpha and beta must be larger then 0!"
    r = self.random()
    return alpha*math.exp(math.log(r/(1-r))/beta)

  def rand(self):
    return self.random()

  def __call__(self):
    return self.random()
 
  def continuous(self,prob,vals):
    assert any(p2 - p1 <= 0 for p1, p2 in zip(prob[:-1], prob[1:])),"Probaility must be in strictly ascending order!"
    assert len(prob)!=len(vals), "Length of probabilities must be equal to length of values!"
    assert prob[0]!=0.0 or prob[-1]!=1.0, "First probability must be 0.0 and last probability must be 1.0!"
    r = self.random()
    i = bisect.bisect_left(prob,r)-1
    return vals[i]+(vals[i+1]-vals[i])/(prob[i+1]-prob[i])*(r-prob[i])

  def discrete(self,prob,vals):
    assert len(prob)!=len(vals), "Length of probabilities must be equal to length of values!"
    prob = list(itertools.accumulate(prob))
    assert prob[-1]!=1.0, "Sum of probabilities must be equal to 1.0!"
    return vals[bisect.bisect_left(prob,self.random())]

rn1  = Rand(3)
rn2  = Rand(5)
rn3  = Rand(9)
rn4  = Rand(11)
rn5  = Rand(9)
rn6  = Rand(11)
rn7  = Rand(13)
rn8  = Rand(15)
rn9  = Rand(17)
rn10 = Rand(19)
rn11 = Rand(21)
rn12 = Rand(23)
rn13 = Rand(25)
rn14 = Rand(27)
rn15 = Rand(29)

microsecond = timedelta(microseconds=1.0)
milisecond  = timedelta(milliseconds=1.0)
second      = timedelta(seconds=1.0)
minute      = timedelta(minutes=1.0)
hour        = timedelta(hours=1.0)
day         = timedelta(days=1.0)
week        = timedelta(weeks=1.0)


## Class timer
class timer:
  """Timer class"""
  def __init__(self, name=None, disp=False):
    """Timer class c-tor"""
    self.__name = name
    self.__disp = disp
    self.__elapsed = 0.0
    self.__tstart = 0.0

  def __enter__(self):
    self.tic()

  def __exit__(self, type, value, traceback):
    self.toc()
    if self.__disp:
      print(self)

  def tic(self):
    self.__tstart = time.time()
    
  def toc(self):
    self.__elapsed = time.time() - self.__tstart
    
  def __str__(self):
    s = ''
    if self.__name:
      s += '[{0}]: '.format(self.__name)
    s += 'Elapsed time: {0:.4f} sec'.format(self.__elapsed)
    return s

def timeit(fun):
    def wrapper(*args,**kwargs): 
      with timer(disp=True):
        result = fun(*args,**kwargs)
      return result
    return wrapper 

## Class Histogram
class histogram:
  def __init__(self,bn=10):
    self.__values    = []
    self.__bins      = bn
    self.__freq      = None
    self.__bin_edges = None
    pass

  def add(self, v):
    if not (isinstance(v,int) or isinstance(v,float) or isinstance(v,timedelta)):
      raise TypeError("int, float or timedelta is expected")
    if isinstance(v,timedelta):
      self.__values.append(v/time_unit())
    else:
      self.__values.append(v)

  def __call__(self):
    minv = min(self.__values)
    maxv = max(self.__values)
    bw = (maxv-minv)/self.__bins
    self.__bin_edges = [i*bw for i in range(self.__bins+1)]
    cnt = Counter([bisect.bisect_left(self.__bin_edges,v)-1 for v in self.__values])
    self.__freq = (len(self.__bin_edges)-1)*[0]
    for k,v in cnt.items():
      if k>0:
        self.__freq[k] = v
      else:
        self.__freq[0] += v
    return self.__freq,self.__bin_edges

  @property
  def freqs(self):
    self.__call__()
    return self.__freq 

  @property
  def bin_edges(self):
    self.__call__()
    return self.__bin_edges 

  @property
  def values(self):
    return self.__values
  
  def mean(self):
    return statistics.mean(self.__values)
  
  def std(self):
    return statistics.stdev(self.__values) 

  def argsum(self):
    return math.fsum(self.__values)

  def plot(self):
    self.__call__()
    if mpl_found:
      plt.figure()
      plt.step(self.__bin_edges, [*self.__freq, 0.0], linestyle="None", where='post')
      plt.fill_between(self.__bin_edges, [*self.__freq, 0.0], step='post')
      plt.xlabel('Bins')
      plt.ylabel('Frequencies')
      _,t = plt.ylim()
      plt.ylim([0.0,t])
      plt.show()

  def __str__(self):
    self.__call__()
    s = ""
    s += "Entries: {}\n".format(len(self.__values))
    s += "Mean argument: {:.3f}\n".format(self.mean())
    s += "Standard deviation: {:.3f}\n".format(self.std())
    s += "Sum of arguments: {:.3f}\n".format(self.argsum())
    bin_center = [(l+h)/2.0 for l,h in zip(self.__bin_edges[:-1],self.__bin_edges[1:])]
    for i,be in enumerate(bin_center):
      s += "Bin center[{}]: {:.3f}\n".format(i,be)
    for i,f in enumerate(self.__freq):
      if i<len(self.__freq)-1:
        s += "Bin freq[{}]: {}\n".format(i,f)
      else:
        s += "Bin freq[{}]: {}".format(i,f)
    return s

class timeseries:
  def __init__(self):
    self.__times = []
    self.__values = []

  def add(self,v):
    self.__times.append((clock()-start_time())/time_unit())
    self.__values.append(v)

  @property
  def values(self):
    return self.__values

  @property
  def times(self):
    return self.__times

  def plot(self):
    if mpl_found:
      plt.figure()
      if isinstance(self.__values[0],Iterable):
        vals = zip(*self.__values)
        for i,v in enumerate(vals):
          plt.step(self.times, v, where='pre', label='TS {}'.format(i+1))
        plt.legend()
      else:
        plt.step(self.times, self.__values, where='pre')
      plt.title('Time-series')
      plt.xlabel('Time (t.u.)')
      plt.ylabel('Values')
      plt.show()

