def prime_factorise(n, prime_factors=None):

    # Check that input is a natural number before we proceed!
    if not (isinstance(n, int) and n > 0):
        raise ValueError("Input must be a natural number")
    
    # Initialise list only once at the beginning of the algorithm
    if prime_factors == None:
        prime_factors = []

    # Base case of 1 (This is really only achieved when user inputs 1 as the number to factorise, if not the for loop handles for this)
    if n == 1: #1 is not a prime number, but neither is it a composite number
        return prime_factors

    if n > 1:
        composite_factor_found = False
        for k in range(1+1,int(n/2)+1):
            if n % k == 0:
                # At this point, since we start from the smallest number, k must be prime, so we find the
                # multiplicative inverse of k which is j. We then ensure that j is not 1 (occurs when n == 2).
                j = int(n/k)
                if j != 1:
                    composite_factor_found = True
                    prime_factors.append(k)
                break
        # Prime factor has been found, append this. These are the base cases in Strong Induction!!!
        if composite_factor_found == False:
            prime_factors.append(int(n))
            return prime_factors
        
        # Composite factor has been found, further factorise. Recursion/inductive step used here!
        else:
            prime_factorise(j, prime_factors)

    # Return full list of prime factors once recursive steps are completed.
    return(prime_factors)


results = prime_factorise(69)
print(results)
