###########################################################
#  Computer Project #8
#
#  Prompt for file name 
#  Prompt for year for peak wind speeds in that year
#        Program loops
#  Prompt to plot     
#  Display ending message
###########################################################
import pylab as py
from operator import itemgetter


def open_file():
    '''The function open_file prompts user to enter
       a filename that contains the hurricane data.
    '''
    while True:       
        filename = input("Input a file name: ")
        try:
            file_handle = open(filename, 'r')
            return file_handle
        except Exception:
            print("Unable to open file. Please try again.")
    pass

def update_dictionary(dictionary, year, hurricane_name, data):
    '''The function update_dictionary receives the dictionary,
       year, name of hurricane and tuple (data) with the coordinates,
       date, wind speed, and pressure.
    '''

    if year not in dictionary:
        dictionary[year] = {}
        dictionary[year][hurricane_name] = [data]

        return dictionary

    if hurricane_name not in dictionary[year]:
        dictionary[year][hurricane_name] = [data]

        return dictionary

    dictionary[year][hurricane_name].append(data)

    return dictionary

def create_dictionary(fp):
    '''The function create_dictionary takes the file pointer, reads the
       file, and creates the dictionary containing the hurricane records.
    '''
    dic = {}
    for row in fp:
        line = row.split()
        year = line[0]
        hurricane_name = line[1]
        lat = float(line[3])
        lon = float(line[4])
        date = line[5]
        wind = float(line[6]) if line[6].isdigit() else 0
        pressure = float(line[7]) if line[7].isdigit() else 0
        data = (lat, lon, date, wind, pressure)
        update_dictionary(dic, year, hurricane_name, data)
    fp.close()
    return dic

def display_table(dictionary, year):
    '''The function display_table receives a dictionary and year value for, and
       every hurricane in that year, it displays name of the hurricane,
       coordinate, date and value of peak wind speed.
    '''
    year_hurricane = dictionary[year]
    print("{:^70s}".format("Peak Wind Speed for the Hurricanes in " + year))
    print("{:1s}{:^63s}".format("Name","              Coordinates  Wind Speed (knots)           Date"))
    names = sorted(year_hurricane.keys())
    for name in names:
        hurricane = year_hurricane[name]
        hurricane.sort(key=itemgetter(3, 0, 1), reverse=True)
        peak = hurricane[:1][0]
        print("{:15s}{:>15s}{:>20s}{:>15s}".format(name, "( %.2f,%.2f)" % (peak[0], peak[1]), "%.2f" % peak[3], str(peak[2])))

def get_years(dictionary):
    '''The function get_years returns the oldest year and most recent in
       the dictionary.
    '''

    sorted_keys = sorted(dictionary.keys())
    return (sorted_keys[0], sorted_keys[-1])
        
def prepare_plot(dictionary, year):
    '''The function prepare_plot prepares for plotting hurricanes for the
       specified year
    '''
    year_hurricane = dictionary[year]
    names = sorted(year_hurricane.keys())
    max_speed = []
    coordinates = [ ]
    for hurricane in names:
        year_hurricane[hurricane].sort(key=itemgetter(3), reverse=True)
        max_speed.append(year_hurricane[hurricane][0][3])
        hurricane_coordinates = [(data[0], data[1]) for data in year_hurricane[hurricane]]
        coordinates.append(hurricane_coordinates)
    

    return (names,coordinates,max_speed)
    
def plot_map(year, size, names, coordinates):
    '''The function plot_map plots the hurricane trayectories for 2017. '''
    
    # The the RGB list of the background image
    img = py.imread("world-map.jpg")

    # Set the max values for the latitude and longitude of the map
    max_longitude, max_latitude = 180, 90
    
    # Set the background image on the plot
    py.imshow(img,extent=[-max_longitude,max_longitude,\
                          -max_latitude,max_latitude])
    
    # Set the corners of the map to cover the Atlantic Region
    xshift = (50,190) 
    yshift = (90,30)
    
    # Show the atlantic ocean region
    py.xlim((-max_longitude+xshift[0],max_longitude-xshift[1]))
    py.ylim((-max_latitude+yshift[0],max_latitude-yshift[1]))
	
    # Generate the colormap and select the colors for each hurricane
    cmap = py.get_cmap('gnuplot')
    colors = [cmap(i/size) for i in range(size)]
    
    
    # plot each hurricane's trajectory
    for i,key in enumerate(names):
        lat = [ lat for lat,lon in coordinates[i] ]
        lon = [ lon for lat,lon in coordinates[i] ]
        py.plot(lon,lat,color=colors[i],label=key)
    

     # Set the legend at the bottom of the plot
    py.legend(bbox_to_anchor=(0.,-0.5,1.,0.102),loc=0, ncol=3,mode='expand',\
              borderaxespad=0., fontsize=10)
    
    # Set the labels and titles of the plot
    py.xlabel("Longitude (degrees)")
    py.ylabel("Latitude (degrees)")
    py.title("Hurricane Trayectories for {}".format(year))
    py.show() # show the full map


def plot_wind_chart(year,size,names,max_speed):
    '''The function plot_wind_chart plots the maximum hurricane wind speed 
      for 2017.
    '''
    
    # Set the value of the category
    cat_limit = [ [v for i in range(size)] for v in [64,83,96,113,137] ]
    
    
    # Colors for the category plots
    COLORS = ["g","b","y","m","r"]
    
    # Plot the Wind Speed of Hurricane
    for i in range(5):
        py.plot(range(size),cat_limit[i],COLORS[i],label="category-{:d}".format(i+1))
        
    # Set the legend for the categories
    py.legend(bbox_to_anchor=(1.05, 1.),loc=2,\
              borderaxespad=0., fontsize=10)
    
    py.xticks(range(size),names,rotation='vertical') # Set the x-axis to be the names
    py.ylim(0,180) # Set the limit of the wind speed
    
    # Set the axis labels and title
    py.ylabel("Wind Speed (knots)")
    py.xlabel("Hurricane Name")
    py.title("Max Hurricane Wind Speed for {}".format(year))
    py.plot(range(size),max_speed) # plot the wind speed plot
    py.show() # Show the plot
    

def main():
    '''The main function uses functions from above'''
    fp = open_file()
    dictionary = create_dictionary(fp)
    (min_year, max_year) = get_years(dictionary)
    print("Hurricane Record Software")
    print("Records from {:4s} to {:4s}".format(min_year, max_year))
    year = None
    while not year:
        year = input("Enter the year to show hurricane data or 'quit': ")
        if year == "quit":
            return
        if not year.isdigit() or not int(year) in range(int(min_year), int(max_year) + 1):
            print("Error with the year key! Try another year")
            year = None
            continue
    display_table(dictionary, year)
    plot = input("\nDo you want to plot? Enter the year to show hurricane data or 'quit': ")
    if plot.lower() in ['y', 'yes', 'yea', 'ok']:
        names, coordinates, max_speed = prepare_plot(dictionary, year)
        size=len(names)
        plot_map(year, size, names, coordinates)
        plot_wind_chart(year, size, names, max_speed)
    
if __name__ == "__main__":
    main()