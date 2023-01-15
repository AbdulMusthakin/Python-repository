# create a powersum function
def powersum(power, *args):
    '''Return the sum of each argument raised to specified power.'''
    total = 0
    for i in args:
        total += pow(i, power)
    return total


# print out the result
print(powersum(2, 3, 4))

# Path: Tests\copilot_test.py

