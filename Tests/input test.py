print("True or False - You like Turtles")
x = input().lower()
if x == "true":
    x = True
else:
    x = False
print("It is", str(x).lower(), "that you like Turtles")

dict = {
"Bob": 5,
"Jim" : 3,
"Tim": 8
}
print(sorted(dict.items(), key = lambda x:x[1]))