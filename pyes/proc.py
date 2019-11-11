"""
Process objects - resource, queue
"""
import aes.base
import aes.stats

class queue:
  """Class queue"""
  def __init__(self,typ='fifo',stats=True):
    """Queue class c-tor"""
    super().__init__()
    # List of agents
    self.__que = []
    # Queue type
    self.__type = typ.lower()
    # Statistics
    if stats:
      self.__stats = aes.stats.stats()
    else:
      self.__stats = None
  
  def push(self,a,n=1):
    """Push agent into queue"""
    # Push agent at the end of queue
    self.__que.append(a)
    # If custom sort
    if self.__type=='custom':
      self.__que.sort()
    # Update statistics
    if self.__stats:
      self.__stats.start(a,n)

  def pop(self,n=1):
    """Pop agent from queue"""
    a = None
    if len(self.__que)>0:
      if self.__type=='fifo' or self.__type=='custom':
        a = self.__que[0]
        del self.__que[0]
      elif self.__type=='lifo':
        a = self.__que[-1]
        self.__que.pop()
    else:
      raise ValueError("queue.pop - Empty queue")
    # Update statistics
    if self.__stats:
      self.__stats.stop(a,n)
    # Return agent
    return a
  
  def __len__(self):
    """Return length of queue"""
    return len(self.__que)

  def __bool__(self):
    """Is queue empty?"""
    return self.__que!=[]

  def clear(self):
    """Clear content of queue"""
    self.__que.clear()
    if self.__stats:
      self.__stats.clear()

  def reset(self):
    if self.__stats:
      self.__stats.clear()    

  @property
  def stats(self):
    """Statistics property"""
    return self.__stats

  def __str__(self):
    s = ""
    if self.__stats:
      s += "Entries: {0}\n".format(self.__stats.count)
      s += "Current contents: {0}\n".format(self.__stats.size)
      s += "Maximum contents: {0}\n".format(self.__stats.max_size)
      s += "Percent zeros: {0:.2f}%\n".format(100.0*self.__stats.count_zw/self.__stats.count)
      s += "Mean time per unit: {0:.3f}\n".format(self.__stats.mean_time)
      s += "Mean time per unit (without zeros): {0:.3f}\n".format(self.__stats.mean_time_zw)
      s += "Average contents: {0:.3f}".format(self.__stats.average)
      pass
    return s

class resource:
  """Class resource"""
  def __init__(self,b,stats=True):
    """Resource class c-tor"""
    super().__init__()
    # Current number of occupied items in resource
    self.__num = 0
    # Capacity of resource
    self.__capacity = b
    # Statistics
    if stats:
      self.__stats = aes.stats.stats()
    else:
      self.__stats = None

  def seize(self,a=None,n=1):
    """Seize item in resource"""
    if not isinstance(n,int):
      raise ValueError("resource.seize - int is expected")
    if self.__num+n<=self.__capacity:
      # Increase number of occupied items
      self.__num += n
    else:
      raise ValueError("resource.seize - Resource is full")
    # Update statistics
    if self.__stats:
      self.__stats.start(a,n)
  
  def release(self,a=None,n=1):
    """Release item in resource"""
    if not isinstance(n,int):
      raise ValueError("resource.release - int is expected")
    if self.__num-n>=0:
      # Decrease number of occupied items
      self.__num -= n
    else:
      raise ValueError("resource.release - Resource is empty")
    # Update statistics
    if self.__stats:
      self.__stats.stop(a,n)

  def __bool__(self):
    """Availability of resource"""
    return self.__num<self.__capacity

  def clear(self):
    """Clear statistics"""
    self.__num = 0
    if self.__stats:
      self.__stats.clear()

  @property
  def stats(self):
    """Statistics property"""
    return self.__stats

  def __str__(self):
    s = ""
    if self.__stats:
      s += "Entries: {0}\n".format(self.__stats.count)
      s += "Capacity: {0}\n".format(self.__capacity)
      s += "Current contents: {0}\n".format(self.__stats.size)
      s += "Maximum contents: {0}\n".format(self.__stats.max_size)
      s += "Mean time per unit: {0:.3f}\n".format(self.__stats.mean_time)
      s += "Average contents: {0:.3f}\n".format(self.__stats.average)
      s += "Utilization: {0:.2f}%".format(100*self.__stats.utilization(self.__capacity))
      pass
    return s