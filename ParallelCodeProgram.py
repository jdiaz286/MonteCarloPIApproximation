# import all the libraries needed to run program
import numpy as np
import multiprocessing
import random
import timeit 
import time
from multiprocessing import Array

# definition of monte carlo method to find pi
def monte_carlo_definition():
    # get random x and y points
    x = random.uniform(-1.0,1.0)
    y = random.uniform(-1.0,1.0)
    
    # determine if the points are in the circle of pi
    return np.square(x) + np.square(y) <= 1

# mini parallelized method
def parallel_monte_carlo_sub_act(sizeOfSubArray, completeSum, i):
    # get the smaller sized array (sizeofArray) of random points 
    completeSum[i] = sum(monte_carlo_definition() for j in range(sizeOfSubArray))

# parallelized method main call
def monte_carlo_parallel(numberOfSampleTrials: int = 1000000, numberOfProcesses: int = 6):
    sizeOfSubArray = int(numberOfSampleTrials/numberOfProcesses) # size of the mini array passed to the processes in parallel
    completeSum = Array('i', [0]*numberOfProcesses, lock=False) # instantiate array to keep track of circle points
    processes = [] # array that will hold the processes executed
    
    # loop through the amount of processes in the program (4 in this case)
    for i in range(numberOfProcesses):
        process = multiprocessing.Process(target=parallel_monte_carlo_sub_act, args=(sizeOfSubArray, completeSum, i))
        
        processes.append(process)
        process.start()
    
    # important to make sure process has enough time to execute
    for process in processes:
        process.join()

    # calculate pi
    pi = 4.0 * (sum(completeSum))/numberOfSampleTrials

    # print out the result
    print("\nParallel approximation of pi with size "+str(numberOfSampleTrials)+" and "+str(numberOfProcesses)+" workers: ", end=' ')
    print(pi)

    # return the approxamation
    return pi
    
def main() -> None:
    # keep track of the start time
    start_time = time.time()

    # run monte carlo approximation using parallel processing
    monte_carlo_parallel(1000000, 2)

    # print out the amount of seconds taken to complete
    print("--- %s seconds to complete ---" % (time.time() - start_time))

if __name__ == '__main__':
    timer_main = timeit.Timer(main)
    timer_main.repeat(repeat=1, number=1)
    
