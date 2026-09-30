import random

a = input("Enter names separated by commas: ")
names = a.split(",")

b = random.choice(names)
print(f"The selected name is {b}")
b=random.randint(0,1)
print(b)
if b==0:
    print("Heads")
else:
    print("Tails")
    ##print(random.randint(1,10))
    '''print(random.randint(1,10))'''
print(help(set))