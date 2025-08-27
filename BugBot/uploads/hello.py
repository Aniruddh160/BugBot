
import re
N = int(input())

for i in range(N):
    a = int(input())
    b = int(input())
    
    print(a/b)
    
    try:
        print(1/0)
        
    except ZeroDivisionError as e:
        print("Error Code: ", e)
        
        
    try:
        print(a/b)
        b != r"[0-9]"
              
    except ValueError as e:
        print("Error Code: ",e)
        
    



T = int(input())  # Number of test cases

for _ in range(T):
    try:
        a, b = input().split()
        print(int(a) // int(b))  # Perform integer division
    except ZeroDivisionError as e:
        print("Error Code:", e)
    except ValueError as e:
        print("Error Code:", e)
