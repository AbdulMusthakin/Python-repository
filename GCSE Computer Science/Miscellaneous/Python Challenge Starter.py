x = int(input("Enter money(GBP):"))
def euro(z):
    return z * 1.15
def gbp(z):
    return z * 0.87
print(f"That will be {euro(x)} euros.")
y = int(input("Enter your remaining money(euros):"))
print(f"That will be {gbp(y)} pounds.")