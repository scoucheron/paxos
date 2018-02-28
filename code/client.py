from message import RequestMessage
from process import Process
from replica import Replica
from utils import *
import time

NREQUESTS = 10

class Client(Process):
    def __init__(self, env, id, config):
        Process.__init__(self, env, id)
        self.config = config
        self.env.addProc(self)

    def body(self):
        for x in range(NREQUESTS):
            for r in self.config:
                cmd = Command(self.id,0,"operation %d.%d" % (x, x))
                self.sendMessage(r,RequestMessage(self.id ,cmd))
