from message import RequestMessage
from process import Process
from replica import Replica
from utils import *

NREQUESTS = 10

class Client(Process):
  def __init__(self, env, id, conf):
    Process.__init__(self, env, id)
    self.env.addProc(self)
    self.conf = conf

  def body(self):
      for x in range(NREQUESTS):
          for r in self.conf:
              cmd = Command(self.id,0,"operation %d.%d" % (1,1))
              self.sendMessage(r,RequestMessage(self.id,cmd))
