import os, signal, sys, time
from acceptor import Acceptor
from leader import Leader
from message import RequestMessage
from process import Process
from replica import Replica
from utils import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sys

NACCEPTORS = 3
NREPLICAS = 2
NLEADERS = 2
NREQUESTS = 10
NCONFIGS = 2

class Env:
    def __init__(self):
        self.procs = {}

    def sendMessage(self, dst, msg):
        if dst in self.procs:
            self.procs[dst].deliver(msg)

    def addProc(self, proc):
        self.procs[proc.id] = proc
        proc.start()

    def removeProc(self, pid):
        del self.procs[pid]

    def run(self):
        initialconfig = Config([], [], [])
        c = 0

        for i in range(NREPLICAS):
            pid = "replica %d" % i
            Replica(self, pid, initialconfig)
            initialconfig.replicas.append(pid)

        for i in range(NACCEPTORS):
            pid = "acceptor %d.%d" % (c,i)
            Acceptor(self, pid)
            initialconfig.acceptors.append(pid)

        for i in range(NLEADERS):
            pid = "leader %d.%d" % (c,i)
            Leader(self, pid, initialconfig)
            initialconfig.leaders.append(pid)

        for i in range(NREQUESTS):
            pid = "client %d.%d" % (c,i)
        for r in initialconfig.replicas:
            cmd = Command(pid,0,"operation %d.%d" % (c,i))
            self.sendMessage(r,RequestMessage(pid,cmd))
            time.sleep(1)

        for c in range(1, NCONFIGS):
            # Create new configuration
            config = Config(initialconfig.replicas, [], [])
            for i in range(NACCEPTORS):
                pid = "acceptor %d.%d" % (c,i)
                Acceptor(self, pid)
                config.acceptors.append(pid)

            for i in range(NLEADERS):
                pid = "leader %d.%d" % (c,i)
                Leader(self, pid, config)
                config.leaders.append(pid)

            # Send reconfiguration request
            for r in config.replicas:
                pid = "master %d.%d" % (c,i)
                cmd = ReconfigCommand(pid,0,str(config))
                self.sendMessage(r, RequestMessage(pid, cmd))
                time.sleep(1)


            for i in range(WINDOW-1):
                pid = "master %d.%d" % (c,i)
            for r in config.replicas:
                cmd = Command(pid,0,"operation noop")
                self.sendMessage(r, RequestMessage(pid, cmd))
                time.sleep(1)

            for i in range(NREQUESTS):
                pid = "client %d.%d" % (c,i)
            for r in config.replicas:
                cmd = Command(pid,0,"operation %d.%d"%(c,i))
                self.sendMessage(r, RequestMessage(pid, cmd))
                time.sleep(1)

    def terminate_handler(self, signal, frame):
        self._graceexit()

    def _graceexit(self, exitcode=0):
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(exitcode)

def main():
    e = Env()
    e.run()
    signal.signal(signal.SIGINT, e.terminate_handler)
    signal.signal(signal.SIGTERM, e.terminate_handler)
    signal.pause()


def plotting(resultList, number_clients):
    '''
        Plot the results and save them to a file

            @ Input:
            @ Output: a graph with the given results given as a pdf-file
    '''

    # Create a list from 0 to the number of number_clients
    clients = np.arange(1, number_clients+1)

    f = plt.figure()

    # Label the above the figure, on x-axis and on y-axis
    plt.title('users')
    plt.ylabel('Accepted proposals per seconds')
    plt.xlabel('# of concurrent clients')

    # Plot the result
    plt.plot(clients, resultList)

    # Force the x-axis to be only integers
    plt.xticks(clients)

    # Calculate the standardeviation of each step
    tr = np.array(resultList)
    stdR = np.std(tr)

    plt.errorbar(clients, resultList, stdR,  marker='o')

    plt.show()

    #Save the graph to a pdf
    #f.savefig("Result.pdf", bbox_inches='tight')

def calculate_std_mean(data):
    '''
        Calculates the given datas mean and standardeviation
            @ Input: All the data from a given number of clients in the test to find the STD and mean
            @ Output: mean and standardeviation from the data
        '''
    stdR = np.std(data)
    mean = np.mean(data)
    return mean, stdR


if __name__=='__main__':
    # Find the wanted size of the cluster as a command line argument
    try:
        size_cluster = int(sys.argv[1])
        number_clients = int(sys.argv[2])

    except:
        sys.exit("The arguments are as follows (both as given as integers): \n \t size: the size of the paxos cluster \n \t treshold: upper threshold of concurrent clients\n\n  Example: ./evalutation 3 4 \t will run the evaluation with a cluster size of 3 and threshold 4")

    # Create a random list
    resultList = np.random.uniform(5, 200, size=number_clients)

    # Plot the results and save them to a file
    plotting(resultList, number_clients)
    main()
