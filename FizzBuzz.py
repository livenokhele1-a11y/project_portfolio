print("Welcome to FizzBuzz!")
n = int(input("Enter a maximum number: "))
for i in range(1, n+1):
    if i % 3 == 0 and i % 5 == 0:
        print(f"{i} - FizzBuzz")
    elif i % 3 == 0:
        print(f"{i} - Fizz")
    elif i % 5 == 0:
            print(f"{i} - Buzz")
    else:
         print(f"{i}")
         
print("Done! Checked 20 numbers.")

#This is a FizzBuzz programme that prints numbers up to a user defined maximum.
#The programme uses a modulus operator to check if the number is divisible by 3, 5, or both.
#Ultimately, the programme prints a certain string depending on the result of the modulus operation.