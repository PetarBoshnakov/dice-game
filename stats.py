import math

def prob_cal(n,q):
    # prob =  C(n,q) * (1/6)**q * (5/6)**(n-q)
    
    prob = comb_cal(n,q) * math.pow((1/6),q) * math.pow(5/6, n-q)
    return prob

def comb_cal(n,k):
    # comb = n! / ( k! ( n! * k!) )
    nfac = math.factorial(n)
    kfac = math.factorial(k)
    comb = nfac / ( kfac * math.factorial(n - k) )
    return comb

def mass_prob(n, x):
    # returns the prob to be >= x
    # prob = sum(n,x) comb (n,x) * (1/6)**x * (5/6)**n
    
    prob_mass = 0

    for i in range (x):
        prob  = prob_cal(n,i)
        prob_mass += prob
    return 1 - prob_mass


print(mass_prob(10,2))