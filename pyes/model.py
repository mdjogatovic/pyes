from aes.base import agent, event,simulation
import aes.proc
import random

class model(simulation):
  def __init__(self):
    self.__model = []
    pass

class transaction(agent):
  __idc = 0
  def __init__(self):
    transaction.__idc += 1
    # Transaction id
    self.__id = transaction.__idc
    self.__mark_time = 0.0
    self.__curr_block = 0
    self.params = {}
  
  @property
  def id(self):
    return self.__id
  
  @property
  def mark_time(self):
    return self.__mark_time

  @property
  def curr_block(self):
    return self.__curr_block


class block:
  def __init__(self):
    self.__model = None
  
  def execute(self):
    pass

  @property
  def model_(self):
    return self.__model

  @model_.setter
  def model_(self,m):
    self.__model = m
  
class event_generate(event):
  # C-tor
  def __init__(self,m,t):
    super().__init__(m)
    self.agents["user"] = transaction()
    self.time += t

  # Action
  def action(self):
    pass
    
class generate(block):
  def __init__(self,fun):
    super().__init__()
    self.__fun = fun
  
  def execute(self):
    pass

class seize:
  def __init__(self, res, n=1):
    super().__init__()
    self.__res = res
    self.__n = n

  def execute(self):
    pass

class release:
  def __init__(self,res,n=1):
    super().__init__()
    self.__res = res
    self.__n = n
  
  def execute(self):
    pass

class enqueue:
  def __init__(self,que,n=1):
    super().__init__()
    self.__que = que
    self.__n = n
  
  def execute(self):
    pass

class depart:
  def __init__(self,que,n=1):
    super().__init__()
    self.__que = que
    self.__n = n
  
  def execute(self):
    pass

class advance:
  def __init__(self,fun):
    super().__init__()
    self.__fun = fun

  def execute(self):
    pass