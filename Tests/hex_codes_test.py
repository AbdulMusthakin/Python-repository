import secrets

for _ in range(100):
    x = int(secrets.token_hex(1), 16)
    if x == 255:
        print (x)