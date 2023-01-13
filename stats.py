import math

def prob_cal(n,q):
    '''
    Summary:
    ---
    Calculates the probabilty that certain count of dice will have a particular face
    
    prob =  C(n,q) * (1/6)**q * (5/6)**(n-q)
    
    Parameters:
    ---
    n: the number of dice
    q: number of dice with particular face
    '''
    
    prob = comb_cal(n,q) * math.pow((1/6),q) * math.pow(5/6, n-q)
    return prob

def comb_cal(n,k):
    '''
    Summary:
    ---
    Calculates the number of combinations for a subset of k elements out of 
    n total number of elements

    comb = n! / ( k! ( n! * k!) )

    Parameters:
    ---
    n: total number of elements
    k: number of elements in the subset

    '''
    nfac = math.factorial(n)
    kfac = math.factorial(k)
    comb = nfac / ( kfac * math.factorial(n - k) )
    return comb

def mass_prob(n, x):
    '''
    Summary:
    ---
    Returns the probability to have x or more elements out of n total elements 
    In mathematical terms:
    returns the prob to be >= x
    prob = sum(n,x) comb (n,x) * (1/6)**x * (5/6)**n
    

    Parameters:
    n: total number of elements
    x: the target number of elements

    '''
    prob_mass = 0

    for i in range (x):
        prob  = prob_cal(n,i)
        prob_mass += prob
    return 1 - prob_mass