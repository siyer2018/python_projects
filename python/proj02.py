quarters = 10
dimes = 10
nickels = 10
pennies = 10
quarterneeded = 0#keep track of how many quarters used 
dimesneeded = 0#keep track of how many dimes used
nickelsneeded = 0#keep track of how many nickels used
penniesneeded = 0#keep track of how many pennies used

print("Welcome to change-making program.")
print("\nStock: {} quarters, {} dimes, {} nickels, and {} pennies".format(quarters, dimes, nickels, pennies))

initial_input = float(input("Enter the purchase price (xx.xx) or 'q' to quit: "))*100
#bypass negative input
while initial_input <0:
    print("Error: purchase price must be non-negative.")
    print("\nStock: {} quarters, {} dimes, {} nickels, and {} pennies".format(quarters, dimes, nickels, pennies))
    initial_input = float(input("Enter the purchase price (xx.xx) or 'q' to quit: "))*100
money_given = float(input("Input dollars paid (int): "))*100
if money_given - initial_input != 0:
    #if money is less than needed
    while money_given - initial_input <=.00001:
        print("Error: insufficient payment.")
        money_given = float(input("Input dollars paid (int): "))*100


initial_input = money_given - initial_input
#constantly ask for input 
while initial_input >=0:

    if quarters >0 and initial_input >=25:
        initial_input -= 25
        quarters-= 1
        quarterneeded +=1
    elif initial_input >= 10 and dimes >0:
        initial_input -= 10
        dimes -= 1
        dimesneeded+=1
    elif initial_input >= 5 and nickels >0:
        initial_input -= 5
        nickels -= 1
        nickelsneeded+=1
    elif 5>initial_input>= 1 and pennies >0:
        initial_input -= 1
        pennies -= 1
        penniesneeded+=1
    elif initial_input == 0:
        print("Collect change below: ")
        if quarterneeded > 0:
            print("Quarters:",quarterneeded)
            quarterneeded = 0
        if dimesneeded >0:
            print("Dimes:",dimesneeded)
            dimesneeded = 0
        if nickelsneeded >0:
            print("Nickels:",nickelsneeded)
            nickelsneeded = 0
        if penniesneeded >0:
            print("Pennies:",penniesneeded)
            penniesneeded = 0
        elif quarters == 10 and dimes == 10 and nickels == 10 and pennies == 10:
            print("No change.")
        print("\nStock: {} quarters, {} dimes, {} nickels, and {} pennies".format(quarters, dimes, nickels, pennies))
        in_str = input("Enter the purchase price (xx.xx) or 'q' to quit: ")
        if in_str == "q":
            break
        elif float(in_str) < 0:
            print("Error")
            break
        initial_input = int(float(in_str)*100)
        money_given = int(input("Input dollars paid (int): "))*100
        initial_input = money_given - initial_input
    else:
        print("Error: ran out of coins.")
        break