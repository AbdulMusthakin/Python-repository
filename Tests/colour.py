# List all ANSI color codes
for i in range(0, 256):
    print("\x1b[38;5;" + str(i) + "m" + str(i), end=" ")
    if i % 10 == 9:
        print()

# Print out text with colour that is #66023c in hex
print("\x1b[38;2;102;2;60mHello, World!\x1b[0m")

# syntax for 256 color mode
