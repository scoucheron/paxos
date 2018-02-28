import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

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
            size = int(sys.argv[1])
            number_clients = int(sys.argv[2])
        except:
            sys.exit("The arguments are as follows (both as given as integers): \n \t size: the size of the paxos cluster \n \t treshold: upper threshold of concurrent clients\n\n  Example: ./env 3 4 \t will run the evaluation with a cluster size of 3 and threshold 4")

        # Create a random list
        resultList = np.random.uniform(50, 10, size=number_clients)

        # Plot the results and save them to a file
        plotting(resultList, number_clients)
