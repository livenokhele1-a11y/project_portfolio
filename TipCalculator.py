meal = input("How much was the meal? $")
percent = input("What percentage would you like to tip? %")
leave = float(meal)*float(percent)/100
print("Leave $", f"{leave:.2f}", "as a tip")



