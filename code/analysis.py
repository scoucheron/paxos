import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from env import Env
import sys, os, time
from env import main
import subprocess as sp

NTEST = 5

def run_test(num_accept, num_client):
    result_list = np.array([])
    stdR_list = np.array([])

    f = open("data.txt", "w")
    # For each client we spawn a subprocess which will handle it
    for x in range(num_client):
        for each in range(NTEST):
            p1 = sp.Popen(['python3', 'env.py', str(num_accept), str(x+1)])
            p1.wait()
        # Fetch the data from the file
        print("Fetching the data for client ", x)
        with open('data.txt') as datafile:
            int_list = [int(i) for i in datafile]


        #Calculate the mean value and the standardeviation
        mean, stdR = calculate_std_mean(int_list)
        time.sleep(1)

        #Append the result (mean) to the result list so it can be plotted
        result_list = np.append(result_list, mean)
        stdR_list = np.append(stdR_list, stdR)
        #Since we want to reset the file we can delete it now
        os.remove('data.txt')

    # Plot the result in PDF
    plotting(result_list, num_client, stdR_list)

def plotting(resultList, number_clients, stdR_list):
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
    print(clients)
    print(resultList)
    plt.plot(clients, resultList)

    # Force the x-axis to be only integers
    plt.xticks(clients)

    # Errorbar
    plt.errorbar(clients, resultList, stdR_list,  marker='o')

    plt.show()

    #Save the graph to a pdf
    f.savefig("Result.pdf", bbox_inches='tight')

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
        num_accept = int(sys.argv[1])
        num_client = int(sys.argv[2])
    except:
        sys.exit("The arguments are as follows (both as given as integers): \n \t size: the size of the paxos cluster \n \t treshold: upper threshold of concurrent clients\n\n  Example: ./env 3 4 \t will run the evaluation with a cluster size of 3 and threshold 4")

    run_test(num_accept, num_client)

    # Plot the results and save them to a file
    # plotting(resultList, number_clients)
