import math

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

def mass_prob(n, x):
    '''
    Summary:
    ---
    Returns the probability to have x or more elements out of n total elements 
    In mathematical terms:
    returns the prob to be > x
    prob = sum(n,x) comb (n,x) * (1/6)**x * (5/6)**n
    

    Parameters:
    n: total number of elements
    x: the target number of elements

    Returns:
    ---
    probability that element face is greater than currrent element face
    '''
    prob_mass = 0

    for i in range (x + 1):
        prob  = prob_cal(n, i)
        prob_mass += prob

    return 1 - prob_mass


def bayes_prob(n, x, y):
    '''
    Summary:
    ---
    Calculates the Bayes probability that a dice is grater than a current number of 
    known dice

    Parameters:
    ---
    n: the number of dice
    x: curr player die face
    y: other player die face

    Returns:
    ---
    the probability that a die face is hiher that current die face

    P(AB) = P(AnB) / P(B)
    '''

    prob_curr_dice = prob_cal(n,x)  # P(B)

    prob_greater = mass_prob(n, y + 1) # P(A)
    
    # actually the Bayessian probability requires that we have the P(B|A),
    # full formula is: P(A|B) = ( P(B|A) * P(A) ) / P(B), 
    # meaning that if event A is true, what is the prob of event B
    # in dice world having 5 (ie even A) guarantees that event B (having any die 
    # # less than 5) is always true. Hence, P(A|B) is 1 when P(A) is true.
    
    bayes = prob_greater / prob_curr_dice # P(AnB) / (P(B))

    return bayes

