
counter = 0

for k in range(1,1000000000):
    n = 7*k
    if (n**2 + 5) % 13 == 0:
        print(f"Found counterexample where k = {k}!")
        counter+=1

print(f"Number of counterexamples found = {counter}.")
    