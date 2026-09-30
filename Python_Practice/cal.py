a=float(input("Enter first number: "))
b=float(input("Enter second number: "))
op=input("Enter operation (+, -, *, /): ")
if op=='+':
    print(f"The result is: {a+b}")
elif op=='-':
    print(f"The result is: {a-b}")
elif op=='*':
    print(f"The result is: {a*b}")
elif op=='/':
    if b!=0:
        print(f"The result is: {a/b}")
    else:
        print("Error: Division by zero")
        