import os, signal, sys, time, json
from acceptor import Acceptor
from leader import Leader
from message import RequestMessage
from process import Process
from replica import Replica
from client import Client
from utils import *

NREPLICAS = 1
NLEADERS = 1
NREQUESTS = 100

class Env:
    def __init__(self, cluster_size, number_clients):
        self.cluster_size = cluster_size
        self.number_clients = number_clients
        self.procs = {}

    def sendMessage(self, dst, msg):
        if dst in self.procs:
            self.procs[dst].deliver(msg)

    def addProc(self, proc):
        self.procs[proc.id] = proc
        proc.daemon = True
        proc.start()

    def removeProc(self, pid):
        del self.procs[pid]

    def run(self):
        initialconfig = Config([], [], [])
        c = 0
        for i in range(self.cluster_size):
            pid = "acceptor %d.%d" % (c,i)
            Acceptor(self, pid)
            initialconfig.acceptors.append(pid)

        for i in range(NLEADERS):
            pid = "leader %d.%d" % (c,i)
            Leader(self, pid, initialconfig)
            initialconfig.leaders.append(pid)

        for i in range(NREPLICAS):
            pid = "replica %d" % i
            Replica(self, pid, initialconfig)
            initialconfig.replicas.append(pid)

        for i in range(self.number_clients):
            pid = "client %d.%d" % (c,i)
            Client(self, pid, initialconfig.replicas, NREQUESTS)

        done = False
        while not done:
            done = False
            for x in initialconfig.replicas:
                if self.procs[x].accepted - (NREQUESTS*self.number_clients) == 0:
                    time_end = time.perf_counter()
                    done = True
            time.sleep(1)

        #Timing variables
        start = self.procs[x].start_time
        acc = self.procs[x].accepted
        time_total = (time_end - start)
        per_second = int(acc/time_total)

        with open('data.txt', 'a') as outfile:
            outfile.write(str(per_second))
            outfile.write("\n")

def main(cluster_size, number_clients):
    e = Env(cluster_size, number_clients)
    e.run()
    os._exit(1)


if __name__=='__main__':
    # Find the wanted size of the cluster as a command line argument
    try:
        cluster_size = int(sys.argv[1])
        number_clients = int(sys.argv[2])
    except:
        sys.exit("The arguments are as follows (both as given as integers): \n \t size: the size of the paxos cluster \n \t treshold: upper threshold of concurrent clients\n\n  Example: ./env 3 4 \t will run the evaluation with a cluster size of 3 and threshold 4")

    # Plot the results and save them to a file
    main(cluster_size, number_clients)
