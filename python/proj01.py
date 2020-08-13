#1 rod = 5.0292 meters
#1 furlong = 40 rods
#1 mile = 1609.34 meters
#1 foot = 0.3048 meters
#average walking speed is 3.1 miles per hour
a=float(input("Input rods: "))
print("You input " + str(a)+ " rods.")
print("Conversions")
meters=round((5.0292*a),3)
feet=round((5.0292*a)/(0.3048),3)
miles=round((5.0292*a)/(1609.34),3)
miles2=((5.0292*a)/(1609.34))
furlongs=round((5.0292*a)/(201.168),3)
print("Meters: " + str(meters))
print("Feet: " + str(feet))
print("Miles: " + str(miles))
print("Furlongs: "+ str(furlongs))
new_variable = round((miles2*60)/(3.1),3)
print("Minutes to walk " + str(a)+ " rods: " + str(new_variable))
print("Nick has corona")
print("Justin says hi serna")
print("Visual studio test")
