import pylab
STATES = {'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI','IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO','MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA','PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY'}
USERS = ["Public", "Domestic", "Industrial", "Irrigation","Livestock"]
def open_file():
    print("Water Usage Data from the US and its States and Territories.")
    while True:
        try:
            file_input = input("Input a file name: ")
            fp = open(file_input)
            break
        except FileNotFoundError:
          print("Unable to open file. Please try again.")
          continue
    return fp

def no_info_check(element):
    """this function checks if there is a number or an empty space"""
    if element == "":
        element = 0
    return float(element)
def obtain_info(line_list):
    pass
def read_file(fp):
    """converts every line into a list of tuples"""
    final_list = list()
    index = 0
    for line in fp:
        if index == 0:
            index += 1
            continue
        line_list = line.split(',')
        state = line_list[0]
        county = line_list[2]
        population = int(round(no_info_check(line_list[6])*1000))
        fresh_water = no_info_check(line_list[114])
        salt_water = no_info_check(line_list[115])
        public_water = no_info_check(line_list[18])
        domestic_water = no_info_check(line_list[26])
        industrial_water = no_info_check(line_list[35])
        irrigation_water = no_info_check(line_list[45])
        livestock_water = no_info_check(line_list[59])
        new_tuple =(state,county,population,fresh_water,\
                    salt_water,public_water,domestic_water,\
                    industrial_water,irrigation_water,livestock_water)
        final_list.append(new_tuple)
    return final_list

def compute_usage(state_list):
    """obtains certain aspects from the tuples and makes a new tuple"""
    final_list = list()
    for element in state_list:
        county = element[1]
        population = element[2]
        total_water = round(element[3] + element[4],4)
        per_person = element[3] / population
        tup = (county, float(population), element[3] + element[4], per_person)
        final_list.append(tup)
    return final_list

def extract_data(data_list, state):
    """obtains the information of the state entered"""
    new_list = list()
    for element in data_list:
        if element[0] == state:
            new_list.append(element)
        else:
            continue
    return new_list


def display_data(state_list, state):
    '''formats the information in order to display it in a proper manner'''
    title = "Water Usage in " + state + " for 2010"
    header = "{:22s} {:>22s} {:>22s} {:>22s}".format("County", \
                 "Population", "Total (Mgal/day)", "Per Person (Mgal/person)")
    print("{:^88s}".format(title))
    print(header)
    new_list = extract_data(state_list,state)
    second_list = compute_usage(new_list)
    for element in second_list:
        print("{:<22s} {:>22,.0f} {:>22.2f} {:>22.4f}".format(str(element[0]), \
                 element[1], element[2], element[3]))

def All(main_list):
    header = "{:22s} {:>22s} {:>22s} {:>22s}".format("County", \
                 "Population", "Total (Mgal/day)", "Per Person (Mgal/person)")
    final_list = compute_usage(main_list)
    title = "Water Usage in " + "ALL" + " for 2010"
    print("{:^88s}".format(title))
    print(header)
    for element in final_list:
        print("{:<22s} {:>22,.0f} {:>22.2f} {:>22.4f}".format(str(element[0]), \
                 element[1], element[2], element[3]))
    answer = input("\nDo you want to plot? ")
    if answer.upper() == "YES":
        print(final_list)
        pass#have to figure out how to plot total

        #plot_water_usage(final_list, "All")


def get_state_info(main_list,state):

    new_list = extract_data(main_list,state)
    display_data(new_list,state)
    answer = input("\nDo you want to plot? ")
    if answer.upper() == "YES":
        plot_water_usage(new_list, state)

def plot_water_usage(some_list, plt_title):
    '''
        Creates a list "y" containing the water usage in Mgal/d of all counties.
        Y should have a length of 5. The list "y" is used to create a pie chart
        displaying the water distribution of the five groups.

        This function is provided by the project.
    '''
    y =[ 0,0,0,0,0 ]

    for item in some_list:

        y[0] += item[5]
        y[1] += item[6]
        y[2] += item[7]
        y[3] += item[8]
        y[4] += item[9]


    total = sum(y)
    y = [round(x/total * 100,2) for x in y] # computes the percentages.

    color_list = ['b','g','r','c','m']
    pylab.title(plt_title)
    pylab.pie(y,labels=USERS,colors=color_list)
    pylab.show()
    #pylab.savefig("plot.png")

def main():
    
    fp = open_file()
    state = input("\nEnter state code or 'all' or 'quit': ").upper()
    main_list = read_file(fp)
    while state != "QUIT":
        if state == "ALL":
            All(main_list)
        elif state not in STATES:
            print("Error in state code. Please try again.")
        else:
            get_state_info(main_list,state)
        state = input("\nEnter state code or 'all' or 'quit': ").upper()

if __name__ == "__main__":
    main()