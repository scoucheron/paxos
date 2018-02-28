from message import RequestMessage
from process import Process
from replica import Replica
from utils import *
import time

class Client(Process):
    def __init__(self, env, id, config, nreq):
        Process.__init__(self, env, id)
        self.config = config
        self.nreq = nreq
        self.env.addProc(self)

    def body(self):
        for x in range(self.nreq):
            for r in self.config:
                cmd = Command(self.id,0,"operation %d.%d" % (x, x))
                self.sendMessage(r,RequestMessage(self.id ,cmd))
