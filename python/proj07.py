###########################################################
#  Computer Project #7
#
#  Prompt for file name for IP address location list
#  Prompt for file name for IP Address Attacks
#       Program loops 
#  Display ending message
###########################################################
import csv
import pylab
from operator import itemgetter

def open_file(message):
    """The open_file function takes in an input and checks 
        for the files existence in the computer.
        If the file is not found, it informs user to try again until 
        valid file is found.
    """
    while True:
        filename = input(message)
        try:
            file_handle = open(filename, 'r')
            return file_handle
        except Exception:
            print("File is not found! Try Again!")
def a_function(hello):
    """The function a_function takes in a string and 
    splits the string into a list and then grabs all elements and 
    converts into an int.
    """
    new_string = ""
    for element in hello.split("."):
        new_string += element.zfill(3);
    return int(new_string)
            
def read_ip_location(file):
    """The function read_ip_location receives a file object and reads
    IP addresses. The function returns a list of a 3-tuple items.
    """
    final_list = list()
    for element in file:
        element = element.strip("\n")
        new_list = element.split(",")
        main_tup = (a_function(new_list[0]),a_function(new_list[1]),\
                    new_list[2])
        final_list.append(main_tup)
    return final_list

def read_ip_attack(file):
    """The function read_ip_attack receives a file object. The function
    returns a list of tuples.
    """
    reader = csv.reader(file)
    result = []
    for row in reader:
        ip_int = int("".join([x.zfill(3) for x in row[0].split('.')]) + "000")
        ip_str = row[0] + ".xxx"
        result.append((ip_int, ip_str))
    file.close()
    return result

def read_country_name(file):
    """The function read_country_name receives a file object and reads the 
    country code and corresponding name. The function returns a list of 2
    tuples.
    """
    reader = csv.reader(file, delimiter=';')
    result = []
    for row in reader:
        result.append((row[1], row[0]))
    file.close()
    return result
    
def locate_address(ip_list, ip_attack):
    """The function locate_address searches for the IP address of one attack
    in the IP address list. If the IP attack address is foundin the list,
    return the country code.
    """
    for ip_tuple in ip_list:
        if ip_tuple[0] <= ip_attack <= ip_tuple[1]:
            return ip_tuple[2]
    return ''

def get_country_name(country_list, code):
    """The function get_country_name searches for a country_code in the list of 
    countries and return the name corresponding to the code.
    """
    for country_tuple in country_list:
        if country_tuple[0] == code:
            return country_tuple[1]
    return ''

def bar_plot(count_list, countries):
    """The function bar_plot plots count_list vs countries."""
    pylab.figure(figsize=(10,6))
    pylab.bar(list(range(len(count_list))), count_list, tick_label = countries)
    pylab.title("Countries with highest number of attacks")
    pylab.xlabel("Countries")
    pylab.ylabel("Number of attacks")
    
def main():
    """The main function calls the three functions to read the files, with
    each returning a list
    """
    display_all_data = False
    file = open_file("Enter the filename for the IP Address location list: ")
    ip_data = read_ip_location(file)
    
    file = open_file("Enter the filename for the IP Address attacks: ")
    attack_data = read_ip_attack(file)
    
    file = open_file("Enter the filename for the country codes: \n")
    country_data = read_country_name(file)
    display_all_choice = input("Do you want to display all data? ").lower()
    if display_all_choice == "yes" or display_all_choice == "y":
        display_all_data = True

    attacks_dict = {}
    for attack_ip in attack_data:
        code = locate_address(ip_data, attack_ip[0])
        if code in attacks_dict:
            attacks_dict[code] += 1
        else:
            attacks_dict[code] = 1
        if display_all_data:
            print('{} {:<15} {:>18s} {}'.format('The IP Address:',attack_ip[1],'originated from', get_country_name(country_data,code)));
    print("/n")
    attacks_list = [(k, v) for k, v in attacks_dict.items()]
    attacks_list.sort(key=itemgetter(1, 0), reverse=True)
    top_ten_attacks = attacks_list[:10]
    print("Top 10 Attack Countries")
    print("Country  Count")
    for attack in top_ten_attacks:
        print("{0:<5} {1:>8}".format(attack[0], attack[1]))

    answer = input("\nDo you want to plot? ").lower()
    if answer == "yes" or answer == "y":
        count_list = [attack[1] for attack in top_ten_attacks]
        countries = [attack[0] for attack in top_ten_attacks]
        bar_plot(count_list, countries)

if __name__ == "__main__":

    main()
    
